# type: ignore

from compas.geometry import Point
from compas.utilities import meshgrid, flatten, linspace
from compas.geometry import NurbsSurface
from compas_view2.app import App
from compas_view2.objects import Collection


points = [
    [Point(0, 0, 0), Point(1, 0, 0), Point(2, 0, 0), Point(3, 0, 0)],
    [Point(0, 1, 0), Point(1, 1, 2), Point(2, 1, 2), Point(3, 1, 0)],
    [Point(0, 2, 0), Point(1, 2, 2), Point(2, 2, 2), Point(3, 2, 0)],
    [Point(0, 3, 0), Point(1, 3, 0), Point(2, 3, 0), Point(3, 3, 0)],
]

surface = NurbsSurface.from_points(points=points)

# ==============================================================================
# Frames
# ==============================================================================

U, V = meshgrid(linspace(*surface.domain_u), linspace(*surface.domain_v), "ij")
frames = [surface.frame_at(u, v) for u, v in zip(flatten(U), flatten(V))]

# ==============================================================================
# Visualisation
# ==============================================================================

view = App()

view.add(surface, show_lines=False)
view.add(Collection(frames, [{"size": 0.1} for frame in frames]), pointsize=0.25)

view.run()
