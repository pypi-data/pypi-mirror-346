from enum import IntEnum
from typing import Dict
import wave
from .utility import curent_time
from .decode import AudioDumpData

class AudioFormat(IntEnum):
    INVALID = 0
    PCM = 1
    SBC = 2
    AAC = 3
    LDAC = 4
    LHAC = 5
    LC3 = 6
    MSBC = 7
    CVSD = 8
    OPUS = 9
class Writer:
    def write(self,bytes):
        pass
    def close(self):
        pass
class RawWriter(Writer):
    def __init__(self,filename:str):
        super().__init__()
        self.file = open(filename, 'wb')
    def write(self, data:bytes):
        if self.file:
            self.file.write(data)
    def close(self):
        if self.file:
            self.file.close()
class WavWriter(Writer):
    def __init__(self,ww:wave.Wave_write):
        super().__init__()
        self.writer:wave.Wave_write = ww
    def write(self, data:bytes):
        if self.writer:
            self.writer.writeframes(data)
    def close(self):
        if self.writer:
            self.writer.close()
class WriterManager:
    def __init__(self):
        self.writer:Dict[int,Writer] = {}
    def write(self,data:AudioDumpData):
        raw_data  = data.getpayload()
        if data.adk_audio.point_map not in self.writer:
            filename = self.get_filename(data)
            if data.adk_audio.format == AudioFormat.PCM:
                of = wave.open(filename, 'wb')
                of.setnchannels(data.adk_audio.channels)
                of.setsampwidth(data.adk_audio.bitwide // 8)
                of.setframerate(data.adk_audio.samplerate)
                self.writer[data.adk_audio.point_map] = WavWriter(of)
            else:
                self.writer[data.adk_audio.point_map] = RawWriter(filename)
            print(f'create  file {filename}')
        if data.adk_audio.format == AudioFormat.PCM:
            raw_data = convert_to_pcm(data)
        self.writer[data.adk_audio.point_map].write(raw_data)
    def get_filename(self,data:AudioDumpData)->str:
        ext = '.dat' # 根据data.adk_audio.format类型选择扩展名,这里只处理wav格式做演示
        if data.adk_audio.format == AudioFormat.PCM:
            ext = '.wav'
        ts = curent_time('%Y-%m-%d-%H-%M-%S-%f')
        filename = f'{ts}-{hex(data.adk_audio.point_map)}{ext}'
        return filename
    def close(self):
        for k,v in self.writer.items():
            if v:
                v.close()
        self.writer = {}
def convert_to_pcm(data:AudioDumpData)->bytes: 
    """
    多channelpcm数据重组
    """
    pl = data.getpayload()
    len = data.adk_audio.bitwide // 8
    datalen = data.adk_audio.length - 24 # 24字节头
    fileData = bytearray(datalen)
    for i in range(data.adk_audio.channels):
        for index in range(0, datalen // data.adk_audio.channels, len):
            fileData[index * data.adk_audio.channels + i * len:index * data.adk_audio.channels + (i + 1) * len] = pl[index:index + len]
    return bytes(fileData)
    