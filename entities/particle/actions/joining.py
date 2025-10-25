import inspect

from entities import (
    Particle,
)

def join_to_other(
        prev_particle: Particle,
        next_particle: Particle,
    ) -> None:
    func_name = inspect.currentframe().f_code.co_name
    prev_particle.extensions["actions"][func_name]["next"] = next_particle
    next_particle.extensions["actions"][func_name]["prev"] = prev_particle


