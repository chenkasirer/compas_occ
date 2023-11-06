from typing import List

from OCC.Core.TopoDS import TopoDS_Wire
from OCC.Core.TopoDS import topods
from OCC.Core.BRepTools import BRepTools_WireExplorer
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire
from OCC.Core.BRepAlgo import brepalgo_IsValid
from OCC.Core.ShapeFix import ShapeFix_Wire

from compas.utilities import pairwise
from compas.geometry import Polyline
from compas.geometry import Polygon
from compas.brep import BrepLoop

from compas_occ.brep import OCCBrepVertex
from compas_occ.brep import OCCBrepEdge


def wire_from_edges(edges: List[OCCBrepEdge]) -> TopoDS_Wire:
    """Construct a wire from a list of edges.

    Parameters
    ----------
    edges : list[:class:`compas_occ.brep.OCCBrepEdge`]
        The edges.

    Returns
    -------
    ``TopoDS_Wire``

    """
    builder = BRepBuilderAPI_MakeWire()
    for edge in edges:
        builder.Add(edge.occ_edge)
    return builder.Wire()


class OCCBrepLoop(BrepLoop):
    """Class representing an edge loop in the BRep of a geometric shape.

    Parameters
    ----------
    occ_wire : ``TopoDS_Wire``
        An OCC BRep wire.

    Attributes
    ----------
    vertices : list[:class:`~compas_occ.brep.BrepVertex`], read-only
        List of BRep vertices.
    edges : list[:class:`~compas_occ.brep.BrepEdge`], read-only
        List of BRep edges.

    Other Attributes
    ----------------
    occ_wire : ``TopoDS_Wire``
        The OCC BRep wire.

    """

    def __init__(self, occ_wire: TopoDS_Wire):
        super().__init__()
        self._occ_wire = None
        self.occ_wire = occ_wire

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
        edges = []
        for edge in self.edges:
            edges.append(edge.data)
        return edges

    # @data.setter
    # def data(self, data):
    #     edges = []
    #     for edgedata in data:
    #         edges.append(BrepEdge.from_data(edgedata))
    #     loop = BrepLoop.from_edges(edges)
    #     self.occ_wire = loop.occ_wire

    @classmethod
    def from_data(cls, data):
        raise NotImplementedError

    # ==============================================================================
    # OCC Properties
    # ==============================================================================

    @property
    def occ_wire(self) -> TopoDS_Wire:
        return self._occ_wire  # type: ignore

    @occ_wire.setter
    def occ_wire(self, loop: TopoDS_Wire) -> None:
        self._occ_wire = topods.Wire(loop)

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def is_valid(self) -> bool:
        return brepalgo_IsValid(self.occ_wire)

    @property
    def vertices(self) -> List[OCCBrepVertex]:
        vertices = []
        explorer = BRepTools_WireExplorer(self.occ_wire)
        while explorer.More():
            vertex = explorer.CurrentVertex()
            vertices.append(OCCBrepVertex(vertex))
            explorer.Next()
        return vertices

    @property
    def edges(self) -> List[OCCBrepEdge]:
        edges = []
        explorer = BRepTools_WireExplorer(self.occ_wire)
        while explorer.More():
            edge = explorer.Current()
            edges.append(OCCBrepEdge(edge))
            explorer.Next()
        return edges

    @edges.setter
    def edges(self, edges: List[OCCBrepEdge]) -> None:
        self.occ_wire = wire_from_edges(edges)

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_edges(cls, edges: List[OCCBrepEdge]) -> "OCCBrepLoop":
        """Construct a loop from a collection of edges.

        Parameters
        ----------
        edges : list[:class:`compas_occ.brep.BrepEdge`]
            The edges.

        Returns
        -------
        ``OCCBrepLoop``

        """
        return cls(wire_from_edges(edges))

    @classmethod
    def from_polyline(cls, polyline: Polyline) -> "OCCBrepLoop":
        """Construct a loop from a polyline.

        Parameters
        ----------
        polyline : :class:`compas.geometry.Polyline`
            The polyline.

        Returns
        -------
        ``OCCBrepLoop``

        """
        edges = []
        for a, b in pairwise(polyline.points):
            edge = OCCBrepEdge.from_point_point(a, b)
            edges.append(edge)
        return cls(wire_from_edges(edges))

    @classmethod
    def from_polygon(cls, polygon: Polygon) -> "OCCBrepLoop":
        """Construct a loop from a polygon.

        Parameters
        ----------
        polygon : :class:`compas.geometry.Polygon`
            The polygon.

        Returns
        -------
        ``OCCBrepLoop``

        """
        edges = []
        for a, b in pairwise(polygon.points):
            edge = OCCBrepEdge.from_point_point(a, b)
            edges.append(edge)
        return cls(wire_from_edges(edges))

    # ==============================================================================
    # Methods
    # ==============================================================================

    def fix(self) -> None:
        """Try to fix the loop.

        Returns
        -------
        None

        """
        fixer = ShapeFix_Wire(self.occ_wire)  # type: ignore
        fixer.Perform()
        self.occ_wire = fixer.Wire()
