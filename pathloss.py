import math
import numpy as np

def gaussian(sigma):
    return np.random.normal(0, sigma)

#d와 f는 각각 킬로미터와 메가헤르츠 단위임. 또는 미터와 기가헤르츠 단위로 표현할 수 있음.
def fspl(d, f):
    #dkm = d/1000
    #fmhz = f*1000
    #ploss= 32.4 + 20 * math.log10(dkm) + 20 * math.log10(fmhz)
    ploss= 32.44 + 20 * math.log10(d) + 20 * math.log10(f)
    return ploss

def ldpl(d, f):
    n1 = 1.61
    dref = 1
    sigma1 = 5.02
    x1 = gaussian(sigma1)
    ploss = fspl(dref, f) + (10 * n1 * math.log10(d/dref)) + x1
    return ploss

def ldpl_t(d, f):
    n1 = 1.93
    dref = 1
    sigma1 = 9.81
    x1 = gaussian(sigma1)
    ploss = fspl(dref, f) + 10 * n1 * math.log10(d/dref) + x1
    return ploss


def tcpl(d, f): #터널-커브 경로손실
#Two-Slope Path Loss Model for Curved-Tunnel Environment With Concept of Break Point
#S. K. Kalyankar, Y. H. Lee and Y. S. Meng, "Two-Slope Path Loss Model for Curved-Tunnel Environment With Concept of Break Point," in IEEE Transactions on Intelligent Transportation Systems, doi: 10.1109/TITS.2020.3012724.
#r300 / w * h 8.4, 6.87

    n1 = 0.82
    n2 = 3.88
    dbp = 96
    dref = 1
    sigma1 = 5.64
    sigma2 = 6.35
    if d <= dbp:
        x1 = gaussian(sigma1)
        ploss = fspl(dref, f) + 10 * n1 * math.log10(d/dref) + x1
    else:
        x2 = gaussian(sigma2)
        ploss = fspl(dbp, f) + 10 * n2 * math.log10(d/dref) + x2

    return ploss

