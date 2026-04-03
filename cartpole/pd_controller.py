import mujoco
import numpy as np
import mujoco.viewer
import time
import os

xml_path = os.path.join(os.path.dirname(__file__), "cartpole.xml")
model = mujoco.MjModel.from_xml_path(xml_path)
data = mujoco.MjData(model)

move = [False, False]
def key_callback(keycode):
    global move
    if keycode == 65:
        move = [True, False]
    elif keycode == 68:
        move = [False, True]

def pd_controller(kp, kd, target, actual, speed):
    """
    This function calculates the forces needed to achieve a target using a Proportional Derivative Controller.
        It accepts the proportional and derivative gain (kp, kd), a target, the current value, the previous error
    and the current time.

    It returns the calculated force.
    """
    error = target - actual
    p_force = kp * error
    d_force = kd * (-speed) # Change in speed
    return -(p_force + d_force)

def move_cartpole(target):
    """
    This function uses a PD controller with cascaded control to return the force needed
    to make a cart movee to a target while maintaining the pole balance.

    :param target: The target in the x direction that the cart should reach
    :return: Returns the force that should be applied to the cart to reach the target
    """
    x, angle = data.qpos[0], data.qpos[1] # Positional data
    v, a_v = data.qvel[0], data.qvel[1] # velocity

    # Calculate angle to maintain
    distance = target - x
    # The angle depends on the distance - the velocity, if the cart goes to fast it slows down.
    target_angle = (0.1 * distance) - (0.15 * v)
    target_angle = np.clip(target_angle, -0.2, 0.2)


    # Use PD controller to maintain given angle, this makes the car advance
    force = pd_controller(150, 50, target_angle, angle, a_v)
    return force

with mujoco.viewer.launch_passive(model, data) as viewer:
    obj = "mocap1" # Objective.

    start_time = time.time()

    while viewer.is_running():
        step_start = time.time()

        mujoco.mj_step(model, data)

        # If we reach the objective, switch and go to the other side
        objective = model.body(obj).pos
        if abs(objective[0] - data.qpos[0]) < 0.1 and abs(data.qvel[0]) < 0.3:
            if obj == "mocap1":
                obj = "mocap2"
            elif obj == "mocap2":
                obj = "mocap1"

        # Move cart
        data.ctrl[0] = move_cartpole(objective[0])

        viewer.sync()

        time_until_next_step = model.opt.timestep - (time.time() - step_start)
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)
