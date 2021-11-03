#아래는 기본 모듈
import math
from datetime import datetime
import matplotlib.pyplot as plt

#아래는 시뮬레이터 자체 모듈.
from pathloss import fspl
pathloss = fspl
pathloss_marker = "fspl"
load_snr = False
from distance import calcdistance

#---------------------------------------------------------------------------------
#<물리적 위치 및 시간 설정 - 타임스탭, 열차 이동 속도, AP 간격 및 위치, 핸드오버 지점>
#타임스텝 - 초 단위로 입력.
#타임스텝은 시뮬레이션 시간의 기초 단위.
timestep_mantissa = 1 #타임스텝 배수
timestep = timestep_mantissa * math.pow(10, -6) #마이크로세컨드 단위.
#열차속도 - m/s 단위로 입력
train_speed = 22.22 #22.2222 m/s = 80 km/h
#AP 관련 파라미터 - m 단위로 입력
#AP 높이는 AP의 높이에서 열차 지붕의 높이를 뺀 값으로 정함.
ap_height = 2
#AP 간격은 2개의 AP가 설치된 간격을 나타냄. AP의 간격은 총 시뮬레이션의 거리를 정하게 됨.
#총 시뮬레이션 거리 = AP간격*2. 2개의 AP는 총 시뮬레이션 거리 중앙에 입력한 간격만큼 위치.
#아래 참고도 확인. *은 AP임. -------는 입력한 AP 간격임.
# 참고도: *-------*------- 
ap_distance = 40
length = ap_distance * 2
#반복 횟수
#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#<무선랜 채널 및 전송 설정 - 주파수, 노이즈 등 설정.>
#채널은 AWGN 채널로 가정.
#f: 주파수. GHz 단위로 입력.
f = 5.25
#txpower: 전송 전력. dBm 단위로 입력. 200mW = 23dBm
#:mW, dBm 계산: http://www.rfdh.com/rfdb/dbmw.htm
txpower = 23

#목표 "최대"SNR: dB 단위
target_snr = 30

#noise_power를 계산하기 위해서는, 다음이 필요->최저 pathloss / noise_power의 단위는 dBm 단위
#이 noise power는 antenna gain을 고려하지 않음
min_pathloss = pathloss(ap_height, f)
noise_power = txpower - min_pathloss - target_snr

#rx antrnna gain , dBi 단위
rx_antenna_gain = 0

#MCS 인덱스 -> Duration 계산에 사용
MCS = 1
#나머지 채널 파라미터들은 txframe에서 수정해야함.
#GI, SYMBOLTIME, STREAM, SUBCARRIERS 등
#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#<시뮬레이션 파라미터 - 수동 입력 필요 없음.>
#스텝: 총 타임스텝의 수. - 정수형으로 변환. / distance_per_step: 한 타임스텝당 거리.

steps = int((length / train_speed)/timestep)
print(steps)
distance_per_step = train_speed * timestep

#핸드오버 지점. 스텝 단위로 표시.
handover_point = int(steps / 3)

#2개의 AP 포인트
ap1_point = (ap_distance * 0, ap_height)
ap2_point = (ap_distance * 1, ap_height)

#열차 좌표 리스트 -> 리스트 내에 튜플이 들어있는 형태.
train_point = [(x * distance_per_step, 0) for x in range(steps)]
train_point_x = [x * distance_per_step for x in range(steps)]

#AP1, AP2와 열차와의 거리 리스트.
ap1_distance = [calcdistance(ap1_point, train_point[i]) for i in range(steps)]
ap2_distance = [calcdistance(ap2_point, train_point[i]) for i in range(steps)]

if load_snr == False:
    #각 스텝당 pathloss 계산
    ap1_pathloss = [pathloss(ap1_distance[i], f) for i in range(steps)]
    ap2_pathloss = [pathloss(ap2_distance[i], f) for i in range(steps)]

    #txpower에서 pathloss 및 노이즈 전력을 뺌. 이것이 SNR임.
    ap1_snr = []
    ap2_snr = []

    for i in range(steps):
        ap1_snr.append(txpower - ap1_pathloss[i] + rx_antenna_gain - noise_power)
        ap2_snr.append(txpower - ap2_pathloss[i] + rx_antenna_gain - noise_power)

    print("시뮬레이션 파라미터 계산 완료.")

else:
    ap1_snr_name = "ap1_"+pathloss_marker+"_snr.txt"
    ap2_snr_name = "ap2_"+pathloss_marker+"_snr.txt"
    f1 = open(ap1_snr_name, "r")
    snr1 = f1.read()
    snr1 = snr1.split("\n")
    snr1.pop()
    ap1_snr = [float(i) for i in snr1]
    f1.close()

    f2 = open(ap2_snr_name, "r")
    snr2 = f2.read()
    snr2 = snr2.split("\n")
    snr2.pop()
    ap2_snr = [float(i) for i in snr2]
    f2.close()

    print("시뮬레이션 파라미터 로드 완료.")
#---------------------------------------------------------------------------------
'''
plt.plot(train_point_x, ap1_snr, label = "AP 1 SNR from train", linestyle = "solid", color = "black")
plt.plot(train_point_x, ap2_snr, label = "AP 2 SNR from train", linestyle = "dashdot", color = "black")
plt.title("SNR graph of simulation environment\nFree Space Pathloss")
plt.xlabel("Distance of train from simulation origin")
plt.ylabel("SNR (dB)")
plt.legend()
plt.axis([0, 80, 0, 35])
plt.grid()
#plt.show()
plt.savefig('./graph/fig_snr_fspl.png', dpi=300)
'''

bar_x = ["Previous system", "Proposed system"]
delay = [10175, 81.1] #기존 - 제안 순서대로
plt.figure()
plt.bar(bar_x, delay, color = ["k", "k"], width=0.2)
plt.title("Simulated average delay comparison")
#plt.xlabel("Simulated system")
plt.ylabel("Delay (µs)")

for i, v in enumerate(bar_x):
    plt.text(v, delay[i], delay[i],                 # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
             fontsize = 10, 
             color='black',
             horizontalalignment='center',  # horizontalalignment (left, center, right)
             verticalalignment='bottom')    # verticalalignment (top, center, bottom)

plt.savefig('./graph/fig_delay_fspl.png', dpi=300)

#plt.show()


def convert_to_step(time): #마이크로세컨드 단위 시간을 받아 스텝으로 변환
    in_step = math.ceil(time / timestep_mantissa)
    return in_step
