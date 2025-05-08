#!/usr/bin/python
# -*- coding: utf-8 -*-

import struct
import binascii
import sys
from abc import ABCMeta
from enum import IntEnum
from typing import List


class CLI_DATA_OPERATION_TYPE(IntEnum):
    REG = 0
    RAM = 1
    FLASH = 2
    REG_GROUP = 3
    MAX = 4

class CLI_DEST(IntEnum):
    LOCAL = 0
    MASTER_ONLY = 1
    SLAVE_ONLY = 2
    MASTER_AND_SLAVE = 3
    MAX = 4


start = bytes([0x23, 0x23])
end = bytes([0x40, 0x40])
header_struct = '<2s3H2B2H'  # 12+6*2 24
header_len = struct.calcsize(header_struct)

# def parseCommand(data=b''):
#     """
#     return an object instanct of CommandBase
#     """
#     rep = CommandBase()
#     if len(data) >= header_len:
#         lst=struct.unpack(header_struct, data[0:header_len])
#         [start, moduleid, crc, msgid, ack, length, seqnum.end]=lst
#         if len(data) >= header_len + length:
#             payload=data[header_len:]
#         if(moduleid==4 and msgid==1):
#             rep=GetVersionResponse()
#     return rep

# 扩展cli步骤
# 1.继承基类CommandBase
# 2.请求类名以Requset结尾，响应类以Response结尾
# 3.如果不在cli模块里面实现，就得重写基类的get_moduleName方法
# 4.如果类名不按照命名约定，需重写基类的get_instanceName方法
# 5.payload内容解析自行实现，参照GetVersionResponse


