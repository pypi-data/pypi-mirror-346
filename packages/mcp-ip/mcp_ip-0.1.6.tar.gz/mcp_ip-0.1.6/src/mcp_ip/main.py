
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware


server = FastAPI(
    title="获取IP API",
    version="1.0.0",
    description="根据当前请求获取其公网IP地址",
)


origins = ["*"]

server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@server.get("/get_log_client_ip", summary="获取当前客户端IP")
async def log_client_ip(request: Request)-> str:
    # 获取真实 IP（支持反向代理）
    client_ip = (
            request.headers.get("x-forwarded-for", "").split(",")[0]
            or request.client.host
    )
    # 将 IP 存入请求状态，供后续路由使用
    request.state.client_ip = client_ip
    print(f"Client IP: {client_ip}")  # 打印到日志
    return client_ip


# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(server, host="0.0.0.0", port=8001)
# def main():
#     import uvicorn
#     """启动 FastAPI 服务器"""
#     uvicorn.run(app, host="0.0.0.0", port=8000)
#
# if __name__ == "__main__":
#     main()