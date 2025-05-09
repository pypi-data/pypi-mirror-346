# -*- coding: utf-8 -*-
# region METADATA
"""
@tags: 群聊相关
@homepage: https://napcat.apifox.cn/230897177e0
@llms.txt: https://napcat.apifox.cn/230897177e0.md
@last_update: 2025-04-27 00:53:41

@description: 

summary:群打卡

"""
__author__ = "LIghtJUNction"
__version__ = "4.7.43"
__endpoint__ = "send_group_sign"
__id__ = "230897177e0"
__method__ = "POST"

# endregion METADATA


# region code
import logging
from typing import Literal
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# region req
class SendGroupSignReq(BaseModel):
    """
    请求模型
    """
    group_id: str = Field(..., description="群号")
# endregion req



# region res
class SendGroupSignRes(BaseModel):
    """
    响应模型
    """
    retcode: int = Field(..., description="状态码")
    status: Literal["ok", "failed"] | str = Field(..., description="状态")
    data: dict = Field(..., description="响应数据")
    msg: str = Field(..., description="信息")
# endregion res

# region api
class SendGroupSignAPI(BaseModel):
    """send_group_sign接口数据模型"""
    endpoint: str = "send_group_sign"
    method: str = "POST"
    Req: type[BaseModel] = SendGroupSignReq
    Res: type[BaseModel] = SendGroupSignRes
# endregion api




# endregion code