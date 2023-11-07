# type: ignore

from math import radians
from compas.geometry import Box
from compas.geometry import Plane
from compas.geometry import Rotation
from compas_view2.app import App

box = Box.from_width_height_depth(1, 1, 1).to_brep()

plane = Plane.worldXY()
R = Rotation.from_axis_and_angle([0, 1, 0], radians(30))

plane.transform(R)

slice = box.slice(plane)

viewer = App()
viewer.add(slice, linewidth=2)
viewer.show()
