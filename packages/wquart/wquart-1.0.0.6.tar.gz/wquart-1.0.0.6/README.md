# 1.wquart 使用卸载说明
安装和更新（会先卸载再安装）
``` shell
    pip install wquart
```
 
# 2.demo 运行
``` shell
python demo.py COM92 2000000 tws-basic-7035AX-B-1.3.3.1.wpk

``` 
demo 
# 3 开发说明

## 3.1 log 解析
``` python
uart = WqUart(port,baudrate)
uart.writebin = False  #是否记录串口原始数据，可以排查解析错误，一般不开启
uart.load(wpk)  # 加载日志解析固件
uart.start(onmessage) #传入日志解析回调函数
uart.isdump_audio = True 
uart.ondump=ondump # audio dump 回调函数
```
### 3.1.1  uart.load(wpk) 
可择时调用，用于ota升级部分image场景，重新加载对应的wpk固件
### 3.1.2 onmessage
本库已解析好的日志回调，分2类类型
* msgtype = 1,2,5 : image的log
* msgtype = 0x10 : sbl的log 或者根据的提示log(丢log检测,audio dump 丢包时补包提示)
## 3.2 audio dump 
必须设置 isdump_audio = True  
## 3.2.1 开启AudioDump
发送如下cli开启
``` python 

    req = cli.AudioDumpStartRequest(0,2,False,[cli.DCorePoint(0x10,4,0)])
```
AudioDumpStartRequest 参数和UI工具是一致的，简单说明如下
* dumpway  dump方式，支持uart usb spp storage i2c
* core  coreid  ,0:a core 1 :dcore
* ack  是否需要回复 默认传Flase
* points 需要dump的点，是一个数组，可传一个核（a core 和 d core 二选一）多个点，不能混合核的多个点
dump 点根据固件需要动态改变，d core点支持cli实时查询 cli.SyncDCoreStreamRequest

## 3.2.2 停止audio dump 
``` python 
    req = cli.AudioDumpStopRequest()
    res = uart.doRequest(req,1,10)
    if res.success:
        print(f'AudioDumpStopRequest success')
```
## 3.2.3 ondump 回调说明

``` python
uart.ondump=ondump

writer = WriterManager()
def ondump(data:AudioDumpData):
    #print(f'{data}')
    writer.write(data)
```
* data为 AudioDumpData 类型的回调对象，里面包含一个24字节的头和payload
* WriterManager 负责写入wav ，同一个dump point为一个文件，多个channel合成多轨的wav,想控制生成的文件名，则重写WriterManager的get_filename方法
## 3.3 cli 
本库已封装好cli的交互，派生类必须是CommandBase的子类，通过doRequest函数同步请求
``` python
   req = GetFWVersionRequest()
   res = uart.doRequest(req,timeout = 0.1,maxResendCnt=10)
   if res.success:
    print(f'GetFWVersionRequest success, {res.cmd}')

```
输出
``` shell
    GetFWVersionRequest success, FW-VERSION-v1.0.0.0---2025-04-27 08:31:26-Debug
```
用户可参照 wquart/extendcli.py 自行扩展cli ,文件可放置任意位置，只需实现CommandBase基类的对应方法

``` python
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
```
CommandBase 基类方法解释
默认约定下，请求和响应需同名并分别以 Request 和 Response结尾，如不遵守，需实现get_instanceName方法指定响应类的类名

## 3.3.1 XXXRequest
* self.moduleid 模块id
* self.msgid 消息id
* getpayload() 请求参数
## 3.3.2 XXXResponse
* loadbytes 解析回复的payload
## 3.3.3 扩展
* get_moduleName 必须重写此方法，不然找不到模块，一般照抄即可