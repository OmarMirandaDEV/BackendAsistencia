from fastapi import Depends, HTTPException
from app.utils.jwt import verify_token

def get_current_teacher(payload: dict = Depends(verify_token)):
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    return payload