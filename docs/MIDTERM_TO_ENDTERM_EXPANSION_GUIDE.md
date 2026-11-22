# 🎓 DTU IT-401 B.Tech Project-I — Endterm Expansion & Viva Guide
## From Midterm Foundation to Endterm Distributed Cyber-Physical System

**Project Title:** AutoNet RCA Agent: A Topology-Aware Tool-Using Agent for Automated Network Fault Diagnosis and Root-Cause Analysis  
**Department:** Department of Information Technology, Delhi Technological University (DTU)  
**Supervisor:** Dr. Anamika Chauhan  
**Group Number:** Group No. 067  
**Team Members:**
1. **Harshit Vaish** (Roll No: **23/IT/067**) — Systems & Network Infrastructure Lead
2. **Harshvardhan Kumar Arya** (Roll No: **23/IT/068**) — AI Agent & Cognitive Reasoning Lead
3. **Ishaan Yadav** (Roll No: **23/IT/073**) — Knowledge Systems, Evaluation & Integration Lead

---

# 📌 1. The Core Narrative: How Midterm Expanded into Endterm

In the **Midterm Evaluation**, our project demonstrated a successful **proof-of-concept (Mode A)**: an in-memory NetworkX network simulation, a ReAct prompt agent, and a local BM25 RAG engine running on a single laptop.

