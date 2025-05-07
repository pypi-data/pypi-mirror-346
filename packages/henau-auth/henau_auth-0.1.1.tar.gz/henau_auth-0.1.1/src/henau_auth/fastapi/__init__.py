from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .jwt import verify_token, create_access_token
from starlette.responses import JSONResponse
import random


class HenauAuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        login_router: str = "/login",
        excluded_routes: list[str] = None,
        get_user_func: callable = None,
        oauth2_user_func: callable = None,
        expires_delta: int = 3600,
        jwt_secret: str = "".join(
            [
                random.choice(
                    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                )
                for i in range(32)
            ]
        ),
        *args,
        **keywords,
    ) -> None:
        super().__init__(app, *args, **keywords)
        self.login_router = login_router
        self.excluded_routes = excluded_routes if excluded_routes else []
        self.get_user_func = get_user_func
        self.oauth2_user_func = oauth2_user_func
        self.jwt_secret = jwt_secret
        self.expires_delta = expires_delta

    async def dispatch(self, request: Request, call_next):
        if request.url.path == self.login_router:
            code = request.query_params.get("code")
            try:
                payload = self.oauth2_user_func(code)
            except Exception as e:
                return JSONResponse(status_code=401, content={"message": str(e)})
            request.state.user = (
                self.get_user_func(payload) if self.get_user_func else payload
            )
            request.state.token = create_access_token(
                payload, expires_delta=self.expires_delta, jwt_secret=self.jwt_secret
            )
        else:
            if request.url.path in self.excluded_routes:
                return await call_next(request)
            request.headers.get("Authorization")
            if request.headers.get("Authorization") is None:
                return JSONResponse(status_code=401, content={"message": "未提供令牌"})
            else:
                token = request.headers.get("Authorization").split(" ")[1]
                try:
                    payload = verify_token(token, jwt_secret=self.jwt_secret)
                    request.state.user = (
                        self.get_user_func(payload) if self.get_user_func else payload
                    )
                except Exception as e:
                    return JSONResponse(
                        status_code=401, content={"message": "令牌错误"}
                    )
        return await call_next(request)
