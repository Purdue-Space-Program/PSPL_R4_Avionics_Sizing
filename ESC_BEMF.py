import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Constants
voltage_max = 24 #peaks of trapezoids
frequency = 50 #can set based off rpm, just a random one rn
time_step = 0.0001
simulation_duration = 0.1 
current_state = 0

time_points = np.arange(0, simulation_duration, time_step)
emf_a_data, emf_b_data, emf_c_data = [], [], []
commutation_states = []


commutation_table = [
    (1, 0, -1),  #A+ B-
    (1, -1, 0),  #A+ C-
    (0, -1, 1),  #B+ C-
    (-1, 0, 1),  #B+ A-
    (-1, 1, 0),  #C+ A-
    (0, 1, -1),  #C+ B-
]


#create the trapezoidal waves
def generate_back_emf(t, frequency, voltage_max):
    phase_a = voltage_max * signal.sawtooth(2 * np.pi * frequency * t, width=0.5)
    phase_b = voltage_max * signal.sawtooth(2 * np.pi * frequency * t - (2/3) * np.pi, width=0.5)
    phase_c = voltage_max * signal.sawtooth(2 * np.pi * frequency * t - (4/3) * np.pi, width=0.5)
    return phase_a, phase_b, phase_c

#check change in sign for zero crossing
def detect_zero_crossing(emf_prev, emf_current):
    return np.sign(emf_prev) != np.sign(emf_current)


prev_emf_a, prev_emf_b, prev_emf_c = 0, 0, 0

for t in time_points:
    emf_a, emf_b, emf_c = generate_back_emf(t, frequency, voltage_max) #create emf

    if detect_zero_crossing(prev_emf_a, emf_a) or detect_zero_crossing(prev_emf_b, emf_b) or detect_zero_crossing(prev_emf_c, emf_c): 
        current_state = (current_state + 1) % 6 #next state, can then output curresnt using this   

    prev_emf_a = emf_a
    prev_emf_b = emf_b
    prev_emf_c = emf_c

    #save for graphs
    commutation_states.append(current_state)
    emf_a_data.append(emf_a)
    emf_b_data.append(emf_b)
    emf_c_data.append(emf_c)

#plot pretty graphs
plt.figure(figsize=(10, 8))
plt.subplot(3, 1, 1)
plt.plot(time_points, emf_a_data, label="EMF Phase A")
plt.plot(time_points, emf_b_data, label="EMF Phase B")
plt.plot(time_points, emf_c_data, label="EMF Phase C")
plt.legend(loc="upper right")
plt.title("Back EMF for BLDC Motor Phases")

plt.subplot(3, 1, 2)
plt.plot(time_points, commutation_states, label="Commutation State", color="orange")
plt.ylim(-0.5, 5.5)
plt.title("Commutation States")
plt.xlabel("Time (s)")
plt.ylabel("State")

plt.tight_layout()
plt.show()
