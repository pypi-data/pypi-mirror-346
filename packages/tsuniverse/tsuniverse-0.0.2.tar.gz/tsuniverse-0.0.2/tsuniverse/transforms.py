"""A list of transforms."""

from .transform import Transform
from .transform_velocity import velocity_transform

TRANSFORMS = {
    Transform.NONE: lambda x: x,
    Transform.VELOCITY: velocity_transform,
}
