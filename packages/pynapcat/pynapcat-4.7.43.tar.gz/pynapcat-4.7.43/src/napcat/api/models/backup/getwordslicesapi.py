# -*- coding: utf-8 -*-
# region METADATA
"""
@tags: 其他/bug
@homepage: https://napcat.apifox.cn/228534368e0
@llms.txt: https://napcat.apifox.cn/228534368e0.md
@last_update: 2025-04-26 01:17:45

@description: 

summary:获取中文分词

"""
__author__ = "LIghtJUNction"
__version__ = "4.7.17"
__endpoint__ = ".get_word_slices"
__id__ = "228534368e0"
__method__ = "POST"

# endregion METADATA


# region code
import logging
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# region req
class GetWordSlicesReq(BaseModel):
    """
    获取中文分词 请求模型
    "

    # API spec defines an empty request object
    pass
# endregion req



# region res
class GetWordSlicesRes(BaseModel):
    """
    获取中文分词 响应模型
    "
    # API spec defines an empty response object
    pass
# endregion res

# region api
class GetWordSlicesAPI(BaseModel):
    """.get_word_slices接口数据模型"""
    endpoint: str = ".get_word_slices"
    method: str = "POST"
    Req: type[BaseModel] = GetWordSlicesReq
    Res: type[BaseModel] = GetWordSlicesRes
# endregion api




# endregion code