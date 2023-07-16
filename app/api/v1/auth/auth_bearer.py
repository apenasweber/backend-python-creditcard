from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    def __call__(self, request: Request):
        if authorization := super().__call__(request):
            if not self.verify_jwt(authorization):
                raise HTTPException(
                    status_code=403, detail="Token inválido ou expirado"
                )
            return authorization.credentials
        else:
            raise HTTPException(status_code=403, detail="Não autenticado")

    def verify_jwt(self, jwtoken: str) -> bool:
        payload = decodeJWT(jwtoken)
        return bool(payload)
