import math
import numpy as np

#d와 f는 각각 킬로미터와 메가헤르츠 단위임. 또는 미터와 기가헤르츠 단위로 표현할 수 있음.
def fspl(d, f):
    #dkm = d/1000
    #fmhz = f*1000
    #ploss= 32.4 + 20 * math.log10(dkm) + 20 * math.log10(fmhz)
    ploss= 32.4 + 20 * math.log10(d) + 20 * math.log10(f)
    return ploss

def tcpl(d, f): #터널-커브 경로손실
#Two-Slope Path Loss Model for Curved-Tunnel Environment With Concept of Break Point
#S. K. Kalyankar, Y. H. Lee and Y. S. Meng, "Two-Slope Path Loss Model for Curved-Tunnel Environment With Concept of Break Point," in IEEE Transactions on Intelligent Transportation Systems, doi: 10.1109/TITS.2020.3012724.
#r300 / w * h 8.4, 6.87

    n1 = 0.82
    n2 = 6.35
    dbp = 96
    dref = 10
    sigma1 = 5.64
    sigma2 = 6.35
    if d <= dbp:
        x1 = np.random.normal(0, sigma1)[0]
        ploss = fspl(dref, f) + 10 * n1 * math.log10(d/dref) + x1
    else:
        x2 = np.random.normal(0, sigma2)[0]
        ploss = fspl(dbp, f) + 10 * n2 * math.log10(d/dref) + x2

    return ploss

