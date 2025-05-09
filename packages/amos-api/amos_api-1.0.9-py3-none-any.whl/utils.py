from pydantic import BaseModel, Field, PositiveInt
from typing import Annotated, Any
from enum import Enum


class CheckAssertionError(AssertionError):
    """
    校验错误,Assertion
    """
    pass


class CheckValueError(ValueError):
    """
    校验错误,Value
    """
    pass


class CheckTypeError(TypeError):
    """
    校验错误,类型
    """
    pass


class AlgorithmKnownError(ValueError):
    """
    算法错误,已知,在计算过程中出现的已知错误
    """
    pass


class UnknownError(ValueError):
    pass


class HttpCode(PositiveInt, Enum):
    _200 = 200  # 成功
    _400 = 400
    _422 = 422  # 校验错误
    _403 = 403
    _404 = 404

    _500 = 500
    _522 = 522  # 算法错误
    _523 = 523  # 算法错误,已知,在计算过程中出现的已知错误
    _599 = 599  # 未知错误


class ResponseBase(BaseModel):
    code: Annotated[
        HttpCode,
        Field(
            title='code',
            description='状态码'
        )
    ] = HttpCode._200
    msg: Annotated[
        str,
        Field(
            title='msg',
            description='状态描述',
            min_length=1
        )
    ] = '成功'
    data: Annotated[
        Any,
        Field(
            title='data',
            description='详细信息'
        )
    ]


class ResponseOK(BaseModel):
    code: Annotated[
        PositiveInt,
        Field(
            title='code',
            description='状态码'
        )
    ] = HttpCode._200
    msg: Annotated[
        str,
        Field(
            title='msg',
            description='状态描述',
            min_length=1
        )
    ] = '成功'
    data: Annotated[
        Any,
        Field(
            title='data',
            description='格式化后的算法结果'
        )
    ] = {'html': '', 'data': {}}


class ResponseValidationError(BaseModel):
    code: Annotated[
        PositiveInt,
        Field(
            title='code',
            description='状态码'
        )
    ] = HttpCode._422
    msg: Annotated[
        str,
        Field(
            title='msg',
            description='状态描述',
            min_length=1
        )
    ] = '校验错误'
    data: Annotated[
        str,
        Field(
            title='data',
            description='错误详细信息'
        )
    ] = ''


class ResponseAlgorithmError(BaseModel):
    code: Annotated[
        PositiveInt,
        Field(
            title='code',
            description='状态码'
        )
    ] = HttpCode._522
    msg: Annotated[
        str,
        Field(
            title='msg',
            description='状态描述',
            min_length=1
        )
    ] = '算法错误'
    data: Annotated[
        str,
        Field(
            title='data',
            description='错误详细信息'
        )
    ] = ''


class ResponseAlgorithmKnownError(BaseModel):
    code: Annotated[
        PositiveInt,
        Field(
            title='code',
            description='状态码'
        )
    ] = HttpCode._523
    msg: Annotated[
        str,
        Field(
            title='msg',
            description='状态描述',
            min_length=1
        )
    ] = '算法错误(已知)'
    data: Annotated[
        str,
        Field(
            title='data',
            description='错误详细信息'
        )
    ] = ''
