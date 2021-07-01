import math

#d와 f는 각각 킬로미터와 메가헤르츠 단위임. 또는 미터와 기가헤르츠 단위로 표현할 수 있음.
def pathloss(d, f):
    dkm = d/1000
    fmhz = f*1000
    ploss= 32.4 + 20 * math.log10(dkm) + 20 * math.log10(fmhz)
    return ploss