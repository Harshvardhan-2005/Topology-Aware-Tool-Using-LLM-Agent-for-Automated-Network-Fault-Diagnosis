"""Read-only Network Topology MCP Server for NIKA.

Provides topological graph awareness to LLM diagnostic agents.
Pure standard-library implementation (zero external dependencies).
Strictly read-only; does not reveal ground-truth fault injection states.
"""

from collections import deque
from typing import Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("network-topology")

# Network topology definition for dc_clos small fabric
NODES = {
    "spine1": {"role": "spine"},
    "spine2": {"role": "spine"},
    "leaf1": {"role": "leaf"},
    "leaf2": {"role": "leaf"},
    "leaf3": {"role": "leaf"},
    "leaf4": {"role": "leaf"},
    "host1": {"role": "host"},
    "host2": {"role": "host"},
    "host3": {"role": "host"},
    "host4": {"role": "host"},
}

ADJACENCY = {
    "spine1": [("leaf1", "fabric"), ("leaf2", "fabric"), ("leaf3", "fabric"), ("leaf4", "fabric")],
    "spine2": [("leaf1", "fabric"), ("leaf2", "fabric"), ("leaf3", "fabric"), ("leaf4", "fabric")],
    "leaf1": [("spine1", "fabric"), ("spine2", "fabric"), ("host1", "access")],
    "leaf2": [("spine1", "fabric"), ("spine2", "fabric"), ("host2", "access")],
    "leaf3": [("spine1", "fabric"), ("spine2", "fabric"), ("host3", "access")],
    "leaf4": [("spine1", "fabric"), ("spine2", "fabric"), ("host4", "access")],
    "host1": [("leaf1", "access")],
    "host2": [("leaf2", "access")],
    "host3": [("leaf3", "access")],
    "host4": [("leaf4", "access")],
}

@mcp.tool()
def list_devices() -> list[dict[str, str]]:
    """List all network devices and their designated architectural roles (spine, leaf, host)."""
    return [{"device": name, "role": data["role"]} for name, data in NODES.items()]

@mcp.tool()
def list_neighbours(device_id: str) -> list[dict[str, Any]]:
    """List all directly connected neighbour devices and link types for a given device."""
    dev = device_id.strip().lower()
    if dev not in ADJACENCY:
        return [{"error": f"Device {dev} not found in topology graph."}]
    
    return [
        {"neighbour": n, "role": NODES[n]["role"], "link_type": link_type}
        for n, link_type in ADJACENCY[dev]
    ]

@mcp.tool()
def find_path(source: str, destination: str) -> dict[str, Any]:
    """Find shortest topological paths between two network devices or hosts using BFS."""
    src = source.strip().lower()
    dst = destination.strip().lower()

    if src not in NODES or dst not in NODES:
        return {"error": "Source or destination device not found in topology graph."}
    if src == dst:
        return {"source": src, "destination": dst, "shortest_hop_distance": 0, "available_paths": [[src]]}

    queue = deque([[src]])
    shortest_paths = []
    min_length = None

    while queue:
        path = queue.popleft()
        current = path[-1]

        if min_length is not None and len(path) > min_length:
            break

        if current == dst:
            if min_length is None:
                min_length = len(path)
            if len(path) == min_length:
                shortest_paths.append(path)
            continue

        for neighbour, _ in ADJACENCY.get(current, []):
            if neighbour not in path:
                queue.append(path + [neighbour])

    if not shortest_paths:
        return {"error": f"No topological path exists between {src} and {dst}."}

    return {
        "source": src,
        "destination": dst,
        "shortest_hop_distance": len(shortest_paths[0]) - 1,
        "available_paths": shortest_paths
    }

if __name__ == "__main__":
    mcp.run()
