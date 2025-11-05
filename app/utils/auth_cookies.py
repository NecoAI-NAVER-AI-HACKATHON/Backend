# app/utils/auth_cookies.py
from fastapi import Response
from app.core.config import configs

def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    cookie_kw = dict(
        httponly=True,
        secure=configs.COOKIE_SECURE,
        samesite=configs.COOKIE_SAMESITE,
        path=configs.COOKIE_PATH,
    )
    if configs.COOKIE_DOMAIN:
        cookie_kw["domain"] = configs.COOKIE_DOMAIN

    response.set_cookie(
        key=configs.ACCESS_TOKEN_NAME,
        value=access_token,
        max_age=configs.ACCESS_TOKEN_MAX_AGE,
        **cookie_kw,
    )
    response.set_cookie(
        key=configs.REFRESH_TOKEN_NAME,
        value=refresh_token,
        max_age=configs.REFRESH_TOKEN_MAX_AGE,
        **cookie_kw,
    )

def clear_auth_cookies(response: Response):
    response.delete_cookie(configs.ACCESS_TOKEN_NAME, path=configs.COOKIE_PATH, domain=configs.COOKIE_DOMAIN)
    response.delete_cookie(configs.REFRESH_TOKEN_NAME, path=configs.COOKIE_PATH, domain=configs.COOKIE_DOMAIN)
