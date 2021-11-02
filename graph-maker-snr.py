#아래는 기본 모듈
import math
import ReadEngine
from datetime import datetime
import matplotlib as mpl
#mpl.rcParams['agg.path.chunksize'] = 10000
import matplotlib.pyplot as plt

per_list_dir = "./snr-per/"
per_list = ["1-400"] #mcs-bytes
per_diction = {}

def load_per_table():
    global per_diction
    global per_list
    global per_list_dir

    for file_name in per_list:
        file_dir = per_list_dir + file_name + ".txt"
        per_diction = ReadEngine.Read_To_Diction(file_dir)

load_per_table()

X = per_diction.keys() #SNR
X_float = [float(i) for i in X]
Y = per_diction.values() #PER
Y_float = [float(i) for i in Y]

print(X)
print(Y)

plt.plot(X_float, Y_float, linestyle = "solid", color = "black")
plt.title("SNR-PER")
plt.xlabel("SNR (dB)")
plt.ylabel("PER")
plt.legend()
plt.axis([0, 35, 0, 1])
plt.grid()
#plt.show()
plt.savefig('./graph/snr-per.png', dpi=300)

