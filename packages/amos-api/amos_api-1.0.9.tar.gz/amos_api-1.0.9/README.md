# amos api

主要用于定义离线分析中的 API 规范以及通用的 Response 等

## 快速开始

```py
import logging
from fastapi import (FastAPI, Body)
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from amos_api import (
    ResponseBase,
    ResponseOK,
    ResponseValidationError,
    ResponseAlgorithmError,
    CheckAssertionError,
    CheckValueError
)

from starlette.responses import RedirectResponse

logger = logging.getLogger()

async def document():
    # return RedirectResponse(url="/docs")
    return RedirectResponse(url="/redoc")

def mount_app_routes(app: FastAPI):
    app.get("/",
            response_model=ResponseBase,
            summary="swagger 文档")(document)
    # tag items
    app.post("/user",
             tags=["User"],
             summary="用户信息",
             )(userInfo)

async def userInfo(name: str=Body(..., description="用户名称", examples=["ray"])) -> ResponseBase:
    return ResponseBase(data={"seq":"1", "name": name,})

async def userList(name: str=Body(..., description="用户名称", examples=["ray"])) -> ResponseBase:
    try:
        dblist()
        return ResponseOK(data=[])
    except Exception as e:
        if isinstance(e, (ValidationError, CheckAssertionError, CheckValueError)):
            ret = ResponseValidationError(data='校验错误的详细信息')
        else:
            ret = ResponseAlgorithmError(data='算法错误的详细信息')
        logger.error() #错误日志
        return JSONResponse(status_code=ret.code, content=ret.model_dump())
```

- `HttpCode._200` 请求成功,正常 code 值，ResponseBase 如果不设置code时，默认值。
- `HttpCode._400` 错误的请求，比如参数错误
- `HttpCode._403` 禁止访问的资源
- `HttpCode._404` 未找到
- `HttpCode._422` 常用于参数错误
- `HttpCode._500` 服务器错误，内部错误
- `HttpCode._522` 服务器错误，内部错误
- `HttpCode._523` 服务器错误，内部错误,已知
  