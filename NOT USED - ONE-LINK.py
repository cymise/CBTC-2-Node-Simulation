#아래는 기본 모듈 (numpy 등 포함)
import math

#아래는 시뮬레이터 자체 모듈.
from pathloss import pathloss
from distance import calcdistance
import makeframe
import backoff

frame_log = []#FER을 계산하기 위한 리스트. 매 프레임 전송이 완료된 후, 전송 성공 또는 실패를 0과 1로 저장한다. FER = sum(frame_log)/len(frame_log)
delay_log = []#매 시뮬레이션이 종료된 후 소요된 딜레이를 저장한다.
frame_list = [{"probe request":400}, {"probe response":400}, {"association request":400, "ack":14}, {"association response":400, "ack":14}]#보낼 프레임 목록. 프레임 이름, 프레임 길이(바이트 단위)를 딕셔너리로 저장. 각 딕셔너리 간에는 백오프 과정 수행. e.g. [{"ProbeReq":100, "Ack": 50}, {"ProbeResp": 100, "Ack": 50}]

#---------------------------------------------------------------------------------
#<기본 설정 - 타임스탭, 열차 이동 속도, AP 간격 및 위치, 핸드오버 지점>
#타임스텝 - 초 단위로 입력.
#타임스텝은 시뮬레이션 시간의 기초 단위.
timestep = 10 * math.pow(10, -6) #1마이크로세컨드 단위.
#열차속도 - m/s 단위로 입력
train_speed = 22.22 #22.2222 m/s = 80 km/h
#AP 관련 파라미터 - m 단위로 입력
#AP 높이는 AP의 높이에서 열차 지붕의 높이를 뺀 값으로 정함.
ap_height = 2
#AP 간격은 2개의 AP가 설치된 간격을 나타냄. AP의 간격은 총 시뮬레이션의 거리를 정하게 됨.
#총 시뮬레이션 거리 = AP간격*2. 2개의 AP는 총 시뮬레이션 거리 중앙에 입력한 간격만큼 위치.
#아래 참고도 확인. *은 AP임. -------는 입력한 AP 간격임.
# 참고도: *-------*------- 
ap_distance = 75
length = ap_distance * 2
#반복 횟수
epoch = 300
#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#<무선랜 채널 설정 - 주파수, 노이즈 등 설정.>
#채널은 AWGN 채널로 가정.
#f: 주파수. GHz 단위로 입력.
f = 2.4
#txpower: 전송 전력. dBm 단위로 입력. 200mW = 23dBm
#:mW, dBm 계산: http://www.rfdh.com/rfdb/dbmw.htm
txpower = 23

#목표 "최대"SNR: dB 단위
target_snr = 35

#noise_power를 계산하기 위해서는, 다음이 필요->최저 pathloss / noise_power의 단위는 dBm 단위
#이 noise power는 antenna gain을 고려하지 않음
min_pathloss = pathloss(ap_height, f)
noise_power = txpower - min_pathloss - target_snr

#rx antrnna gain , dBi 단위
rx_antenna_gain = 0

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

#AP1, AP2와 열차와의 거리 리스트.
ap1_distance = [calcdistance(ap1_point, train_point[i]) for i in range(steps)]
ap2_distance = [calcdistance(ap2_point, train_point[i]) for i in range(steps)]

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
#---------------------------------------------------------------------------------


#def calc_ho_delay():
    #열차가 진행중, 핸드오버 포인트를 만나면 이벤트 발생! - 이벤트 시작 시, 기존 AP와 연결이 끊어진 것으로 간주. 타임스탬프 기록
    #핸드오버 이벤트 발생 시, 다음 AP에 프레임 교환 절차 수행. 각 타임스탬프별로 노이즈가 바뀌며, 그 과정에서 프레임 에러 발생 시 오류로 간주. 재전송 시도.
    #다음 AP에 Association했다면, 타임스탬프 기록. Delay가 산출됨.
    #스텝이 끝날 때까지 Association 실패 시, Fail로 기록.

#    for ep in range(epoch):
#        print("시뮬레이션 {}회째 시작".format(ep+1))
#        #awgn()
#        for i in range(steps):
#            if i == handover_point:
#                
#
#    return


f1 = open("ap1snr.txt", "w")
for i in range(steps):
    f1.write(str(ap1_snr[i])+"\n")
f1.close()

f2 = open("ap2snr.txt", "w")
for i in range(steps):
    f2.write(str(ap2_snr[i])+"\n")
f2.close()
