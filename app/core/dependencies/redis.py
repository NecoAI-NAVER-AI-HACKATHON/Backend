"""
Script giả lập trigger cho workflow engine dựa trên workflow JSON.
- Kết nối Redis và push job vào queue:main theo định dạng worker mong đợi.

Usage examples:
  # kích hoạt 1 node tên cụ thể
  python trigger_simulator.py --trigger "FileUpload"
"""

import argparse
import asyncio
import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import redis.asyncio as aioredis

# ---------------- CONFIG ----------------
# REDIS_DSN = os.getenv("REDIS_DSN", "redis://localhost:6379/0")
WORKFLOW_FILE_DEFAULT = os.getenv("WORKFLOW_FILE", "workflow.json")
# MAIN_QUEUE = os.getenv("MAIN_QUEUE", "queue:main")

logger = logging.getLogger("trigger_sim")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


# ---------------- Workflow Client (OOP) ----------------
class WorkflowClient:
    """Object-oriented wrapper for Redis workflow trigger utilities.

    Usage:
                    client = WorkflowClient(dsn=..., main_queue=...)
                    await client.connect()
                    client.load_workflow(path)
                    await client.trigger_node_manual()
                    await client.close()
    """

    def __init__(self, config: Optional[Any] = None):
        self.dsn = config.get("REDIS_URL") if config else None
        self.main_queue = config.get("MAIN_QUEUE") if config else None
        self.redis: Optional[aioredis.Redis] = None
        self.workflow_def: Dict[str, Any] = {}
        self.node_by_name: Dict[str, Dict[str, Any]] = {}
        self.connections_map: Dict[str, List[str]] = {}
        self.shutdown = False

    async def connect(self) -> None:
        if not self.dsn:
            raise ValueError("Redis DSN not provided.")
        self.redis = aioredis.from_url(
            self.dsn, encoding="utf-8", decode_responses=True
        )
        try:
            await self.redis.ping()
            logger.info("Connected to Redis: %s", self.dsn)
        except Exception as e:
            logger.error("Failed connect to Redis: %s", e)
            raise

    async def close(self) -> None:
        if self.redis:
            await self.redis.aclose()

    def load_workflow(self, wf: dict | None = None) -> None:
        self.workflow_def = wf
        nodes = wf.get("nodes", [])
        self.node_by_name = {n["name"]: n for n in nodes}
        conn_map: Dict[str, List[str]] = {}
        for c in wf.get("connections", []):
            main = c.get("main", [])
            for group in main:
                for edge in group:
                    src = edge.get("sourceNode")
                    tgt = edge.get("targetNode")
                    if src and tgt:
                        conn_map.setdefault(src, []).append(tgt)
        self.connections_map = conn_map
        logger.info("Loaded workflow '%s' (%d nodes)", wf.get("name"), len(nodes))

    def find_trigger_node(self) -> Optional[Dict[str, Any]]:
        for _, node in self.node_by_name.items():
            ntype = (node.get("type") or "").lower()
            if ntype == "trigger":
                return node
        return None

    def make_job(
        self,
        instance_id: str,
        node_name: str,
        payload: Dict[str, Any],
        exec_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        if exec_id is None:
            exec_id = str(uuid.uuid4())
        job = {
            "job_id": str(uuid.uuid4()),
            "instance_id": instance_id,
            "node_name": node_name,
            "payload": payload or {},
            "exec_id": exec_id,
            "created_at": int(time.time()),
            "workflow_id": self.workflow_def.get("id"),
            "is_trigger_job": True,
        }
        return job

    async def enqueue_job(
        self, instance_id: str, node_name: str, payload: Dict[str, Any]
    ) -> None:
        if not self.redis:
            raise RuntimeError(
                "Redis connection not established. Call connect() first."
            )
        job = self.make_job(instance_id, node_name, payload)
        await self.redis.lpush(self.main_queue, json.dumps(job))
        logger.info(
            "Enqueued job: instance=%s node=%s job_id=%s",
            instance_id,
            node_name,
            job["job_id"],
        )

    async def trigger_node_manual(self) -> None:
        """Trigger the first node with type 'trigger' in the loaded workflow."""
        node = self.find_trigger_node()
        if not node:
            logger.error("No trigger node found in workflow")
            return
        node_name = node["name"]
        instance_id = str(uuid.uuid4())
        payload = {
            "trigger": "manual",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        if node.get("parameters"):
            payload.update(node["parameters"])
        await self.enqueue_job(instance_id, node_name, payload)


# ---------------- Main ----------------
# async def main(args):
#     client = WorkflowClient(dsn=REDIS_DSN, main_queue=MAIN_QUEUE)
#     await client.connect()
#     client.load_workflow(args.workflow)
#     # run one-off trigger
#     await client.trigger_node_manual()
#     # close redis
#     await client.close()


# def parse_args():
#     p = argparse.ArgumentParser(description="Workflow trigger (Redis queue)")
#     p.add_argument(
#         "--workflow",
#         "-w",
#         default=WORKFLOW_FILE_DEFAULT,
#         help="Path to workflow JSON file",
#     )
#     return p.parse_args()


# if __name__ == "__main__":
#     args = parse_args()
#     try:
#         asyncio.run(main(args))
#     except KeyboardInterrupt:
#         logger.info("Interrupted by user")
#         sys.exit(0)
