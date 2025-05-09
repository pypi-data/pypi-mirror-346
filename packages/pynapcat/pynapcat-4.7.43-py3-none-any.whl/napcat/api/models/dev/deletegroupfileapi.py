# -*- coding: utf-8 -*-
# region METADATA
"""
@tags: 文件相关
@homepage: https://napcat.apifox.cn/226658755e0
@llms.txt: https://napcat.apifox.cn/226658755e0.md
@last_update: 2025-04-27 00:53:40

@description: 

summary:删除群文件

"""
__author__ = "LIghtJUNction"
__version__ = "4.7.43"
__endpoint__ = "delete_group_file"
__id__ = "226658755e0"
__method__ = "POST"

# endregion METADATA


# region code
import logging
from typing import Literal
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# region req
class DeleteGroupFileReq(BaseModel):
    """
    删除群文件请求模型
    """
    group_id: int | str = Field(..., description="群号")
    file_id: str = Field(..., description="文件ID")
# endregion req



# region res
class TransGroupFileResultInnerResult(BaseModel):
    """
    删除群文件操作结果详情
    """
    retCode: int = Field(..., description="返回码")
    retMsg: str = Field(..., description="返回信息")
    clientWording: str = Field(..., description="客户端文案")

class TransGroupFileResult(BaseModel):
    """
    群文件操作结果
    """
    result: TransGroupFileResultInnerResult = Field(..., description="操作结果")
    successFileIdList: list[str] = Field(..., description="删除成功的文件ID列表")
    failFileIdList: list[str] = Field(..., description="删除失败的文件ID列表")

class DeleteGroupFileResData(BaseModel):
    """
    删除群文件响应数据
    """
    result: int = Field(..., description="删除结果，1为成功")
    errMsg: str = Field(..., description="错误信息")
    transGroupFileResult: TransGroupFileResult = Field(..., description="群文件操作结果详情")

class DeleteGroupFileRes(BaseModel):
    """
    删除群文件响应模型
    """
    status: Literal["ok"] = Field(..., description="响应状态")
    retcode: int = Field(..., description="响应码")
    data: DeleteGroupFileResData = Field(..., description="响应数据")
    message: str = Field(..., description="信息")
    wording: str = Field(..., description="文案")
    echo: str | None = Field(None, description="echo信息")

# endregion res

# region api
class DeleteGroupFileAPI(BaseModel):
    """delete_group_file接口数据模型"""
    endpoint: str = "delete_group_file"
    method: str = "POST"
    Req: type[BaseModel] = DeleteGroupFileReq
    Res: type[BaseModel] = DeleteGroupFileRes
# endregion api




# endregion code