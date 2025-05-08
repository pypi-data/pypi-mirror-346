#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import logging
import os
from typing import Dict, List, Union
from   .btsnoop import BTSnoop
import serial
import threading
import struct
import datetime
import time
from .decode import AudioDumpData, LogBase, UartDecode, Ack, DumpData, StringLog,audio_header_len,audio_header_fmt,AudioDumpDataHeader
from .cli import CommandBase
from .utility import getPrevNumber,  getRangeNumber
from enum import Enum
class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    CRITICAL = 3
class Request:
    def __init__(self, clicmd: CommandBase, resmsgid: int = -1):
        self.clicmd = clicmd
        self.event = threading.Event()
        self.result = b''
        self.resmsgid = resmsgid  # 匹配回应的msgid
        self.check = False
        self.cliresult = -1
    def wait(self, timeout=5):
        return self.event.wait(timeout)

    def reset(self):
        self.event.set()


class Response:
    def __init__(self):
        self.success = False
        self.msg = ''
        self.cliresult = -1
        self.cmd:Union[CommandBase,None] = None  # CommandBase
class BufferMemoryStream:
    def __init__(self) -> None:
        self.buffsize = 20*1024*1024
        self.readindex = 0
        self.writeindex = 0
        self.data = bytearray(self.buffsize)
    def write(self,data:bytes):
        count = len(data)
        if self.length + count > self.buffsize:
            raise Exception('buff fulled.')
        wp = self.writeindex % self.buffsize
        if wp+count>self.buffsize:
            self.data[wp:] = data[0:self.buffsize-wp]
            self.data[0:wp+count-self.buffsize] = data[self.buffsize-wp:]
        else:
            self.data[wp:wp+count] = data
        self.writeindex +=count
    def read(self,length:int=-1)->bytes:
        len = length if length!=-1 else self.length
        rp = self.readindex % self.buffsize
        result = b''
        if rp + len > self.buffsize:
            result += self.data[rp:]
            result += self.data[0:rp + len - self.buffsize]
        else:
            result += self.data[rp:rp + len]
        self.readindex+=len
        return result

    @property
    def length(self)->int:
        return self.writeindex - self.readindex