In the **Endterm**, we did not discard our midterm work; we **expanded every module into a production-grade, distributed cyber-physical system**:
1. **Harshit** expanded the synthetic in-memory simulation into a **live multi-container Linux Kernel VRF and Kathará BGP Clos fabric**, backed by an on-line LVM disk expansion and a live FastAPI bridge.
2. **Harshvardhan** expanded the custom ReAct agent into an open **Model Context Protocol (MCP) Topology Server**, solved the Google Gemini 3.x `thought_signature` protocol crash, and proved a **34.0% latency reduction** on the NIKA benchmark.
3. **Ishaan** expanded the local dashboard and RAG into a **Distributed Hybrid Architecture over Cloudflare Tunnels**, grounded the agent in **IETF RFC standards (RFC 7938 / RFC 1191)**, and engineered a **Closed-Loop Safe Remediation Pipeline** with automated recovery verification.

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           MIDTERM TO ENDTERM EVOLUTION MATRIX                                  │
├───────────────────┬───────────────────────────────────┬────────────────────────────────────────┤
│ TEAM MEMBER       │ MIDTERM CONTRIBUTION (Phase 1-2)  │ ENDTERM EXPANSION (Phase 3-4)          │
├───────────────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ 1. Harshit Vaish  │ • Mode A NetworkX in-memory mock  │ • Live Linux Kernel VRF & netns        │
│    (23/IT/067)    │ • 5 read-only simulated tools     │ • Live Kathará Docker BGP Clos fabric  │
│                   │ • Synthetic 5-fault injector      │ • On-line LVM partition expansion      │
│                   │ • `network_sandbox.py`            │ • Live Bridge Daemon (`nika_bridge`)   │
├───────────────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ 2. Harshvardhan   │ • Basic ReAct loop (Thought/Act)  │ • Model Context Protocol (FastMCP)     │
│    Kumar Arya     │ • 6-step budget constraint        │ • Pure-Python stdlib BFS shortest path │
│    (23/IT/068)    │ • Regex hallucination filter      │ • Google Gemini Thought Signature Fix  │
│                   │ • ZeroShot & Static RAG baselines │ • 34% Latency Drop on NIKA Benchmark   │
├───────────────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ 3. Ishaan Yadav   │ • Local BM25 ranking RAG          │ • Distributed Hybrid Driver (`hybrid`) │
│    (23/IT/073)    │ • 10-scenario synthetic benchmark │ • Cloudflare Zero-Trust Tunnel Gateway │
│                   │ • Basic FastAPI Canvas UI         │ • RFC 7938 (BGP) & RFC 1191 (PMTU) RAG │
│                   │ • `run_eval.py` evaluation runner │ • 1-Click Safe Remediation & Pingmesh  │
└───────────────────┴───────────────────────────────────┴────────────────────────────────────────┘
```

---

# 👤 MEMBER 1: Harshit Vaish (23/IT/067)
**Role:** Systems & Network Infrastructure Lead  
**Midterm Foundation:** Module 1 (Testbed Simulation, Diagnostic Tooling & Fault Injection)  
**Endterm Expansion:** Live Linux Kernel VRF, Docker Kathará BGP Clos Fabric & Bridge Daemon

---

### 1.1 Layman Explanation (The Story)
> *"In the midterm, I built a toy model of a network using Python in-memory math on Windows. While that worked for unit testing, real data centers don't run on Python mocks—they run on Linux switches.  
> For the endterm, I took our toy model and built a real, working data center inside an Ubuntu virtual machine. Every switch is an independent Docker container running real enterprise BGP routing software (FRRouting). When we cut a cable or change an MTU, real Linux packets drop. I also built the FastAPI bridge daemon so my teammates could control this real network across the internet."*

### 1.2 Technical Deep Dive (The Grilling Knowledge)
* **From Mode A (Simulation) to Mode B (Ground Truth):**
  * Midterm used NetworkX graph traversal (`_resolve_l3_path`).
  * Endterm transitioned to **Kathará Network Emulation** running on **Ubuntu 26.04 LTS aarch64**.
  * Configured a 2-Spine, 4-Leaf, 4-Host Clos topology (`dc_clos`).
* **Linux Kernel Virtual Routing & Forwarding (VRF):**
  * Configured the Linux kernel `vrf` module to isolate routing domains across switches, preventing route leaking in multi-tenant fabrics.
* **Live FRRouting (FRR) Dynamic Peering:**
  * Replaced static routing tables with active `bgpd` and `zebra` daemons.
  * Switches peer via eBGP (ASNs 65001–65006), exchanging `/30` interface subnets and `/32` loopbacks with Equal-Cost Multi-Path (ECMP).
* **On-Line LVM Volume Expansion:**
  * Compiling multi-architecture Docker images (`nika/base`, `nika/onos`, `nika/frr`) filled the 12 GB virtual disk.
  * Harshit expanded the root partition on-the-fly without taking the VM offline:
    ```bash
    sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
    sudo resize2fs /dev/ubuntu-vg/ubuntu-lv
    ```
    Expanded root volume from 12 GB to 24 GB while preserving running containers.
* **Live Bridge Daemon (`src/nika_bridge_api.py`):**
  * Authored the FastAPI daemon listening on port 8000 inside the VM.
  * Implemented live execution hooks (`docker exec`), real fault injection (`ip link set down`, `vtysh` BGP teardowns, `tc qdisc` NetEm jitter/loss), and post-fix verification.

### 1.3 Key Files Owned
* `src/sandbox/network_sandbox.py` (Midterm Mode A engine)
* `src/tools/network_tools.py` (Least-privilege diagnostic primitives)
* `src/faults/fault_injector.py` (5 failure archetypes)
* `src/nika_bridge_api.py` (Endterm live bridge daemon)
* Kathará scenario files: `/home/harsh_linux/nika/scenarios/dc_clos/`

### 1.4 Rehearsed Viva Speaking Script (75 Seconds)
> *"Respected panel members, my name is Harshit Vaish (Roll No: 23/IT/067). In the midterm, I presented Module 1, where I engineered our in-memory NetworkX sandbox and our 5 least-privilege diagnostic tools.  
> For the endterm, I expanded our system from a synthetic simulation into a **live Linux kernel ground-truth emulation substrate**.  
> Because enterprise networks run real routing protocols, I deployed an ARM64 Ubuntu Linux environment running a multi-container Clos leaf-spine fabric using Kathará and Docker. Every switch runs the Linux kernel VRF subsystem and active FRRouting BGP daemons exchanging live routing updates.  
> To simulate realistic network degradation, I upgraded our fault injector to mutate real kernel states—including physical interface drops, BGP peer withdrawals via vtysh, MTU fragmentation drops, and Linux tc netem packet loss. I also built the FastAPI bridge daemon that exposes live container telemetry to our teammates over port 8000.  
> I now hand over to Harshvardhan, who will explain how our cognitive reasoning agent evolved."*

### 1.5 Tough Questions & Answers for Harshit
* **Q: "Why did you keep NetworkX if you moved to Kathará?"**
  * **A:** *"We preserved NetworkX as our fail-safe fallback (Mode A) inside our Hybrid Driver. If network connectivity drops or the VM is offline during testing, the agent transparently falls back to NetworkX, guaranteeing zero downtime."*
* **Q: "How does FRRouting handle an interface failure in your Clos fabric?"**
  * **A:** *"When `leaf1:eth1` drops, the Linux kernel carrier signal is lost. FRR's `zebra` daemon detects the link-down event and signals `bgpd`, which immediately sends a BGP UPDATE message withdrawing the prefix from `spine1`. Traffic then reroutes over `spine2` via ECMP."*

---

# 👤 MEMBER 2: Harshvardhan Kumar Arya (23/IT/068)
**Role:** AI Agent & Cognitive Reasoning Lead  
**Midterm Foundation:** Module 2 (ReAct Detective Agent & Hallucination Guardrails)  
**Endterm Expansion:** Model Context Protocol (MCP) Topology Server, Gemini Thought Signature Patch & NIKA Benchmarking

---

### 2.1 Layman Explanation (The Story)
> *"In the midterm, I created the detective brain. Instead of letting the AI guess blindly, I made it think step-by-step: Thought, Action, Observation. I also built a filter that stopped it from hallucinating fake switch names.  
> For the endterm, I upgraded the AI from solving textbook puzzles to diagnosing our real data center. I gave it a dedicated Model Context Protocol (MCP) tool that acts like Google Maps for switches, calculating shortest paths in milliseconds. When Google's newest Gemini 3.5 AI started crashing because of an industry-wide protocol bug in LangChain, I found the bug and fixed it with a monkey-patch. In our final tests, my upgrades made the AI 34% faster while using 9% fewer tokens!"*

### 2.2 Technical Deep Dive (The Grilling Knowledge)
* **From Custom Python Tools to Standardized Model Context Protocol (MCP):**
  * In midterm, tools were loose Python functions passed into a local agent.
  * In endterm, Harshvardhan engineered a standalone **FastMCP Topology Server** (`src/topology_server.py`) adhering to Anthropic's open MCP JSON-RPC standard.
  * Exposes three read-only primitives: `list_devices`, `list_neighbours`, and `find_path`.
* **Zero-Dependency BFS Graph Traversal:**
  * Wrote an optimized Breadth-First Search (BFS) shortest-path algorithm using standard library `collections.deque` with $O(V + E)$ complexity.
  * Zero external pip dependencies (no NetworkX or SciPy), allowing instant $<1\text{ms}$ startup inside locked-down sandboxes.
* **The Google Gemini "Thought Signature" Patch (`src/thought_signature_patch.py`):**
  * **The Problem:** Google Gemini 3.5 Flash Lite thinking models attach an internal cryptographic `extra_content.google.thought_signature` to function calls.
  * LangChain's OpenAI client adapter stripped this field during message serialization.
  * On Turn 2 of multi-turn tool calling, Google AI Studio rejected the request with `400 BadRequestError: Function call is missing a thought_signature`.
  * **The Fix:** Harshvardhan monkey-patched `_convert_dict_to_message` and `_lc_tool_call_to_openai_tool_call` in `langchain_openai.chat_models.base`, preserving `extra_content` through multi-turn ReAct loops.
* **NIKA Benchmark Comparative Evaluation:**
  * Evaluated on the standardized **NIKA benchmark** (`sands-lab/nika`):
    * **Version (b) [Baseline]:** Standard tools, no topology awareness.
    * **Version (c) [Proposed]:** Standard tools + `topology_mcp_server`.
  * Proved a **34.0% wall-clock latency reduction** (64.4s down to 42.5s) and **9.1% input token reduction** (66,524 down to 60,448).

### 2.3 Key Files Owned
* `src/agent/diagnostic_agent.py` (ReAct cognitive loop & budget controller)
* `src/agent/prompt_templates.py` (Dynamic few-shot system prompts)
* `src/baselines/` (`baseline_zero_shot.py`, `baseline_rag.py`)
* `src/topology_server.py` (FastMCP topology engine)
* `src/thought_signature_patch.py` (LangChain Google thought signature fix)
* `results/version_b_smoke_test.json` & `results/version_c_smoke_test.json`

### 2.4 Rehearsed Viva Speaking Script (75 Seconds)
> *"Respected panel members, I am Harshvardhan Kumar Arya (Roll No: 23/IT/068). In the midterm, I presented Module 2, where I designed our ReAct cognitive loop with a 6-step tool budget and our graph validation filter that achieved 0.0% entity hallucinations.  
> For the endterm, I expanded our cognitive engine into a standardized **Model Context Protocol (MCP) Topology Server** and resolved a critical model serialization barrier.  
> First, I implemented a read-only FastMCP server providing topological graph intelligence. Using an unweighted BFS shortest-path algorithm, it computes Clos ECMP paths in under 1 millisecond without external dependencies.  
> Second, during integration with Gemini 3.5 Flash Lite, I uncovered a protocol flaw: LangChain's adapter stripped Google's cryptographic thought_signature on multi-turn function calls, throwing 400 Bad Request errors. I reverse-engineered the serialization pipeline and authored a monkey-patch preserving extra_content, enabling stable multi-turn diagnosis.  
> On the NIKA benchmark, our topology-aware agent reduced diagnostic latency by **34.0%** and cut prompt token overhead by **9.1%**, while maintaining a **100% Root-Cause F1 score**.  
> I now hand over to Ishaan, who will present our distributed hybrid architecture and interactive dashboard."*

### 2.5 Tough Questions & Answers for Harshvardhan
* **Q: "Why does topology awareness reduce input tokens if you added more tools?"**
  * **Answer:** *"Without topology awareness, the baseline agent searches blindly: it runs repeated traceroutes and routing table dumps on non-faulty nodes, loading thousands of lines of terminal output into the prompt context. With `find_path`, the agent immediately bounds the search space to candidate devices between source and destination, issuing fewer diagnostic tool calls and keeping the context window concise."*
* **Q: "What exactly is the thought signature in Gemini 3.x?"**
  * **Answer:** *"Gemini 3.x thinking models generate explicit reasoning tokens before emitting a tool call. Google validates these internal tokens across conversation turns via a cryptographic signature stored in `extra_content.google.thought_signature`. If an intermediary framework strips this payload, Google AI Studio rejects Turn 2 because the tool response cannot be cryptographically verified against the model's prior thought."*

---

# 👤 MEMBER 3: Ishaan Yadav (23/IT/073)
**Role:** Knowledge Systems, Evaluation & Integration Lead  
**Midterm Foundation:** Module 3 (BM25 Runbook RAG, Benchmarks, Interactive Dashboard & Evaluation)  
**Endterm Expansion:** Distributed Hybrid Architecture, Cloudflare Zero-Trust Tunnel, RFC Standards Grounding & Safe Remediation

---

### 3.1 Layman Explanation (The Story)
> *"In the midterm, I built a local library search engine using BM25 and a basic web dashboard that ran entirely on my own laptop.  
> For the endterm, I connected everything together into a distributed, real-world system. Because Harshit's Linux switches were running inside a VM on his Mac, I built a Hybrid Execution Driver that connects my dashboard on Windows to his VM over an encrypted Cloudflare tunnel across the internet. I upgraded our library to index official internet engineering standards (IETF RFCs) so the AI never guesses wrong CLI flags. Finally, I built a safe 'One-Click Fix' button so the human operator can approve the AI's repair command, and our system automatically pings the network to confirm 100% recovery."*

### 3.2 Technical Deep Dive (The Grilling Knowledge)
* **Distributed Hybrid Execution Driver (`src/sandbox/hybrid_driver.py`):**
  * In midterm, the dashboard talked directly to local Python memory.
  * In endterm, Ishaan engineered `HybridNetworkDriver`, implementing a dynamic proxy pattern:
    * Probes Harshit's bridge endpoint (`http://<IP>:8000/health`) with a 1.5s timeout.
    * If reachable $\rightarrow$ Operates in **`LIVE_KATHARA` 🟢** mode, routing pings, routes, and link inspections to real Docker containers over the Cloudflare tunnel.
    * If offline $\rightarrow$ Seamlessly falls back to **`LOCAL_SANDBOX` 🔵** mode (in-memory simulation), ensuring **zero demo-crash risk** during evaluation.
