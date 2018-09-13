# -*- coding:utf-8 -*-

from PIL import Image
import binascii

def get2lsb(n):
    """ Return 2 last LSB as String """
    n = n%4
    if(n == 0):
        return "00"
    if(n == 1):
        return "01"
    if(n == 2):
        return "10"
    if(n == 3):
        return "11"

def decode(i):
    """ Long int to String (thanks to #ENOENT) """
    if len(i) > 0:
        n = int(i, 2)
        n = hex(n)[2:][:-1]
        if len(n) % 2 != 0:
            n = "0"+n
        return n.decode("hex")
    return ""

###############################################################################

img = Image.open("PITorMiss.png")

w,h = img.size

IC = 0  # set Indicator channel
c1 = 1  # set Channel
c2 = 2  # set Channel

# RMS = Remaining Size (data embedded)
RMS = 8*1207  # Set remaining data (first was ~ 100 then I updated to get the full flag)

# pxsl = 1D list of pixels
pxsl = list(img.getdata())[w:]  # [w:] => Starting parsing at line 2

flag = ""  # Flag (bits)

i = 0  # Current px
while(RMS > 0):  # WHile there is still px to parse
    indicLSB = pxsl[i][IC]%4 # Get IC Informations
    if(indicLSB == 1):  # if IC == 01
        flag += get2lsb(pxsl[i][c1])  # Note that we used C1 instead of C2 (see diff' n° 2)
        RMS -= 2
    elif(indicLSB == 2):  # if IC ==  10
        flag += get2lsb(pxsl[i][c2])  # Note that we used C2 instead of C1 (see diff' n° 2)
        RMS -= 2
    elif(indicLSB == 3):  # if IC == 11
        flag += get2lsb(pxsl[i][c1])
        flag += get2lsb(pxsl[i][c2])
        RMS -= 4
    i += 1

### Decode flag

print(decode(flag))