class WqUart:
    def __init__(self,
                 port: str = 'COM10',
                 baudrate: int = 2000000,
                 readtimeout=0.02,
                 writetimeout=0.02,
                 logging_only: bool = False,
                 param_logger=None,
                 decode_obj=None,
                 logger_bin_file_dir=None,
                 writebin=True,
                 isdump_audio=False):
        self.port = None
        self.__port = port
        self.__baudrate = baudrate
        self.__readtimeout = readtimeout
        self.__writetimeout = writetimeout

        if decode_obj is None:
            self.decode = UartDecode()
        else:
            self.decode = decode_obj
        if logger_bin_file_dir and os.path.isdir(logger_bin_file_dir):
            self.logger_bin_file_dir = logger_bin_file_dir
        else:
            self.logger_bin_file_dir = 'logs'
            if not os.path.exists(self.logger_bin_file_dir):
                os.makedirs(self.logger_bin_file_dir)
        self.isstop = False
        self.seqnum = 0
        self.requests:Dict[int,Request] = { } # k-v :seqnum:Request
        self.lock = threading.Lock()
        self.isdump = False
        self.logDictionary = {}
        self.logging_only = logging_only
        self.ischeckmiss = True

        self.emptyTime = 10

        self.task = None
        self.onstop = None
        self.ondump = None
        self.onmessage = None
        self.on_exception = None
        self.on_unhandlehci=None
        self.on_unhandlecli=None
        self.packages = {}

        self.logger_wq_uart = param_logger
        self.buffstream = BufferMemoryStream()
        self.btsnoop = BTSnoop()
        self.writesnoop = False
        self.writebin= writebin
        self.isdump_audio = isdump_audio
        self.timefmt='%Y-%m-%d %H:%M:%S'
        self.loglevels = [LogLevel.INFO,LogLevel.WARNING,LogLevel.CRITICAL]
    def get_timespan(self):
            time = datetime.datetime.now()
            return f'{time.strftime(self.timefmt)} {time.microsecond//1000:03d}'
    def logger_debug(self, param_logger_info):
        if  LogLevel.DEBUG not in self.loglevels:
            return
        if self.logger_wq_uart and isinstance(self.logger_wq_uart, logging.Logger):
            self.logger_wq_uart.debug(str(param_logger_info))
        else:
            cur_time_stamp = self.get_timespan()
            print(f' >{cur_time_stamp} - DEBUG: {param_logger_info}')

    def logger_info(self, param_logger_info):
        if  LogLevel.INFO not in self.loglevels:
            return
        if self.logger_wq_uart and isinstance(self.logger_wq_uart, logging.Logger):
            self.logger_wq_uart.info(str(param_logger_info))
        else:
            cur_time_stamp = self.get_timespan()
            print(f' >{cur_time_stamp} - INFO: {param_logger_info}')

    def logger_warning(self, param_logger_info):
        if  LogLevel.WARNING not in self.loglevels:
            return
        if self.logger_wq_uart and isinstance(self.logger_wq_uart, logging.Logger):
            self.logger_wq_uart.warning(str(param_logger_info))
        else:
            cur_time_stamp = self.get_timespan()
            print(f' >{cur_time_stamp} - WARNING: {param_logger_info}')

    def logger_critical(self, param_logger_info):
        if  LogLevel.CRITICAL not in self.loglevels:
            return
        if self.logger_wq_uart and isinstance(self.logger_wq_uart, logging.Logger):
            self.logger_wq_uart.critical(str(param_logger_info))
        else:
            cur_time_stamp = self.get_timespan()
            print(f' >{cur_time_stamp} - CRITICAL: {param_logger_info}')

    def inituart(self):
        if self.port is None:
            self.port = serial.Serial(self.__port, self.__baudrate)
            self.port.write_timeout = self.__writetimeout
            self.port.timeout = self.__readtimeout
            import platform
            os_name  = platform.system()
            if os_name.lower()=="windows":# ifsystem is linux ,do  nothing
                self.port.set_buffer_size(20*1024*1024)
    @property
    def baudrate(self):
        return self.port.baudrate

    @baudrate.setter
    def baudrate(self, value):
        self.port.baudrate = value
        pass

    def open(self):
        self.inituart()
        if not self.port.is_open:
            self.port.open()
            self.port.dsrdtr = True

    def close(self):
        if self.port is not None and self.port.is_open:
            self.port.dsrdtr = False
            self.port.close()

    def load(self, file='dbglog_table.txt',romtable=''):
        self.decode.load(file,False,romtable)

    def receive(self):
        flag = False
        lasttime = time.time()
        binfile=os.path.join(self.logger_bin_file_dir, '{0}-{1}.bin'.format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),self.__port.split('/')[-1]))
        fb =None
        if self.writebin:
            fb = open(binfile,'wb+')
        while not self.isstop:
            try:
                self.open()
                count = self.port.in_waiting
                if count > 0:
                    min_len= min(count,500)
                    rdata = self.port.read(min_len)
                    #print(f'wdata={rdata.hex()}')
                    self.buffstream.write(rdata)
                    if fb:
                        fb.write(rdata)
                    if flag:
                        cur = time.time()
                        if (cur - lasttime) > self.emptyTime:
                            emptymsg = 'more than {0} seconds not read data'.format(cur - lasttime)
                            self.onmessage(StringLog(emptymsg))
                    flag = False
                else:
                    time.sleep(0.001)
                    flag = True
                    lasttime = time.time()
            except BaseException as ex:
                print(ex)
                if self.on_exception:
                    self.on_exception(ex)
                time.sleep(0.001)
        if fb:
            fb.close()
        if self.onstop:
            self.onstop()

    def handle(self, msg:LogBase):
        msgtype = msg.msgtype
        if msgtype == 3:  # cli
            if msg.header_check and msg.content_check:
                [moduleid, crc, msgid, value,cliresult, length,seqnum] = struct.unpack('<3H2B2H', msg.payload[2:14])
                autoack = value & 0b1
                tp = (value>>1) & 0b111 #
                self.logger_debug(f'receive cli response:moduleid={moduleid},msgid={msgid},seqnum={seqnum}({hex(seqnum)}),tp={tp},seqnum={seqnum},threadid={threading.get_ident()},data={msg.payload.hex()}')
                if tp == 1:
                    if seqnum in self.requests:
                        req = self.requests[seqnum]
                        req.check =True
                        req.cliresult = cliresult
                        req.result = msg.payload
                        req.reset()
                        self.logger_debug(f'notify event set ...')
                    else:
                        self.logger_debug(f'notify event set fail...')
                    return
                elif tp==2:
                    if self.on_unhandlehci:
                        self.on_unhandlehci(msg)
                    return
                if self.on_unhandlecli:
                    self.on_unhandlecli(msg)
                self.logger_warning(f'mismatch cli response:moduleid={moduleid}, msgid={msgid},seqnum={seqnum},type={tp}')
            else:
                self.logger_warning(f'receive cli response error:{msg.payload.hex()},hc={msg.header_check},cc={msg.content_check}')

        elif msgtype == 4:
            if self.logging_only:
                return
            ack = Ack()
            ack.seq = msg.seqnum
            ack.tid = msg.tid
            ack.status = 1
            if not msg.header_check:
                return
            if msg.content_check:
                ack.status = 0
                self.sortdumpdata(msg,self.isdump_audio)
            wdata = ack.getbytes()
            if self.decode.ack and msg.ack and self.port.is_open and not self.isstop:
                self.write(wdata)
            if ack.status == 1:
                self.logger_debug('ack audio dump={0}'.format(wdata.hex()))

        elif msgtype == 1 or msgtype == 2 or msgtype == 5:
            if msg.timespan < 0.5*32768:  # 重启过开启检测
                self.ischeckmiss = True
            if msgtype == 5:  # 出现异常 不检测
                self.ischeckmiss = False
            if msg.header_check:
                if msg.content_check:
                    if self.ischeckmiss:
                        self.checkmisslog(msg)
                    self.onmessage(msg)
                    return
            self.logger_debug('stream or raw log error :{0}'.format(msg.getbytes().hex()))

        elif msgtype == 0x10:
            if 'WuQi - Second Bootloader' in msg.get_string():
                self.logDictionary.clear()
            if not self.isdump:
                self.onmessage(msg)
        elif msgtype== 6:#hci log
            #print(msg.payload.hex())
            if self.writesnoop:
                self.btsnoop.addRecord(msg.payload)
        else:
            error = 'other msgtype error:{0},msgtype={1},payload={2}'.format(msg,msgtype,msg.payload.hex())
            self.onmessage(StringLog(error))
            self.logger_debug(error)

    def start(self, onmessage: callable,cfafile:str=''):
        self.isstop = False
        self.onmessage = onmessage
        if self.writesnoop:
            if not cfafile:
                cfafile=os.path.join(self.logger_bin_file_dir, '{0}-{1}.cfa'.format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),self.__port.split('/')[-1]))
            self.btsnoop.createHeader(cfafile)
        self.open()
        self.task = threading.Thread(target=self.receive, daemon=True)  # daemon = True退出进程，子线程自动退出
        self.task.start()
        self.ht = threading.Thread(target=self.handleth, daemon=True)  # daemon = True退出进程，子线程自动退出
        self.ht.start()
    def handleth(self):
        while not self.isstop:
            try:
                rdata = self.buffstream.read()
                if len(rdata) >0:
                    #print(f'rdata={rdata.hex()}')
                    self.decode.get_result(rdata, self.handle)
                    continue
                time.sleep(0.001)
            except BaseException as ex:
                print(ex)
                if self.on_exception:
                    self.on_exception(ex)
                time.sleep(0.001)
    def stop(self):
        self.btsnoop.close()
        self.isstop = True
        self.close()

    def write(self, data):
        self.lock.acquire()
        self.port.write(data)
        self.lock.release()

    def getnextid(self):
        seqid = self.seqnum
        self.seqnum += 1
        if self.seqnum > 0xFFFF:
            self.seqnum = 0
        return seqid
    def doRequest(self,
                   reqcmd: CommandBase,
                   timeout: float = 5.0,
                   maxResendCnt: int = 1,
                   resmsgid: int = -1) -> Response:
        return self.doRequsest(reqcmd,timeout,maxResendCnt,resmsgid)
    def doRequsest(self,
                   reqcmd: CommandBase,
                   timeout: float = 5.0,
                   maxResendCnt: int = 1,
                   resmsgid: int = -1) -> Response:
        # self.isdump = False
        # self.isdump = isinstance(reqcmd, AncDumpStartRequest)
        # self.logger_debug('IsAncDumpStartRequest={0}'.format(self.isdump))
        res = Response()
        retry = 0
        if maxResendCnt <= 0:
            maxResendCnt = 1
        reqcmd.seqnum = self.getnextid() #重传不自增
        while retry < maxResendCnt:
            #self.logger_debug(f'module id:{reqcmd.moduleid}, msg id:{reqcmd.msgid}, retry time:{retry},seqnum={reqcmd.seqnum}')
            req = Request(reqcmd, resmsgid)
            data = self.decode.getbytes(reqcmd.seqnum, reqcmd)  # reqcmd.getbytes()
            self.requests[reqcmd.seqnum] = req
            self.logger_debug(f'send cli request:moduleid={reqcmd.moduleid},msgid={reqcmd.msgid},seqnum={reqcmd.seqnum}({hex(reqcmd.seqnum)}),retry={retry},threadid={threading.get_ident()},data={data.hex()}')
            self.write(data)
            retry = retry + 1
             # 没有回复的请求
            if not reqcmd.hasresponse:
                res.success = True
                res.msg = 'the request suceess.'
                self.logger_debug(f'{res.msg}')
                return res
            suc = req.wait(timeout)
            res.success = suc and req.check
            res.cliresult =  req.cliresult
            if res.success and req.cliresult == 0:
                rescmd = reqcmd.getresponse()
                try:
                    rescmd.loadbytes(req.result)
                except Exception as ex:
                    self.logger_debug('exception:{0}'.format(ex))
                    self.logger_debug('error while receive module id: %d, msg id: %d' % (req.clicmd.moduleid, req.clicmd.msgid))
                    self.logger_debug('received raw data is %s' % req.result)
                    self.logger_debug('received data is %s' % rescmd.payload)
                    res.success = False
                    continue
                if not rescmd.check(req.clicmd):
                    res.success =False
                    res.msg =f'the request returned but check fail,response result={rescmd}.'
                    self.logger_critical(f'{res.msg}')
                    return res
                res.cmd=rescmd
                res.msg='the request suceess.'
                del self.requests[reqcmd.seqnum] #正确才删除
                return res
            elif req.cliresult !=-1:
                res.success =False
                res.msg =f'the request return error,result={req.cliresult}.'
                self.logger_critical(f'{res.msg}')
                return res
            else:
                res.msg = 'the request timeout.'
        return res
    def dump(self, ondump: callable):
        self.ondump = ondump
        self.packages = {}

    def sortdumpdata(self, msg: DumpData,is_dump_audio =False):
        if msg.tid not in self.packages:
            self.packages[msg.tid] = DumpDataSort()
        self.packages[msg.tid].is_audio = is_dump_audio
        self.packages[msg.tid].sortdumpdata(msg, self.ondump)

    def cleardump(self):
        self.packages.clear()

    def checkmisslog(self, msg:LogBase):
        if msg.coreid != 255:
            if msg.coreid in self.logDictionary:
                lastseq = self.logDictionary[msg.coreid]
                if msg.timespan > 0.5*32768:
                    if getPrevNumber(msg.seqid) != lastseq:
                        #ls = ','.join([str(id) for id in getRangeNumber(msg.seqid, lastseq)])
                        misslog = f'[auto] miss log type={msg.msgtype},coreid={msg.coreid},seqid range({lastseq},{msg.seqid})...'
                        self.onmessage(StringLog(misslog))
            self.logDictionary[msg.coreid] = msg.seqid


