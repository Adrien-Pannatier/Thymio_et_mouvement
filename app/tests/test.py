import numpy as np
import matplotlib.pyplot as plt

class PIDController:
    def __init__(self, Kp, Ki, Kd, sample_time):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.sample_time = sample_time
        self.last_error = 0
        self.integral = 0

    def update(self, setpoint, current_value):
        error = setpoint - current_value
        self.integral += error * self.sample_time
        derivative = (error - self.last_error) / self.sample_time
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.last_error = error
        return output

def simulate_vehicle(initpose, target_speed, target_orientation, time, dt, Kp, Ki, Kd):
    pid_speed_controller = PIDController(Kp, Ki, Kd, dt)
    pid_orientation_controller = PIDController(Kp, Ki, Kd, dt)
    # pid_position_controller = PIDController(Kp, Ki, Kd, dt)
    print(initpose)
    # pose = None
    pose = initpose
    speed = 0.0
    orientation = 0.0
    speed_history = []
    orientation_history = []
    pose_history = []

    for t in np.arange(0, time, dt):
        # print(t)
        # speed_error = target_speed - speed
        # orientation_error = target_orientation - orientation
        # position_error = target_position - pose

        speed_output = pid_speed_controller.update(target_speed, 0)
        orientation_output = pid_orientation_controller.update(target_orientation, 0)
        # position_output = pid_position_controller.update(np.linalg.norm(position_error), 0)

        speed = speed + speed_output * dt
        orientation = orientation + orientation_output * dt

        pose = pose + speed * np.array([np.cos(orientation), np.sin(orientation)]) * dt
        print(initpose)
        # print(pose)
        speed_history.append(speed)
        orientation_history.append(orientation)
        pose_history.append(pose)

    return pose, pose_history, speed_history, orientation_history

if __name__ == "__main__":
    initial_pose = np.array([0.1, 0.1])
    target_speed = 1
    target_orientation = 3.14
    total_time = 200
    time_step = 0.1

    Kp = 1.0
    Ki = 0.1
    Kd = 0.1

    print(initial_pose)
    final_pose, pose_history, speed_history, orientation_history = simulate_vehicle(initial_pose, target_speed, target_orientation, total_time, time_step, Kp, Ki, Kd)


    plt.plot(speed_history)
    plt.title("Speed Control")
    plt.xlabel("Time")
    plt.ylabel("Speed")
    plt.show()

    plt.plot(orientation_history)
    plt.title("Orientation Control")
    plt.xlabel("Time")
    plt.ylabel("Orientation")
    plt.show()

    # print(pose_history)
    print(initial_pose)
    for pose in pose_history:
        plt.plot(pose[0], pose[1], 'o')
    plt.plot(initial_pose[0], initial_pose[1], '+')
    plt.title("Pose")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()
