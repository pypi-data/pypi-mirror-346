# HenauAuth FastAPI 集成示例

本项目将 河南农业大学 OAuth 2.0 服务 与 FastAPI 应用程序集成，以便于开发者使用

## 概述

`HenauAuth` 库简化了在 FastAPI 应用程序中针对河南农业大学 OAuth 2.0 服务器验证用户的过程。 此示例展示了该库的基本设置和用法。

## 准备工作

- Python 3.10+
- FastAPI
- `henau_auth` 库 (通过 pip 安装: `pip install henau_auth`)

## 配置

1.  从河南农业大学 OAuth 2.0 服务器管理面板获取 `app_id` 和 `app_secret`。
2.  在您的 FastAPI 应用程序中配置 `HenauAuth` 客户端:

    ```python
    from fastapi import FastAPI, Request
    from henau_auth import HenauAuth

    app = FastAPI()

    client = HenauAuth(
        app_id="YOUR_APP_ID",  # 替换为您的应用程序 ID
        app_secret="YOUR_APP_SECRET",  # 替换为您的应用程序密钥
        base_url="https://oauth.henau.edu.cn"  # 授权服务器地址 (默认为 https://oauth.henau.edu.cn)
    )

    app.add_middleware(
        client.get_fastapi_middleware(),
        login_router="/login",  # 登录接口路由 (默认为 /login)
        excluded_routes=["/test"],  # 排除的路由 (不需要身份验证, 默认为 [])
        jwt_secret="YOUR_JWT_SECRET",  # JWT 密钥 (建议提供一个 32 字符的字符串)
        expires_delta=3600,  # JWT 过期时间，以分钟为单位 (默认为 3600)
        # get_user_func = lambda payload: User.get_or_none(User.open_id == payload["henau_openid"])
        # 如果提供了 get_user_func，它将在检索用户信息后被调用。
        # 该函数应返回一个用户对象，该对象将存储在 request.state.user 中。
    )


    @app.get("/login")
    async def login(request: Request, code: str):
        return {"user": request.state.user, "token": request.state.token}


    @app.get("/other")
    async def user(request: Request):
        return {"user": request.state.user}


    @app.get("/test")
    async def test(request: Request, code: str = None):
        return {"code": code, "user": request.state}
    ```

    **重要提示:** 将 `"YOUR_APP_ID"` 和 `"YOUR_APP_SECRET"` 替换为您实际的应用程序凭据。 强烈建议设置一个强大的 32 字符 `jwt_secret` 以确保安全。

## 用法

1.  运行 FastAPI 应用程序:

    ```bash
    uvicorn app:app --reload
    ```

2.  访问 `/login` 端点以启动 OAuth 2.0 流程。 您需要使用您的 `app_id` 构建授权 URL，并将用户重定向到河南农业大学 OAuth 2.0 服务器。 成功验证后，服务器会将用户重定向回您的 `/login` 端点，并提供授权 `code`。

3.  `HenauAuth` 中间件将自动处理授权码的交换以获取访问令牌，并检索用户的信息。 用户对象将在 `request.state.user` 中可用，JWT 令牌将在 `request.state.token` 中可用。

4.  受保护的路由 (即，不在 `excluded_routes` 中的路由) 将需要在 `Authorization` 标头中提供有效的 JWT 令牌。

## 接口

-   `/login`: 登录接口。 处理来自河南农业大学 OAuth 2.0 服务器的 OAuth 2.0 回调。
-   `/other`: 示例受保护的接口。 需要有效的 JWT 令牌。
-   `/test`: 示例不受保护的接口。 无需身份验证即可访问。

## 自定义用户检索 (`get_user_func`)

`app.add_middleware` 中的 `get_user_func` 参数允许您将经过身份验证的用户信息与应用程序的用户模型集成。 该函数接收来自访问令牌的有效负载，并应根据有效负载中的信息返回用户对象。 示例代码展示了如何使用有效负载中的 `open_id` 从数据库中检索用户。

## 注意

-   这是一个基本示例，可能需要根据您的特定应用程序要求进行调整。
-   确保在您的生产环境中实施适当的错误处理和安全措施。
-   有关更高级的配置选项和功能，请参阅 `henau_auth` 库文档。