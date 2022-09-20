from compas.geometry import Point
from compas.geometry import Polyline
from compas_occ.geometry import OCCNurbsSurface
from compas_view2.app import App


points = [
    [Point(0, 0, 0), Point(1, 0, 0), Point(2, 0, 0), Point(3, 0, 0)],
    [Point(0, 1, 0), Point(1, 1, 2), Point(2, 1, 2), Point(3, 1, 0)],
    [Point(0, 2, 0), Point(1, 2, 2), Point(2, 2, 2), Point(3, 2, 0)],
    [Point(0, 3, 0), Point(1, 3, 0), Point(2, 3, 0), Point(3, 3, 0)],
]

surface = OCCNurbsSurface.from_points(points=points)

# ==============================================================================
# JSON Data
# ==============================================================================

string = surface.to_jsonstring(pretty=True)

print(string)

other = OCCNurbsSurface.from_jsonstring(string)

print(surface == other)

# ==============================================================================
# Visualisation
# ==============================================================================

view = App()

u = surface.u_isocurve(0.5 * sum(surface.u_domain))
v = surface.v_isocurve(0.5 * sum(surface.v_domain))

view.add(Polyline(u.locus()), linewidth=1, linecolor=(0.3, 0.3, 0.3))
view.add(Polyline(v.locus()), linewidth=1, linecolor=(0.3, 0.3, 0.3))

for curve in surface.boundary():
    view.add(Polyline(curve.locus()), linewidth=2, linecolor=(0, 0, 0))

view.add(other.to_mesh(), show_lines=False)

view.run()