* **Cloudflare Zero-Trust QUIC Gateway Integration:**
  * Enabled remote cross-network demonstration across different Wi-Fi networks (e.g. Ishaan's home Wi-Fi to Harshit's Mac).
  * Exposes sub-100ms REST and WebSocket channels without requiring router port-forwarding or triggering NAT firewalls.
* **IETF RFC Domain Knowledge Grounding:**
  * Upgraded the BM25 retrieval engine ($k_1 = 1.5, b = 0.75$) with official IETF RFC playbooks:
    * **RFC 7938:** *Use of BGP for Routing in Large-Scale Data Centers* (Idle/Active state triage, ASN loop prevention).
    * **RFC 1191:** *Path MTU Discovery* (DF-bit packet drops and MTU mismatch diagnosis).
* **Glass-Box Mission Control UI & Safe Remediation:**
  * Upgraded `web/server.py` to FastAPI 2.0 with asynchronous WebSockets.
  * Streams raw agent ReAct thoughts, chosen tools, and CLI outputs live to the browser.
  * **One-Click Human-in-the-Loop Safe Remediation:**
    * Synthesizes exact Linux CLI commands (`ip link set eth1 up`).
    * Operator clicks **`[ 🚀 Approve & Apply Live Fix ]`**, which dispatches to the live container and automatically re-executes pingmesh to verify 0% packet loss.

