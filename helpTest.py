def to2Int(x):
    # argument: int (>=0, <65536)
    # return upper int and lower int
    if (x < 0 or x >= 16**4):
        print("error: cannot convert " + str(x) + " into 2 bytes")
        return
    
    return [x//(16**2), x%(16**2)]

def calcCRC(command):
    # calculate last 2 bytes of command (= CRC-16 error check)
    # argument is command without error check (type: bytes)
    res = 0xFFFF

    for byte in command:
        res ^= byte
        cnt = 0
        while(cnt < 8):
            if (res&1):
                res >>= 1
                cnt += 1
                res ^= 0xA001
            else:
                res >>= 1
                cnt += 1

    res = to2Int(res)
    # upper byte <-> lower byte
    res.reverse()
    res = bytes(res)

    return command + res

def genCommand(slaveAddress, functionCode, dataStart, dataNum, data):
    # generate command
    
    # array of int
    res = []
    res += [slaveAddress]
    res += [functionCode]

    # dataStart, dataNum: 2 byte
    res += to2Int(dataStart)
    res += to2Int(dataNum)

    # e in data: 2 byte
    for e in data:
        res += to2Int(e)

    res = bytes(res)
    res = calcCRC(res)

    return res

"""
def toBytes(byte):
    # if byte in [9, 10, 13, 32, 33, ..., 125, 126], error
    
    # <int> 97 = <bytes> b"a"
    pass

for i in range(256):
    #print(i, format(i, "x"), hex(i), "%02x" % i)
    #全部str
    #print(type(format(i, "x")), type(hex(i)), type("%02x" % i))
    #print(bytes(hex(i)))
    s = "\\x" + ("%02x" % i)
    print(s, type(s))
    t = s.encode()
    print(t, type(t))
"""

"""
# 見た目がエンコードされてるだけで実は動くのでは？？？
command = b"\x01\x03\x00\x7f\x13\x03"
command = calcCRC(command)
print(command)
for byte in command:
    print(byte)
"""

"""
# parameters
slaveAddress = 1
functionCode = 3
dataStart = 127
dataNum = 1
data = [8500]
command = genCommand(slaveAddress, functionCode, dataStart, dataNum, data)
print(command)
"""
"""
for byte in command:
    print(byte, "%02x" % byte)
"""

def moveRelative(slaveAddress, dist):
    data = [dist]
    command = genCommand(slaveAddress, 10, 0, 2, data)
    # cliant.write(command)
    print(command)

def moveToHome(slaveAddress):
    data = []
    command = genCommand(slaveAddress, 0, 0, 0, data)
    # cliant.write(command)
    print(command)

slaveAddress = 1
dist = 8500
moveToHome(slaveAddress)
moveRelative(slaveAddress, dist)