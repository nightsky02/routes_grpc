from fastapi import Request, HTTPException
import app_settings
import jwt

def extract_token(request: Request) -> str:
    data = request.headers.get("Authorization")

    if data is None:
        raise HTTPException(
            status_code=401,
            detail="No given token"
        )

    try:
        jwt.decode(data, app_settings.JWT_SIGN_KEY, app_settings.JWT_ALG)
    except jwt.InvalidTokenError as err:
        raise HTTPException(
            status_code=401,
            detail="Invalid token (maybe expired, or the wrong structure)"
        )

    return data