### 3.3 Key Files Owned
* `src/rag/runbook_retriever.py` (Okapi BM25 ranking algorithm)
* `data/runbooks/` (`clos_bgp_troubleshooting.md`, `mtu_fragmentation_triage.md`)
* `src/sandbox/hybrid_driver.py` (Dynamic hybrid execution proxy)
* `web/server.py` & `web/static/` (`index.html`, `app.js`, `style.css`)
* `scripts/run_eval.py` & `benchmarks/benchmarks.json`

### 3.4 Rehearsed Viva Speaking Script (75 Seconds)
> *"Respected panel members, my name is Ishaan Yadav (Roll No: 23/IT/073). In the midterm, I presented Module 3, where I developed our native BM25 runbook retrieval engine, our 10-scenario benchmark suite, and our initial web dashboard.  
> For the endterm, I expanded our platform into a **Distributed Hybrid Architecture with IETF RFC Grounding and Closed-Loop Remediation**.  
> First, I developed the Hybrid Execution Driver. It dynamically probes Harshit's live Linux environment over a secure Cloudflare tunnel. When connected, all telemetry queries execute on real Docker containers; if offline, it transparently falls back to our deterministic local engine.  
> Second, I grounded our agent in official IETF standards—specifically indexing RFC 7938 for BGP Clos fabrics and RFC 1191 for Path MTU Discovery—completely eliminating CLI syntax hallucinations.  
> Third, I upgraded our mission-control dashboard to stream the agent's ReAct thoughts in real time via WebSockets. To make our system enterprise-safe, I implemented a human-in-the-loop remediation pipeline: once the fault is isolated, the operator approves the synthesized fix with one click, and our platform autonomously verifies 0% packet loss.  
> We will now demonstrate our live system on screen."*

