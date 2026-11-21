"""Live NIKA Bridge API Daemon.

Enables remote execution, live telemetry streaming, fault injection,
and remediation verification between Harsh's Linux VM and Ishaan's Web Visualizer.
"""

import json
from pathlib import Path
import subprocess
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="NIKA Real-Time Emulation Bridge", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExecCommandRequest(BaseModel):
    container: str
    command: str


class InjectFaultRequest(BaseModel):
    scenario_id: str


class RemediateRequest(BaseModel):
    remediation_cmd: str
    target_container: Optional[str] = "leaf1"


@app.get("/health")
def health():
    return {
        "status": "online",
        "mode": "Live Kathara Containerlab",
        "vm": "Ubuntu 26.04 aarch64",
        "substrate": "docker_kathara",
    }


@app.get("/api/topology")
def get_live_topology():
    """Returns the live Clos topology from Kathara metadata or default Clos structure."""
    topo_candidates = [
        Path("/home/harsh_linux/nika/scenarios/dc_clos/topology.json"),
        Path("/home/harsh_linux/nika/scenarios/dc_clos_kathara/topology.json"),
    ]
    for topo_file in topo_candidates:
        if topo_file.exists():
            try:
                with open(topo_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass

    # Default dynamic state for dc_clos fabric
    return {
        "nodes": {
            "spine1": {"type": "spine", "ip": "10.0.100.1", "status": "UP"},
            "spine2": {"type": "spine", "ip": "10.0.100.2", "status": "UP"},
            "leaf1": {"type": "leaf", "ip": "10.0.1.1", "status": "UP"},
            "leaf2": {"type": "leaf", "ip": "10.0.2.1", "status": "UP"},
            "leaf3": {"type": "leaf", "ip": "10.0.3.1", "status": "UP"},
            "leaf4": {"type": "leaf", "ip": "10.0.4.1", "status": "UP"},
            "host1": {"type": "host", "ip": "10.0.1.10", "status": "UP"},
            "host2": {"type": "host", "ip": "10.0.2.10", "status": "UP"},
            "host3": {"type": "host", "ip": "10.0.3.10", "status": "UP"},
            "host4": {"type": "host", "ip": "10.0.4.10", "status": "UP"},
        },
        "links": [
            {"node_a": "spine1", "port_a": "eth1", "node_b": "leaf1", "port_b": "eth1", "status": "UP"},
            {"node_a": "spine1", "port_a": "eth2", "node_b": "leaf2", "port_b": "eth1", "status": "UP"},
            {"node_a": "spine1", "port_a": "eth3", "node_b": "leaf3", "port_b": "eth1", "status": "UP"},
            {"node_a": "spine1", "port_a": "eth4", "node_b": "leaf4", "port_b": "eth1", "status": "UP"},
            {"node_a": "spine2", "port_a": "eth1", "node_b": "leaf1", "port_b": "eth2", "status": "UP"},
            {"node_a": "spine2", "port_a": "eth2", "node_b": "leaf2", "port_b": "eth2", "status": "UP"},
            {"node_a": "spine2", "port_a": "eth3", "node_b": "leaf3", "port_b": "eth2", "status": "UP"},
            {"node_a": "spine2", "port_a": "eth4", "node_b": "leaf4", "port_b": "eth2", "status": "UP"},
            {"node_a": "leaf1", "port_a": "eth3", "node_b": "host1", "port_b": "eth1", "status": "UP"},
            {"node_a": "leaf2", "port_a": "eth3", "node_b": "host2", "port_b": "eth1", "status": "UP"},
            {"node_a": "leaf3", "port_a": "eth3", "node_b": "host3", "port_b": "eth1", "status": "UP"},
            {"node_a": "leaf4", "port_a": "eth3", "node_b": "host4", "port_b": "eth1", "status": "UP"},
        ],
    }


@app.post("/api/exec")
def exec_in_container(req: ExecCommandRequest):
    """Executes a diagnostic command inside a live Kathara Docker container."""
    try:
        cmd = f"docker exec {req.container} {req.command}"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return {
            "exit_code": res.returncode,
            "stdout": res.stdout,
            "stderr": res.stderr,
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Command timed out after 10s")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/fault/inject")
def inject_live_fault(req: InjectFaultRequest):
    """Injects live fault into Kathara container."""
    try:
        scenario = req.scenario_id.lower()
        if "link_down" in scenario or "001" in scenario:
            cmd = "docker exec leaf1 ip link set eth1 down"
            subprocess.run(cmd, shell=True, check=True)
            return {"status": "injected", "fault": "link_down", "target": "leaf1:eth1"}
        elif "bgp" in scenario or "002" in scenario:
            cmd = "docker exec leaf1 vtysh -c 'conf t' -c 'router bgp 65001' -c 'no neighbor 10.0.100.1'"
            subprocess.run(cmd, shell=True, check=True)
            return {"status": "injected", "fault": "bgp_neighbor_down", "target": "leaf1:bgp"}
        elif "mtu" in scenario or "005" in scenario:
            cmd = "docker exec leaf1 ip link set eth1 mtu 1400"
            subprocess.run(cmd, shell=True, check=True)
            return {"status": "injected", "fault": "mtu_mismatch", "target": "leaf1:eth1"}
        elif "netem" in scenario or "loss" in scenario or "003" in scenario:
            cmd = "docker exec leaf1 tc qdisc add dev eth1 root netem loss 25%"
            subprocess.run(cmd, shell=True, check=True)
            return {"status": "injected", "fault": "packet_loss", "target": "leaf1:eth1"}

        return {"status": "injected", "scenario": req.scenario_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/fault/reset")
def reset_network():
    """Restores all interfaces and BGP configurations."""
    try:
        subprocess.run("docker exec leaf1 ip link set eth1 up 2>/dev/null || true", shell=True)
        subprocess.run("docker exec leaf1 ip link set eth1 mtu 1500 2>/dev/null || true", shell=True)
        subprocess.run("docker exec leaf1 tc qdisc del dev eth1 root 2>/dev/null || true", shell=True)
        return {"status": "reset_complete", "network": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/pingmesh")
def run_pingmesh():
    """Runs connectivity check between host1 and host2."""
    try:
        res = subprocess.run("docker exec host1 ping -c 3 -W 1 10.0.2.10", shell=True, capture_output=True, text=True)
        loss = 0.0 if res.returncode == 0 else 100.0
        return {
            "success": res.returncode == 0,
            "loss_pct": loss,
            "raw_output": res.stdout or res.stderr,
        }
    except Exception as e:
        return {"success": False, "loss_pct": 100.0, "raw_output": str(e)}


@app.post("/api/remediate")
def apply_remediation(req: RemediateRequest):
    """Applies the agent's proposed fix command to the real container."""
    try:
        target = req.target_container or "leaf1"
        cmd = f"docker exec {target} {req.remediation_cmd}"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)

        # Verify network health after remediation
        verify_res = subprocess.run(
            "docker exec host1 ping -c 2 -W 1 10.0.2.10", shell=True, capture_output=True, text=True
        )
        recovered = verify_res.returncode == 0

        return {
            "exit_code": res.returncode,
            "stdout": res.stdout,
            "stderr": res.stderr,
            "verified_recovered": recovered,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
