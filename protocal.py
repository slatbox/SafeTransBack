import struct
import binascii
class Proto:
    
    CMD_LOGIN=11
    CMD_CLOSE=12
    CMD_GET_FILE_LIST=13
    CMD_DOWNLOAD=14
    CMD_UPLOAD = 15
    CMD_UPLOAD_END = 16
    CMD_FILE_SUCCESS=17
    STATE_SUCCESS= 1
    STATE_FAIL = 2
    STATE_END = 3
    STATE_DOWN_START = 4
    
    def createReq(cmd,byte_info):
        return Proto.pack({'cmd':cmd},byte_info)
    
    def pack(state_cmd,byte_info):
        header = binascii.hexlify(struct.Struct('i').pack(state_cmd['cmd']))
        data = byte_info
        return header + data
    
    def unpack(byte_data):
        if len(byte_data) == 0:
            return Proto.STATE_FAIL,b''
        s = struct.Struct('I')
        size = s.size * 2
        header = s.unpack(binascii.unhexlify(byte_data[:size]))
        info = byte_data[size:] if size < len(byte_data) else b''
        return header[0],info
    
    def getCmdLen():
        return struct.Struct('I').size * 2
        



if __name__ == '__main__':
    req = Proto.createReq(30,'hello')
    header,info = Proto.unpack(req)
    print(header,info)
        
    