### 3.5 Tough Questions & Answers for Ishaan
* **Q: "Why did you use BM25 instead of a Vector Database like Chroma or FAISS?"**
  * **Answer:** *"Dense embeddings map text to general semantic concepts, which frequently causes false matches on technical network tokens like `eth1`, `MTU 1400`, or `BGP Active`. BM25 is a probabilistic keyword matching algorithm that rewards exact technical term frequency while penalizing length. For structured network RFC runbooks, BM25 provides higher precision, zero GPU memory requirements, and deterministic sub-millisecond retrieval."*
* **Q: "Why do you require human approval before remediation?"**
  * **Answer:** *"In production data centers, autonomous write actions carry severe operational risk. If an unverified AI executes `reload` or restarts BGP sessions, it can trigger network-wide route flapping. Our architecture enforces 'Autonomous Diagnosis, Supervised Remediation'—the agent conducts the complex investigation, but the operator retains cryptographic control over state-altering commands."*

---

# ⏱️ 2. The 5-Minute Synchronized Viva Presentation Script

```text
[0:00 - 1:15]  Harshit Vaish:
               Problem context, transition from midterm NetworkX mock to live Linux Kernel VRF,
               Kathará multi-container BGP Clos fabric, and FastAPI bridge daemon.

[1:15 - 2:30]  Harshvardhan Kumar Arya:
               Evolution from basic ReAct prompt to FastMCP Topology Server, the Google Gemini
               thought_signature patch, and empirical proof of 34% latency reduction on NIKA.

[2:30 - 3:45]  Ishaan Yadav (Live Screen Demo):
               Show live Cloudflare hybrid connection -> Inject Link Drop (Link turns RED) ->
               Stream ReAct thoughts live over WebSockets -> BM25 RFC runbook match -> Pinpoint leaf1:eth1 down.

[3:45 - 4:30]  Ishaan Yadav & Team (Remediation & Recovery):
               Click 'Approve & Apply Live Fix' -> Dispatches `ip link set eth1 up` to container ->
               Automated pingmesh verification confirms 0% packet loss -> Link turns GREEN.

[4:30 - 5:00]  Harshit, Harshvardhan, Ishaan:
               Conclusion: Validated distributed cyber-physical system. Open for panel questions.
```

---

# 📊 3. Master Metrics & Standards Cheat Sheet

| Category | Metric / Specification | Value / Description |
| :--- | :--- | :--- |
| **Speedup** | Diagnostic Wall-Clock Latency | **42.5s vs 64.4s (⚡ 34.0% Faster)** |
| **Token Savings** | Prompt Input Tokens | **60,448 vs 66,524 (📉 9.1% Reduction)** |
| **Accuracy** | Root-Cause F1 (`rca_f1`) | **1.000 (100% Precision & Recall)** |
| **Reliability** | Entity Hallucinations | **0.0% (Zero non-existent devices)** |
| **Algorithm** | Topology Graph Search | **Pure stdlib BFS ($O(V + E)$ in $<1\text{ms}$)** |
| **Algorithm** | Domain Runbook Retrieval | **Okapi BM25 ($k_1 = 1.5, b = 0.75$)** |
| **Standards** | RFC 7938 | BGP in Large-Scale Data Centers (Clos Leaf-Spine) |
| **Standards** | RFC 1191 | Path MTU Discovery & DF Packet Fragmentation |
| **Standards** | RFC 792 | Internet Control Message Protocol (ICMP) |
