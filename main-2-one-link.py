#아래는 기본 모듈 
import math
import sys
from datetime import datetime

#아래는 시뮬레이터 자체 모듈.
#PATHLOSS 모델을 바꿀 때에는, 아래의 세 파라미터를 모두 바꿀 것!
from pathloss import fspl, ldpl, ldpl_t, tcpl
pathloss = ldpl_t
pathloss_marker = "ldpl_t"
load_snr = False
save_snr = False

from distance import calcdistance
import txframe
import backoff
import ReadEngine

aSlotTime = 9
aSIFSTime = 16
aDIFSTime = aSIFSTime + (2 * aSlotTime)

frame_log = []#FER을 계산하기 위한 리스트. 매 프레임 전송이 완료된 후, 전송 성공 또는 실패를 0과 1로 저장한다. FER = sum(frame_log)/len(frame_log)
delay_log = []#매 시뮬레이션이 종료된 후 소요된 딜레이를 저장한다.
frame_list = [{"authentication request":400, "ack":14}, {"authentication response":400, "ack":14}, {"association request":400, "ack":14}, {"association response":400, "ack":14}]#보낼 프레임 목록. 프레임 이름, 프레임 길이(바이트 단위)를 딕셔너리로 저장. 각 딕셔너리 간에는 백오프 과정 수행. e.g. [{"ProbeReq":100, "Ack": 50}, {"ProbeResp": 100, "Ack": 50}]
num_frame_group = len(frame_list)

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
epoch = 10000
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
min_pathloss = fspl(ap_height, f)
noise_power = txpower - min_pathloss - target_snr

#rx antrnna gain , dBi 단위
rx_antenna_gain = 0

#MCS 인덱스 -> Duration 계산에 사용
MCS = 2
#나머지 채널 파라미터들은 txframe에서 수정해야함.
#GI, SYMBOLTIME, STREAM, SUBCARRIERS 등
#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#<시뮬레이션 파라미터>
#스텝: 총 타임스텝의 수. - 정수형으로 변환. / distance_per_step: 한 타임스텝당 거리.

steps = int((length / train_speed)/timestep)
print(steps)
distance_per_step = train_speed * timestep

#핸드오버 지점. 스텝 단위로 표시.
handover_point = 0 #최대한 이른 시점에서 핸드오버 시작

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

#!!!!!수동 입력 필요!!!!!
txframe.ap_snr = ap2_snr #이 시뮬레이션은 AP2를 위한 시뮬레이션이므로.
#---------------------------------------------------------------------------------

def convert_to_step(time): #마이크로세컨드 단위 시간을 받아 스텝으로 변환
    in_step = math.ceil(time / timestep_mantissa)
    return in_step

def calc_ho_delay():
    #열차가 진행중, 핸드오버 포인트를 만나면 이벤트 발생! - 이벤트 시작 시, 기존 AP와 연결이 끊어진 것으로 간주. 타임스탬프 기록
    #핸드오버 이벤트 발생 시, 다음 AP에 프레임 교환 절차 수행. 각 타임스탬프별로 노이즈가 바뀌며, 그 과정에서 프레임 에러 발생 시 오류로 간주. 재전송 시도.
    #다음 AP에 Association했다면, 타임스탬프 기록. Delay가 산출됨.
    #스텝이 끝날 때까지 Association 실패 시, Fail로 기록.
    initial_step = handover_point

    for ep in range(epoch):
        #print("시뮬레이션 {}회 시작".format(ep+1))
        printProgress(ep+1, epoch, 'Progress:', 'Complete', 1, 50)
        step = initial_step
        failed = False

        progress = 1 #Progress가 num_frame_group과 같지 않거 전송 종료 시 실패.
        for frame_group in frame_list: #프레임 그룹 = 시퀀스에 백오프가 필요한 프레임들.
            rtrycount = 0

            while(1): #프레임 그룹의 프레임 전송
                #print("현재 재전송 카운트: ", rtrycount)
                isrtry = False
                step += convert_to_step(backoff.backoff(rtrycount))

                for frame in frame_group:
                    #print(frame, "전송중", "    프레임 길이: ", frame_group[frame],"  현재 스텝: ", step, "/", steps)
                    if step >= steps: #시뮬레이션 시간을 초과할 경우
                        failed = True
                        print("프레임 시퀀스 실패")
                        break

                    #result, time, per = txframe.txframe(frame_group[frame], MCS, ap2_snr[step])
                    result, tx_step, per = txframe.txframe(frame_group[frame], MCS, step)
                    #print("PER: ", per, "SNR: ", ap2_snr[step])
                    step += tx_step

                    #프레임 전송에 성공시 프레임 그룹 내의 다음 프레임 전송
                    if result == False: # 프레임 전송에 실패하면
                        #print("프레임 전송 실패. 재전송")
                        rtrycount +=1 #재전송 카운트 증가
                        isrtry = True #재전송 플래그 설정
                        break


                if failed == True:
                    #print("프레임 시퀀스 실패, while을 빠져나옴.")
                    break
                elif isrtry == False: #루프에서 빠져나왔을 때, 재전송이 아니라면
                    break
            
            if failed:
                break
            else:
                progress += 1
    
        if failed:
            frame_log.append(9)
            delay_log.append(step)
            #print("핸드오버 시점은", step, "스텝 입니다.")
            #print("프레임 시퀀스 실패")
        else:
            frame_log.append(3)
            delay_log.append(step)
            #print("핸드오버 시점은", step, "스텝 입니다.")
            #print("프레임 시퀀스 성공")


    #print(frame_log)
    print(delay_log)
    filename = "./save/"+"SC2-HO_"+pathloss_marker+datetime.today().strftime("%d_%H_%M") + ".txt"
    ReadEngine.Write_List_To_Text(filename, frame_log, delay_log)

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

if save_snr == True:
    ap1_snr_name = "ap1_"+pathloss_marker+"_snr.txt"
    ap2_snr_name = "ap2_"+pathloss_marker+"_snr.txt"
    f1 = open(ap1_snr_name, "w")
    for i in range(steps):
        f1.write(str(ap1_snr[i])+"\n")
    f1.close()

    f2 = open(ap2_snr_name, "w")
    for i in range(steps):
        f2.write(str(ap2_snr[i])+"\n")
    f2.close()

calc_ho_delay()
