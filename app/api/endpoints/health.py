from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/health', tags=['health'])


@router.get('/', response_model=dict)
async def health_check():
    try:
        return {"status": "ok", "message": "Server is healthy!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
