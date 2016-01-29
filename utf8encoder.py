import sys
import os
import binascii

def getIntValue(input):
    if input != '':
        hexVal = binascii.hexlify(input)
        intVal = int(hexVal, 16)
        binaryValue = bin(intVal)
        intValue = int(binaryValue,2)
        return intValue

def read(filePath):
    content=[]
    with open(filePath, "rb") as f:
        byte=f.read(2)
        intVal = getIntValue(str(byte))
        content.append(intVal)
        while byte != "":
            byte = f.read(2)
            if str(byte) != '':
                intVal = getIntValue(str(byte))
                content.append(intVal)
        f.close()
    return content

def utf8Convertor(input):
    result=[]
    for item in input:
        if item < int('10000000', 2):
            utf8Data = bin(0b1111111 & item)[2:]
            space = '0'* (7-len(utf8Data))
            utf8Data = '0'+space+utf8Data
            result.append(utf8Data)
        elif item < int('100000000000', 2):
            utf8DataLow = bin(0b111111 & item)[2:]
            spaceLow = '0'* (6-len(utf8DataLow))
            utf8DataLow = '10' + spaceLow + utf8DataLow
            utf8DataHigh = bin(0b11111000000 & item)[2:-6]
            spaceHigh = '0'* (5-len(utf8DataHigh))
            utf8DataHigh = '110' + spaceHigh + utf8DataHigh
            utfData =  utf8DataHigh + utf8DataLow
            result.append(utfData)
        else:
            utf8DataLow = bin(0b111111 & item)[2:]
            spaceLow = '0' * (6 - len(utf8DataLow))
            utf8DataLow = '10' + spaceLow + utf8DataLow
            utf8DataMid = bin(0b111111000000 & item)[2:-6]
            spaceMid = '0' * (6 - len(utf8DataMid))
            utf8DataMid = '10' + spaceMid + utf8DataMid
            utf8DataHigh = bin(0b1111000000000000 & item)[2:-12]
            spaceHigh = '0' * (4 - len(utf8DataHigh))
            utf8DataHigh = '1110' + spaceHigh + utf8DataHigh
            utf8Data = utf8DataHigh + utf8DataMid + utf8DataLow
            result.append(utf8Data)
    return result

def divide(str, bits):
    return [str[start:start+bits] for start in range(0, len(str), bits)]

def output(data):
    with open('utf8encoder_out.txt', "wb") as result:
        for item in data:
            bytes = divide(item, 8)
            for byte in bytes:
                result.write(chr(int(byte,2)))

fileData = read(sys.argv[1])
utf8Data = utf8Convertor(fileData)
output(utf8Data)
