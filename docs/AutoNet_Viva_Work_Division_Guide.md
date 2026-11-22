---
title: "AutoNet RCA Agent: Work Division & Master Viva Guide"
subtitle: "B.Tech Project-I (IT-401) — Department of Information Technology, DTU"
author:
  - "Harshit Vaish (23/IT/067)"
  - "Harshwardhan Kumar Arya (23/IT/069)"
  - "Ishaan Yadav (23/IT/073)"
date: "Academic Year 2026-2027"
geometry: "margin=1in"
fontsize: 11pt
header-includes:
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhead[L]{AutoNet RCA Agent --- DTU IT-401}
  - \fancyhead[R]{Group 067}
  - \usepackage{booktabs}
  - \usepackage{microtype}
---

# 1. Project Overview & Midterm-to-Endterm Evolution

## 1.1 Project Metadata
* **Title:** AutoNet RCA Agent: A Topology-Aware Tool-Using LLM Agent for Automated Network Fault Diagnosis and Root-Cause Analysis
* **Institution:** Delhi Technological University (DTU), Bawana Road, Delhi-110042
* **Department:** Department of Information Technology
* **Supervisor:** Dr. Anamika Chauhan
* **Team Group:** Group No. 067
  * Harshit Vaish (Roll No: **23/IT/067**) — Systems & Network Infrastructure Lead
  * Harshwardhan Kumar Arya (Roll No: **23/IT/069**) — Live Linux Emulation, AI Protocol & MCP Lead
  * Ishaan Yadav (Roll No: **23/IT/073**) — Cognitive Control-Plane, BM25 RAG & Integration Lead

---

## 1.2 Evolution from Midterm to Endterm
In our **Midterm Evaluation**, our group established a functional **Mode A Proof-of-Concept**: an in-memory NetworkX graph simulation, five simulated read-only tools, a preliminary ReAct loop, and a local BM25 runbook retriever on a single host.

