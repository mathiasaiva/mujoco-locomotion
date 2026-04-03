# mujoco-locomotion

A progressive implementation of locomotion controllers in MuJoCo, built to develop deep understanding of RL-based control. Each stage isolates one new problem, the goal is to understand what's actually happening, not wrap a library call.

## Overview

This repo follows a deliberate curriculum, each environment adds one new hard problem on top of the last. The goal is to build genuine understanding of locomotion control rather than wrapping a library call.

| Stage | Environment | Method | Status      |
|-------|-------------|--------|-------------|
| 1 | Cartpole | PD Controller | In progress |
| 2 | Cartpole | PPO (from scratch, PyTorch) | Planned     |
| 3 | Hopper | PPO | Planned     |
| 4 | Humanoid | PPO / SAC | Planned     |

## Motivation

Locomotion is one of the core unsolved problems in embodied AI. Before reaching humanoid walking, this project works through the canonical MuJoCo progression understanding each failure mode before moving to the next environment.

## Structure

```
mujoco-locomotion/
├── cartpole/          # Stage 1: balance control
├── humanoid/          # Stage 4: bipedal locomotion
├── sequence_model/    # Sequence modeling experiments
├── notebooks/         # Analysis and visualization
└── logs/              # Training runs
```

## Stages

### Stage 1 - Cartpole: PD Controller
Classical proportional-derivative controller for pole balancing. Establishes the environment setup and a performance baseline before any learning.

### Stage 2 - Cartpole: PPO from Scratch
Reimplementation of Proximal Policy Optimization in PyTorch against the same cartpole environment. Includes:
- Actor-critic network
- GAE (Generalized Advantage Estimation)
- Clipped surrogate objective
- Training curves across multiple random seeds

Target: match or approach SB3 baseline performance.

### Stage 3 - Hopper
First real locomotion task. A single-legged agent that must balance and hop forward. Applies the Stage 2 PPO implementation without algorithm changes, if it works here, the implementation is solid.

### Stage 4 - Humanoid
17-joint bipedal locomotion in full 3D. The primary target of the project. PPO baseline followed by SAC for improved sample efficiency.

## Stack

- [MuJoCo](https://mujoco.org/) - physics simulation
- [Gymnasium](https://gymnasium.farama.org/) - environment interface
- [PyTorch](https://pytorch.org/) - neural network implementation
- [uv](https://github.com/astral-sh/uv) - dependency management

## Setup

```bash
git clone https://github.com/mathiasaivasovsky/mujoco-locomotion
cd mujoco-locomotion
uv sync
```

## References

- Schulman et al., [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347) (2017)
- Haarnoja et al., [Soft Actor-Critic](https://arxiv.org/abs/1801.01290) (2018)
- [CleanRL](https://github.com/vwxyzjn/cleanrl) - reference PPO implementation
- Todorov et al., [MuJoCo: A physics engine for model-based control](https://ieeexplore.ieee.org/document/6386109) (2012)

---

*Part of a broader interest in embodied intelligent systems, computer vision, control, and perception for physical-world agents.*