class CommandBase:
    """
    Derived classes come in pairs, with Request and Response classes ending in Request and Response, respectively
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.start = start
        self.moduleid = 0
        # self.crc = 0
        self.msgid = 0
        self.ack = 0
        self.result = 0
        # self.len=0
        self.seqnum = 0
        self.payload = b''
        self.end = end

        self.hasresponse = True

    @property
    def length(self):
        pl = self.getpayload()
        return len(pl) if pl else 0

    @property
    def crc(self):
        if self.length > 0:
            return binascii.crc32(self.getpayload()) & 0xFFFF
        return 0

    def loadbytes(self, data: bytes):
        if len(data) >= header_len:
            lst = struct.unpack(header_struct, data[0: header_len])
            [self.start, self.moduleid, crc, self.msgid,
                self.ack, self.result, length, self.seqnum] = lst
        if len(data) >= header_len + self.length:
            self.payload = data[header_len: len(data) - 2]

    def getbytes(self):
        return (self.start +
                struct.pack('<3H2B2H', self.moduleid, self.crc, self.msgid, self.ack,self.result, self.length, self.seqnum) +
                self.getpayload() +
                self.end)

    def check(self, cmd: 'CommandBase'):
        return True

    def getpayload(self):
        """
        子类重写,默认返回payload
        """
        return self.payload

    def getresponse(self) ->'CommandBase':
        """
        return an Response object instance of CommandBase by the Request
        """
        modulename = self.get_moduleName()
        insName = self.get_instanceName()
        objaddr = getattr(modulename, insName)
        obj = objaddr()
        return obj

    def get_moduleName(self):
        """
        模块名，默认实现为本类中的模块，如果不在本模块扩展，则需派生类重写此方法
        """
        modulename = sys.modules[__name__]
        return modulename

    def get_instanceName(self):
        """
        响应类名，默认约定请求类为Request结束，响应类为Response结束，如不是以此命名，则需派生类重写此方法,返回对应响应类的类名
        """
        name = self.__class__.__name__
        resname = name.replace('Request', 'Response')
        return resname

    def __str__(self):
        return 'moduleid:{0}, msgid:{1}, len={2}, payload:{3},seqnum={4}'.format(self.moduleid,
                                                                      self.msgid,
                                                                      self.length,
                                                                      self.getpayload().hex(),self.seqnum)


class GetVersionRequest(CommandBase):
    def __init__(self):
        super().__init__()
        self.moduleid = 4
        self.msgid = 0


class GetVersionResponse(CommandBase):
    def __init__(self):
        super().__init__()
        self.sw_ver = 0
        self.soc_id = []
        self.reserver = bytes([0] * 72)

    def loadbytes(self, data):
        super().loadbytes(data)
        [self.sw_ver, *self.soc_id] = struct.unpack('<3I', self.payload[0:12])

    def __str__(self):
        # print(self.payload[0:12].hex())
        return 'moduleid:{0}, msgid:{1}, len={2}, sw_ver:{3}, soc_id:{4}'.format(self.moduleid,
                                                                                 self.msgid,
                                                                                 self.length,
                                                                                 '%#x' % self.sw_ver,
                                                                                 self.soc_id)
class DCoreStream:
    def __init__(self,id:int,num:int,name :str) -> None:
        self.id :int = id
        self.num :int = num
        self.name :str = name
        self.processorlist:List[Processor]=[]
    def __str__(self) -> str:
        # for d in self.processorlist:
        #     print(f'{d}')
        return f'id={self.id},name={self.name},num={self.num}'
class Processor:
    def __init__(self,id:int,name :str) -> None:
        self.id:int = id
        self.name = name
    def __str__(self) -> str:
        return f'{self.name}({hex(self.id)})'
class SyncDCoreStreamRequest(CommandBase):
    def __init__(self,):
        super().__init__()
        self.moduleid = 8
        self.msgid = 322
class SyncDCoreStreamResponse(CommandBase):
    def __init__(self):
        super().__init__()
        self.dumpnames= ['TONE','MUSIC','CALL_UP','CALL_DOWN','AANC','LOOPBACK','FEEDBACK','REOORD','MIC','SIGNAL','LOOPBACK_RX','USB']
        self.dcorelist :List[DCoreStream]= []
    def loadbytes(self, data: bytes):
        super().loadbytes(data)
        if not self.payload:
            return
        index = 0
        while index < len(self.payload):
            id = int.from_bytes(self.payload[index:index+1],byteorder='little')
            num = int.from_bytes(self.payload[index+1:index+2],byteorder='little')
            #print(f'num={num}')
            name = self.dumpnames[id-1] if id>0 and id <= len( self.dumpnames) else 'unknown'
            ds =DCoreStream(id,num,name)
            index += 2
            for i in range(num):
                pid = i
                e_index = self.payload.find(b'\0',index)
                #print(f'e_index={e_index}')
                pname = bytes.decode(self.payload[index:e_index])
                p = Processor(pid,pname)
                ds.processorlist.append(p)
                index = e_index + 1
            self.dcorelist.append(ds)
    def __str__(self):
        # for d in self.dcorelist:
        #     print(f'{d}')
        return f''

class UsbInitRequest(CommandBase):
    def __init__(self,enable = True):
        super().__init__()
        self.moduleid = 4
        self.msgid = 43
        self.enable = enable
    def getpayload(self):
        return struct.pack('<B',1 if self.enable else 0)
class UsbInitResponse(CommandBase):
    def __init__(self):
        super().__init__()
 
class IPoint:
    def getbytes(self):
        return b''*4
class ACorePoint(IPoint):
    def __init__(self,srcid:int,sampleid:int,channel:int) -> None:
        self.srcid = srcid
        self.sampleid = sampleid
        self.channel = channel
    def getbytes(self):
        return struct.pack('<H2B', self.srcid,self.channel,self.sampleid)
class DCorePoint(IPoint):
    def __init__(self,streamid:int,processorid:int,channel:int) -> None:
        self.streamid= streamid
        self.processorid= processorid
        self.channel = channel
    def getbytes(self):
        return struct.pack('<H2B', self.streamid,self.channel,self.processorid)
class AudioDumpStartRequest(CommandBase):
    def __init__(self,dumpway:int,core:int,ack:bool,points:List[IPoint] = []):
        super().__init__()
        self.moduleid = 8
        self.msgid = 320
        self.dumpway = dumpway
        self.core = core
        self.ack = ack
        self.points = points
    @property
    def count(self):
        return len(self.points)
    def getpayload(self):
        pl = b''
        for point in self.points:
            pl+=point.getbytes()
        return struct.pack('<4B', self.dumpway,self.core,1 if self.ack else 0,self.count) + pl
class AudioDumpStartResponse(CommandBase):
    def __init__(self):
        super().__init__()
class AudioDumpStopRequest(CommandBase):
    def __init__(self):
        super().__init__()
        self.moduleid = 8
        self.msgid = 321
class AudioDumpStopResponse(CommandBase):
    def __init__(self):
        super().__init__()
