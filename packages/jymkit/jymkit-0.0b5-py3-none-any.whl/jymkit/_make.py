import difflib
from typing import Optional, TypedDict

import jymkit.envs
from jymkit._environment import Environment

from ._wrappers import GymnaxWrapper, Wrapper

JYMKIT_ENVS = [
    "CartPole",
    "Acrobot",
]

GYMNAX_ENVS = [
    "Pendulum-v1",
    "MountainCar-v0",
    "MountainCarContinuous-v0",
    # "Asterix-MinAtar",
    "Breakout-MinAtar",
    # "Freeway-MinAtar",
    "SpaceInvaders-MinAtar",
    "DeepSea-bsuite",
]

ALL_ENVS = JYMKIT_ENVS + GYMNAX_ENVS


class ExternalEnvDict(TypedDict):
    package_name: str
    git_url: str


def make(
    env_name: str,
    wrapper: Optional[Wrapper] = None,
    external: Optional[ExternalEnvDict] = None,
    **env_kwargs,
) -> Environment:
    if external is not None:
        # try to import package_name
        try:
            __import__(external["package_name"])
        except ImportError:
            # if the package is not installed, try to install it
            try:
                import subprocess

                # add git+ to the url if it is not already there
                if not external["git_url"].startswith("git+"):
                    external["git_url"] = "git+" + external["git_url"]

                subprocess.run(["pip", "install", external["git_url"]])
                __import__(external["package_name"])
            except Exception as e:
                raise ImportError(
                    f"Failed to install {external['package_name']}. Please install it manually.",
                    e,
                )
            # import the environment from the package
        env = getattr(__import__(external["package_name"]), env_name)(**env_kwargs)

    elif env_name in JYMKIT_ENVS:
        if env_name == "CartPole":
            env = jymkit.envs.CartPole(**env_kwargs)
        elif env_name == "Acrobot":
            env = jymkit.envs.Acrobot(**env_kwargs)

    elif env_name in GYMNAX_ENVS:
        try:
            import gymnax
        except ImportError:
            raise ImportError(
                "Gymnax is not installed. Please install it with `pip install gymnax`."
            )
        env, _ = gymnax.make(env_name, **env_kwargs)
        if wrapper is None:
            print(
                "Wrapping Gymnax environment with GymnaxWrapper\n",
                " Disable this behavior by passing wrapper=False",
            )
            env = GymnaxWrapper(env)
    else:
        matches = difflib.get_close_matches(env_name, ALL_ENVS, n=1, cutoff=0.6)
        suggestion = (
            f" Did you mean {matches[0]}?"
            if matches
            else " Available environments are:\n" + "\n".join(ALL_ENVS)
        )
        raise ValueError(f"Environment {env_name} not found.{suggestion}")

    if wrapper is not None:
        if isinstance(wrapper, Wrapper):
            env = wrapper(env)  # type: ignore
        else:
            raise ValueError("Wrapper must be an instance of Wrapper class.")
    return env  # type: ignore
