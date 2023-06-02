import Jetson.GPIO as GPIO
import time

# PWM 값의 최소, 최대값 설정
MIN_PWM = 1050
MAX_PWM = 1950

# 채널 개수 설정
NUM_CHANNELS = 8

# GPIO 핀 번호 설정
PPM_PIN = 18

# PPM 신호 생성 함수
def generate_ppm(pwm_values):
    # PPM 프레임 시작 펄스
    ppm_frame_start = 300

    # 채널 펄스 시간 계산
    ppm_channel_time = (22500 - ppm_frame_start) // NUM_CHANNELS

    # PPM 프레임 생성
    ppm_frame = [ppm_frame_start]

    for pwm_value in pwm_values:
        # 채널 값 범위 조정
        pwm_value = max(MIN_PWM, min(pwm_value, MAX_PWM))
        
        # 채널 펄스 길이 계산
        channel_pulse = (pwm_value - 1000) // 2

        # PPM 프레임에 채널 펄스 추가
        ppm_frame.append(channel_pulse)

    # PPM 프레임의 마지막에 추가 펄스 추가
    ppm_frame.append(0)

    # PPM 프레임 시간 계산
    ppm_frame_time = sum(ppm_frame) * 0.000001

    # PPM 신호 생성
    ppm_signal = []

    for _ in range(NUM_CHANNELS + 2):
        ppm_signal.append(GPIO.HIGH)

    ppm_signal.append(GPIO.LOW)

    for i in range(len(ppm_frame) - 1):
        for j in range(ppm_frame[i]):
            ppm_signal.append(GPIO.LOW)

        ppm_signal.append(GPIO.HIGH)

    for i in range(int((22500 - sum(ppm_frame)) / 2)):
        ppm_signal.append(GPIO.LOW)

    ppm_signal.append(GPIO.HIGH)

    # PPM 신호 전송
    GPIO.output(PPM_PIN, GPIO.LOW)

    for i in range(NUM_CHANNELS + 3):
        GPIO.output(PPM_PIN, ppm_signal[i])
        time.sleep(ppm_frame_time)

    GPIO.output(PPM_PIN, GPIO.LOW)

# 테스트용 PWM 값 설정
test_pwm = [1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800]

# GPIO 핀 모드 설정
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PPM_PIN, GPIO.OUT)

while True:
    # PPM 신호 생성
    generate_ppm(test_pwm)

    # 1초 대기
    time.sleep(1)
