# Cartpole

Progressive control implementations for the cartpole task in MuJoCo. The same environment is used across both stages so results are directly comparable.

## Task

A cart on a frictionless track must shuttle between two fixed targets while keeping a pole balanced upright. When the cart reaches one target it switches to the other, indefinitely.

| Stage | Method | Status  |
|-------|--------|---------|
| 1 | PD Controller | Done    |
| 2 | PPO (PyTorch, from scratch) | Planned |

---

## Stage 1 - PD Controller

![balancing](logs/media/pid_balancing.png)

A naive approach, applying separate forces for position and balance, fails because both forces compete through a single actuator. The working solution is **cascaded control**: instead of pushing the cart directly, the controller sets a target pole angle based on distance and velocity. The cart moves as a consequence of the pole leaning.

```
target_angle = (0.1 * distance) - (0.15 * velocity)
target_angle = clip(target_angle, -0.2, 0.2)
force = pd_controller(kp=150, kd=50, target=target_angle, actual=angle, speed=angular_velocity)
```

Key insight: locomotion requires controlled imbalance. A perfectly vertical pole produces no horizontal movement.

→ [Full development log](logs/PID_controller.md)

---

## Stage 2 - PPO (planned)

Proximal Policy Optimization implemented from scratch in PyTorch, trained on the same cartpole environment.

Will include:
- Actor-critic network
- GAE (Generalized Advantage Estimation)
- Clipped surrogate objective
- Training curves across 3+ random seeds
- Comparison against Stage 1 PD baseline

---

## File Structure

```
cartpole/
├── main.py          # PD controller
├── cartpole.xml     # MuJoCo scene
└── logs/
    ├── PID_controller.md   # Development log
    └── media/
        ├── pid_balancing.png
        └── pid_fail.png
```

## Run PD Controller

```bash
uv run python cartpole/pd_controller.py
```