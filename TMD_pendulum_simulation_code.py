
import numpy as np
import matplotlib.pyplot as plt
import math

import bpy
import math

# 기존 객체 삭제
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 파라미터 설정
radius = 1.5   # 원통 반경
height = 1.5   # 원통 높이
distance = 4.0 # 삼각형 한 변 길이
tower_height = 10.0
pendulum_mass = 50
pendulum_length = 3.5

# 원통형 부유체 3개 (정삼각형 배열)
for i in range(3):
    angle = i * (2 * math.pi / 3)
    x = distance * math.cos(angle)
    y = distance * math.sin(angle)
    z = height / 2
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height, location=(x, y, z))
    bpy.context.object.name = f"Buoyant_Cylinder_{i+1}"

# 중앙 타워 생성
tower_z = height + tower_height / 2
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=tower_height, location=(0, 0, tower_z))
bpy.context.object.name = "Central_Tower"

# 진자 추가 (구형 질량체)
pendulum_z = tower_z - pendulum_length
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(0, 0, pendulum_z))
bpy.context.object.name = "TMD_Pendulum"

# 진자 줄 시각화 (실선 대신 얇은 원통)
bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=pendulum_length,
                                    location=(0, 0, tower_z - pendulum_length / 2))
bpy.context.object.name = "Pendulum_Rod"

print("✅ 통합 구조 생성 완료: 삼각형 원통 + 중앙 타워 + 진자")


# 기본 상수
g = 9.81  # 중력가속도
theta0 = math.radians(15)  # 초기 각도 (15도)
duration = 10  # 시뮬레이션 시간 (초)
fps = 25  # 초당 프레임 수
n_frames = duration * fps
t = np.linspace(0, duration, n_frames)

# 시뮬레이션 변수 예시 (질량, 길이, 감쇠비)
masses = [50, 100, 150, 200, 250, 300]
lengths = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
positions = ['very top', 'top', 'upper middle', 'lower middle', 'bottom', 'very bottom']
offsets = [3.5, 3.0, 2.25, 0.75, 0.3, -0.2]

# 감쇠 시뮬레이션 함수
def simulate_damped_pendulum(mass, length, zeta, offset=0):
    omega_n = math.sqrt(g / length)
    omega_d = omega_n * math.sqrt(1 - zeta**2)
    theta_t = theta0 * np.exp(-zeta * omega_n * t) * np.cos(omega_d * t)
    z_t = -length * np.cos(theta_t) + offset
    return z_t

# 그래프 예시: 질량에 따라 감쇠 궤적 비교 (감쇠비 질량에 따라 조정)
colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown']
plt.figure(figsize=(10, 6))
for i, m in enumerate(masses):
    zeta = 0.2 / math.sqrt(m)  # 질량이 클수록 감쇠비 낮음
    z = simulate_damped_pendulum(mass=m, length=3.0, zeta=zeta)
    plt.plot(t, z, label=f"mass = {m} kg", color=colors[i])
plt.xlabel("Time (s)")
plt.ylabel("Z Position (m)")
plt.title("Damped Pendulum Trajectories by Mass")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("pendulum_mass_variable_damping.png", dpi=300)
plt.close()

# 그래프 예시: 길이에 따라 감쇠 궤적 비교
plt.figure(figsize=(10, 6))
for i, L in enumerate(lengths):
    z = simulate_damped_pendulum(mass=200, length=L, zeta=0.05)
    plt.plot(t, z, label=f"length = {L} m", color=colors[i])
plt.xlabel("Time (s)")
plt.ylabel("Z Position (m)")
plt.title("Damped Pendulum Trajectories by Length")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("pendulum_length_variation.png", dpi=300)
plt.close()

# 그래프 예시: 위치에 따라 감쇠 궤적 비교
plt.figure(figsize=(10, 6))
for i in range(6):
    z = simulate_damped_pendulum(mass=200, length=3.0, zeta=0.05, offset=offsets[i])
    plt.plot(t, z, label=positions[i], color=colors[i])
plt.xlabel("Time (s)")
plt.ylabel("Z Position (m)")
plt.title("Damped Pendulum Trajectories by Mounting Position")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("pendulum_position_6variation.png", dpi=300)
plt.close()
