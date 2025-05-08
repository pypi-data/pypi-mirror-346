import sys
from .cli import CommandBase

class ExtendCommandBase(CommandBase):
    def get_moduleName(self):
        """
        模块名，默认实现为本类中的模块，如果不在本模块扩展，则需派生类重写此方法
        """
        modulename = sys.modules[__name__]
        return modulename       
 
# 获取 fw 版本信息
class GetFWVersionRequest(ExtendCommandBase):
    def __init__(self):
        super().__init__()
        self.moduleid = 4
        self.msgid = 27


class GetFWVersionResponse(ExtendCommandBase):
    def __init__(self):
        super().__init__()
        self.versioninfo = ''

    def loadbytes(self, data: bytes):
        super().loadbytes(data)
        self.versioninfo = bytes.decode(
            self.payload, encoding='utf-8', errors='ignore').strip('\0')
    def __str__(self):
        return f'{self.versioninfo}'