class DumpDataSort:
    def __init__(self):
        self.tid = 0xFF
        self.lastnum = -1
        self.packages = {}
        self.audiodata :bytes = b''
        self.is_audio = False
        self.audio_seqid =-1
    def cleardump(self):
        self.lastnum = -1
        self.packages.clear()
        self.audiodata = b''
    def getnextid(self,curid:int,maxid:int=0xFFFF)->int:
        if curid==maxid:
            return 0
        return curid + 1
    def cachecache(self):

        pass
    def sortdumpdata(self, msg: DumpData, ondump: callable):
        maxseqnum = 0xFFFF  # if msg.version==0 else 0xFFFF>>4
        if ondump is None:
            return
        if self.lastnum == -1:
            self.handle_dumpdata(msg,ondump)
            self.lastnum = msg.seqnum
        else:
            #print(f'other1  data ,msg.seqnum = {msg.seqnum},self.lastnum={self.lastnum}')
            nextid  = self.getnextid(self.lastnum,maxseqnum)
            if not msg.ack and isinstance(msg, AudioDumpData): #ack 不需要排序,且需要补包
                self.handle_dumpdata(msg,ondump)
                self.lastnum = msg.seqnum
                return
            if msg.seqnum ==nextid:
                self.handle_dumpdata(msg,ondump)
                self.lastnum = msg.seqnum
                while True:
                    nextid  =self.getnextid(self.lastnum,maxseqnum)
                    if nextid in self.packages:
                        self.handle_dumpdata(self.packages[nextid],ondump)
                        del self.packages[nextid]
                        self.lastnum  =nextid
                        continue
                    break
            else:
                self.packages[msg.seqnum] = msg
    def handle_dumpdata(self, msg: DumpData, ondump: callable):
        if not self.is_audio:
            ondump(msg)
            return
        # if  self.audiodata[0:4] != bytes([0x55,0xAA,0x70,0x36]) and msg.payload[0:4] != bytes([0x55,0xAA,0x70,0x36]):
        #     return
        self.audiodata += msg.payload
        index = self.audiodata.find(bytes([0x55,0xAA,0x70,0x36]))
        if index >=0 and index + len(self.audiodata)>=audio_header_len:
            adk_audio  = AudioDumpDataHeader(self.audiodata[index:audio_header_len])
            if len(self.audiodata)>=adk_audio.length +index:
                dd = AudioDumpData()
                dd.loadbytes(self.audiodata[index:adk_audio.length])
                ## 制造丢包
                # if (dd.adk_audio.seqid+1) % 88 ==0:
                #     print(f'skip audio seqid={dd.adk_audio.seqid}')
                #     self.audiodata = self.audiodata[adk_audio.length:]
                #     return
                if self.audio_seqid !=-1 and dd.adk_audio.seqid !=  self.audio_seqid + 1:
                    fillValue = 1 << (dd.adk_audio.bitwide - 1)
                    fillBytes = fillValue.to_bytes(dd.adk_audio.bitwide // 8, 'little')
                    for i in range(1,dd.adk_audio.seqid - self.audio_seqid):
                        hd = copy.deepcopy(dd.adk_audio)
                        hd.seqid = self.audio_seqid + i
                        md = AudioDumpData(hd)
                        md.payload = dd.payload[0:audio_header_len] + fillBytes * ((dd.adk_audio.length - audio_header_len) // len(fillBytes))
                        ondump(md)
                        print(f'fill data seqid={hd.seqid}')
                ondump(dd)
                self.audio_seqid = dd.adk_audio.seqid
                self.audiodata = self.audiodata[index + adk_audio.length:]
