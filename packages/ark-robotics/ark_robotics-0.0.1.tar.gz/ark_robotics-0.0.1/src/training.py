"""
half_cheetah_gif.py
-------------------
Train a HalfCheetah agent with Stable-Baselines3 A2C, record a rollout, and
export the frames to an animated GIF.

Usage from the command line
---------------------------
python half_cheetah_gif.py            # uses defaults
python half_cheetah_gif.py --steps 5e4 --gif cheetah.gif --fps 60
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

import imageio
import numpy as np
from stable_baselines3 import A2C

# If you keep HalfCheetahEnv in a local `env.py`, replace this import as needed
from env import HalfCheetahEnv


# --------------------------------------------------------------------------- #
# Core utilities
# --------------------------------------------------------------------------- #
def make_env(render_mode: str = "rgb_array") -> HalfCheetahEnv:
    """Construct and return a HalfCheetahEnv instance."""
    return HalfCheetahEnv(render_mode=render_mode)


def train_agent(
    env: HalfCheetahEnv,
    total_timesteps: int = 10_000,
    policy: str = "MlpPolicy",
) -> A2C:
    """
    Train an A2C agent and return the trained model.

    Parameters
    ----------
    env
        The Gym environment (must expose `render()` with rgb_array support).
    total_timesteps
        Training budget.
    policy
        Policy architecture identifier for Stable-Baselines3.
    """
    return A2C(policy, env).learn(total_timesteps)


def rollout_frames(
    model: A2C,
    rollout_steps: int = 1_000,
    every_n: int = 2,
) -> List[np.ndarray]:
    """
    Run a policy rollout and collect rendered frames.

    Parameters
    ----------
    model
        A trained Stable-Baselines3 model. Assumes `model.env` is present.
    rollout_steps
        Number of interaction steps for the rollout.
    every_n
        Keep only every *n*th frame (useful for thinning long rollouts).

    Returns
    -------
    List[np.ndarray]
        RGB images (H×W×3, dtype uint8).
    """
    images: List[np.ndarray] = []
    obs, _ = model.env.reset()  # Gymnasium returns (obs, info)
    img = model.env.render()
    for step in range(rollout_steps):
        if step % every_n == 0:
            images.append(img)

        action, _ = model.predict(obs)
        # Gymnasium -> (obs, reward, terminated, truncated, info)
        # Gym classic -> (obs, reward, done, info)
        # Use underscore placeholders to stay agnostic.
        obs, *_ = model.env.step(action)
        img = model.env.render()
    return images


def write_gif(
    frames: List[np.ndarray],
    filename: str | Path = "custom_animal1.gif",
    fps: int = 29,
) -> None:
    """Save an image sequence to an animated GIF."""
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    imageio.mimsave(filename, frames, fps=fps)
    print(f"GIF saved → {filename}")


# --------------------------------------------------------------------------- #
# Command-line interface
# --------------------------------------------------------------------------- #
def _parse_args() -> argparse.Namespace:
    """CLI helper for quick experimentation."""
    parser = argparse.ArgumentParser(description="Train Half-Cheetah and export GIF.")
    parser.add_argument("--steps", type=int, default=10_000, help="Training timesteps")
    parser.add_argument(
        "--rollout", type=int, default=1_000, help="Rollout steps for the GIF"
    )
    parser.add_argument("--fps", type=int, default=29, help="GIF frame-rate")
    parser.add_argument("--gif", default="custom_animal1.gif", help="Output GIF file")
    parser.add_argument("--skip", type=int, default=2, help="Keep every n-th frame")
    return parser.parse_args()


def main() -> None:
    """Run the full training → rollout → GIF pipeline."""
    args = _parse_args()

    env = make_env()
    model = train_agent(env, total_timesteps=args.steps)
    frames = rollout_frames(model, rollout_steps=args.rollout, every_n=args.skip)
    write_gif(frames, args.gif, fps=args.fps)


if __name__ == "__main__":
    main()
