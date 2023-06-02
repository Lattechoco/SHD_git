import random
import time
import matplotlib.pyplot as plt

class PID:
    def __init__(self, kp, ki, kd):
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd
        self.last_error = 0
        self.integral = 0

    def calculate(self, setpoint, pv):
        error = setpoint - pv
        self.integral += error
        derivative = error - self.last_error
        output = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)
        self.last_error = error
        return output
        

# PID 제어기 초기화
pid = PID(kp=1, ki=0.1, kd=0.05)

# 그래프 초기화
plt.ion()
fig, ax = plt.subplots()
plt.title("PID Control")
plt.xlabel("Time")
plt.ylabel("Value")
line1, = ax.plot([], [], 'r-', label='Setpoint')
line2, = ax.plot([], [], 'b-', label='Process Value')
line3, = ax.plot([], [], 'y-', label='output Value')
ax.legend()

# 초기값 설정
t = []
sp = []
op = []
pv_list = []

setpoint = float(input("Setpoint : "))%360
pv = float(input("Present_Valus : "))%360

# PID 제어 알고리즘을 실행
start_time = time.time()
while True:
    # 목표값 초기화 (랜덤 값 추가)
    if random.random() < 0.1:  # 10% 확률로 setpoint 변경
        setpoint = random.uniform(-100, 100)

    if random.random() < 0.1: # 20% 확률로 값 변경
        pv += random.uniform(-100, 100)

    # PID 제어 알고리즘 적용
    output = pid.calculate(setpoint, pv)
    print("output : ", output)
    pv += output

    # 현재값(pv)과 목표값(setpoint) 저장
    t.append(time.time() - start_time)
    sp.append(setpoint)
    op.append(output)
    pv_list.append(pv)

    # 그래프 업데이트
    line1.set_data(t, sp)
    line2.set_data(t, pv_list)
    line3.set_data(t, op)
    ax.relim()
    ax.autoscale_view(True, True, True)
    fig.canvas.draw()
    fig.canvas.flush_events()

# 그래프 표시
plt.show()