In our **Endterm Project**, we expanded this foundation into a **distributed cyber-physical system across two complementary tracks**:
* **Track A (AutoNet Enterprise Sandbox):** The high-speed simulation environment on Windows/macOS evaluating 10 core scenarios and 100 scaled campus scenarios with 0.0% entity hallucinations.
* **Track B (Live Linux Kernel & NIKA Benchmark):** The genuine Linux data center fabric running inside an Ubuntu aarch64 VM under UTM, featuring Docker, Kathará, FRRouting (BGP), the FastMCP Topology Server, and an encrypted Cloudflare tunnel.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          MIDTERM TO ENDTERM WORK DISTRIBUTION                          │
├────────────────────┬───────────────────────────────────┬───────────────────────────────┤
│ TEAM MEMBER        │ MIDTERM CONTRIBUTION (Phase 1-2)  │ ENDTERM EXPANSION (Phase 3-4) │
├────────────────────┼───────────────────────────────────┼───────────────────────────────┤
│ 1. Harshit Vaish   │ • Mode A NetworkX in-memory mock  │ • 8-node & 28-node topologies │
│    (23/IT/067)     │ • 5 read-only simulated tools     │ • Dynamic LLDP / ARP crawler  │
│                    │ • Synthetic 5-fault injector      │ • 10-core & 100-scaled eval   │
├────────────────────┼───────────────────────────────────┼───────────────────────────────┤
│ 2. Harshwardhan    │ • Basic ReAct loop (Thought/Act)  │ • Live Linux Kernel VRF & FRR │
│    Kumar Arya      │ • 6-step budget constraint        │ • FastMCP Topology Server     │
│    (23/IT/069)     │ • Regex hallucination guardrails  │ • Gemini Thought Signature fix│
│                    │ • ZeroShot & Static RAG baselines │ • 34% Speedup on NIKA (Track B│
├────────────────────┼───────────────────────────────────┼───────────────────────────────┤
│ 3. Ishaan Yadav    │ • Local BM25 ranking RAG          │ • Distributed Hybrid Driver   │
│    (23/IT/073)     │ • 10-scenario synthetic benchmark │ • Cloudflare Tunnel client    │
│                    │ • Basic FastAPI Canvas UI         │ • RFC 7938 / RFC 1191 RAG     │
│                    │ • `run_eval.py` evaluation runner │ • 1-Click Safe Remediation    │
└────────────────────┴───────────────────────────────────┴───────────────────────────────┘
```

---

# 2. Detailed Technical Breakdown & Ownership

## 2.1 Harshwardhan Kumar Arya (23/IT/069) — Track B: Live Linux Substrate & MCP Engine

### Responsibilities & Completed Tasks:
1. **Live Linux Emulation Substrate (Report Page 9, Sec 4):**
   * Configured an **Ubuntu 26.04 aarch64 virtual machine under UTM** on Apple Silicon Mac to provide the native Linux kernel `vrf` module required by NIKA.
   * Built and cached multi-container images (`nika/base`, `nika/frr`, `nika/onos`) running live FRRouting BGP spines, leaves, and hosts.
2. **Resolution of 7 Apple-Silicon Hardware Obstacles (Report Page 16–17):**
   * *Disk Exhaustion:* Dynamically resized the LVM root volume from 12 GB to 24 GB using `lvextend -l +100%FREE` and `resize2fs`.
   * *Emulation:* Configured `qemu-user-static` for AMD64 container support on ARM64 host.
   * *Permissions:* Managed Docker daemon socket access via `usermod -aG docker`.
3. **The LangChain Thought-Signature Patch (`src/thought_signature_patch.py`):**
   * Diagnosed HTTP 400 Bad Request error on Turn 2 of Google Gemini 3.5 Flash Lite tool calling.
   * Authored the serialization patch wrapping `_convert_dict_to_message` and `_lc_tool_call_to_openai_tool_call` so Google's cryptographic `thought_signature` survives multi-turn reasoning loops.
4. **FastMCP Topology Server (`src/topology_server.py`):**
   * Engineered the Model Context Protocol (MCP) server exposing `list_devices`, `list_neighbours`, and `find_path` over Clos fabrics.
   * Built using **pure Python standard library BFS queues** ($O(V+E)$ complexity), booting in $<1\text{ms}$ with zero external dependencies.
5. **NIKA Benchmark Smoke Test (Report Page 16, Table 3):**
   * Proved that topology awareness cut wall-clock time by **34.0%** (64.4s down to 42.5s) and saved **9.1% input tokens** with parity in root-cause F1 (1.000).
6. **Live Bridge Daemon (`src/nika_bridge_api.py`) & Cloudflare Tunnel:**
   * Built the FastAPI bridge on port 8000 and exposed it via an encrypted Cloudflare Tunnel (`trycloudflare.com`).

---

## 2.2 Ishaan Yadav (23/IT/073) — Cognitive Control-Plane, BM25 RAG & Visualizer

### Responsibilities & Completed Tasks:
1. **The ReAct Diagnostic Agent Core (Report Page 12, Sec 5):**
   * Built the bounded ReAct loop with a hard ceiling of 6 steps.
   * Implemented the decision tree separating MTU truncation from NetEm channel loss.
2. **Graph Hallucination Guardrail (Report Page 13, Sec 6):**
   * Wrote the regex token parser cross-referencing final reports against immutable `raw_topology`, guaranteeing **0.0% entity hallucinations**.
3. **Okapi BM25 Domain Runbook RAG (Report Page 12, Sec 4):**
   * Implemented native BM25 ($k_1 = 1.5, b = 0.75$) indexing 6 RFC runbooks:
     * `icmp_troubleshooting.md` (RFC 792 ICMP)
     * `interface_state.md` (Administrative states)
     * `routing_triage.md` (Missing default routes)
     * `dns_resolution.md` (/etc/resolv.conf)
     * `clos_bgp_troubleshooting.md` (RFC 7938 Clos BGP)
     * `mtu_fragmentation_triage.md` (RFC 1191 Path MTU Discovery)
4. **Dual-Substrate Hybrid Execution Driver (Report Page 13, Sec 8):**
   * Built `HybridNetworkDriver` querying `GET /health` with a 1.2s timeout.
   * Automatically switches between **`LIVE_KATHARA` 🟢** mode (remote Docker containers) and **`LOCAL_SANDBOX` 🔵** mode (fail-safe local simulation).
5. **Glass-Box Mission Control Web UI (Report Page 14, Sec 10):**
   * Built the FastAPI 2.0 backend and HTML5 Canvas visualizer with real-time WebSocket trace streaming.
   * Engineered the **One-Click Safe Remediation Pipeline** (`/api/remediate`) with automated post-repair verification ping confirming 0% packet loss.

---

## 2.3 Harshit Vaish (23/IT/067) — Track A: Network Sandbox, Tools & Benchmarks

### Responsibilities & Completed Tasks:
1. **Network Topologies Formulation (Report Page 8, Sec 1):**
   * Formulated the 8-node corporate network (`config/topology.json`) with subnets `10.0.0.0/24` and `10.0.1.0/24`.
   * Formulated the 28-node campus network generator (`topology_large.json`) for the 100-scenario scaled benchmark.
2. **Network Sandbox Class (Mode A — Report Page 11, Sec 1):**
   * Implemented in-memory NetworkX state machine that runs on any machine with no root access.
   * Implemented 5 Linux-style CLI output synthesizers (`exec_ping`, `exec_traceroute`, `exec_ip_route`, `exec_ip_link`, `exec_nslookup`).
3. **Diagnostic Tool Registry (Report Page 11, Sec 2):**
   * Defined the 5 least-privilege read-only inspection primitives (`ping_tool`, `traceroute_tool`, `routing_table_tool`, `interface_stats_tool`, `dns_query_tool`).
4. **Fault Injection Engine (Report Page 12, Sec 3):**
   * Built the 5 fault archetype mutators (Link-down, routing blackhole, channel impairment, DNS failure, MTU mismatch).
5. **Dynamic Topology Discovery (Report Page 13, Sec 7):**
   * Built the simulated IEEE 802.1AB LLDP / ARP crawler that builds a live discovered graph without reading `topology.json`.
6. **Benchmark Suites Execution (Report Page 15, Sec 1 & 2):**
   * Ran the 10-scenario core benchmark (100% accuracy, 2.3 avg calls) and the 100-scenario scaled benchmark (97% category, 94% precision).

---

# 3. Codebase Audit: Key Updates & Improvements

| Area | Initial Codebase Guide | What Was Actually Implemented & Pushed | Reason for Evolution |
| :--- | :--- | :--- | :--- |
| **Topology Engine** | Recommended `networkx` for `topology_server.py`. | **Pure Python Standard Library BFS (`collections.deque`).** Zero pip dependencies. | NetworkX installation timed out in VM sandbox; pure stdlib executes in $<1\text{ms}$ with zero memory footprint. |
| **Networking** | Assumed same Wi-Fi LAN (`192.168.64.2:8000`). | **Cloudflare Zero-Trust QUIC Tunnel (`trycloudflare.com`).** | Team members worked remotely across different home Wi-Fi networks; tunnel bypasses NAT firewalls securely. |
| **Bridge API** | Basic interface down & BGP endpoints. | **Full REST suite:** `/health`, `/api/topology`, `/api/exec`, `/api/fault/inject`, `/api/fault/reset`, `/api/pingmesh`, `/api/remediate`. | Enables complete closed-loop fault injection, MTU testing, and post-remediation verification from UI. |

---

# 4. Synchronized 5-Minute Viva Presentation Script

* **[0:00 – 1:15] Harshit Vaish:**  
  *"Respected examiners, I developed Track A: The Network Sandbox, Diagnostic Tools, and Benchmark Topologies. I formulated our 8-node and 28-node campus topologies and engineered the `NetworkSandbox` class in Python using NetworkX. Following the principle of least privilege, I exposed 5 strictly read-only inspection tools and 5 fault mutators. I also implemented simulated LLDP discovery and conducted our 10-scenario core benchmark (100% accuracy) and 100-scenario scaled evaluation (97% accuracy). Harsh will now present Track B on live Linux emulation."*

* **[1:15 – 2:30] Harshwardhan Kumar Arya:**  
  *"Respected examiners, I engineered Track B: The Live Linux Emulation Substrate, NIKA Benchmark, and the MCP Topology Server. Because macOS lacks the kernel VRF module, I set up an ARM64 Ubuntu VM running real Kathará Docker containers with live FRRouting BGP daemons, resolving 7 hardware and storage obstacles including on-line LVM expansion. I developed our FastMCP Topology Server using standard-library BFS shortest-path queries. When integrating Gemini 3.5 Flash Lite, I discovered an industry protocol bug where LangChain stripped Google's `thought_signature`, causing 400 Bad Request crashes; I authored a serialization monkey-patch that solved it. On the NIKA benchmark, our topology tool cut diagnostic latency by **34.0%** and saved **9.1% input tokens**. I also created the FastAPI bridge daemon and Cloudflare tunnel that allows Ishaan to drive my containers live."*

* **[2:30 – 4:30] Ishaan Yadav (with Live Screen Demo):**  
  *"Respected examiners, I developed the Cognitive Control-Plane, BM25 Runbook RAG, Hybrid Driver, and Web Dashboard. I built the ReAct diagnostic agent with MTU-vs-NetEm disambiguation and our graph guardrail that guarantees 0.0% entity hallucinations. I integrated native Okapi BM25 retrieval over 6 IETF RFC runbooks (including RFC 7938 for BGP and RFC 1191 for PMTU). I built the `HybridNetworkDriver` connecting my Windows dashboard to Harsh's live Linux containers over the Cloudflare tunnel, with fail-safe local fallback.*  
  *(Live Demo): Watch the screen: I inject a trunk drop on spine1—the link turns RED. The Gemini agent streams its thoughts over WebSockets, retrieves the RFC runbook, and isolates `leaf1:eth1` down in 2 steps. With one click, I approve the synthesized fix: `ip link set eth1 up` executes on the remote container, the link turns GREEN, and our automated ping verification confirms 100% recovery."*

* **[4:30 – 5:00] All Members:**  
  *Concluding remarks and open for panel examination.*

---

# 5. Master Empirical Metrics Summary

| Evaluation Track | Benchmark | Diagnostic Latency | Input Tokens | Output Tokens | Root-Cause Accuracy | Hallucinations |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Track A (Sandbox)** | Core Benchmark ($N=10$) | 2.4s | --- | --- | **100.0%** | **0.0%** |
| **Track A (Sandbox)** | Scaled Benchmark ($N=100$) | 2.8s avg | --- | --- | **94.0%** | **0.0%** |
| **Track B (Live NIKA)** | Baseline Version (b) | 64.4s | 66,524 | 1,123 | **100.0% (1.000)** | Clean |
| **Track B (Live NIKA)** | Topology-Aware Version (c) | **42.5s (-34.0%)** | **60,448 (-9.1%)** | **926 (-17.5%)** | **100.0% (1.000)** | **0.0%** |
