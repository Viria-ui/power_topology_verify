"""Core package exports.

Heavy graph modules depend on optional runtime packages such as pydantic,
networkx and pandas. Keep package import lightweight so modules like
core.telemetry_evaluator and core.score_engine can be tested independently.
"""

__all__ = [
    "Device",
    "ConnectPoint",
    "TopoEdge",
    "AbnormalItem",
    "BreakpointItem",
    "TieLoopItem",
    "TopologyGraph",
    "build_device_internal_edges",
    "TopologyBuilder",
    "validate_svg_only",
    "validate_svg_vs_topology",
    "validate_edit_action",
    "export_defect_report",
]

try:
    from .graph_model import (
        Device,
        ConnectPoint,
        TopoEdge,
        AbnormalItem,
        BreakpointItem,
        TieLoopItem,
        TopologyGraph,
        build_device_internal_edges,
    )
    from .topology_builder import TopologyBuilder
    from .topology_validator import (
        validate_svg_only,
        validate_svg_vs_topology,
        validate_edit_action,
        export_defect_report,
    )
except ImportError:
    pass
