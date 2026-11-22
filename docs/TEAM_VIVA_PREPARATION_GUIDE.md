# 🎓 Master Viva Preparation Guide & 3-Way Project Breakdown
## Topology-Aware Tool-Using LLM Agent for Automated Network Fault Diagnosis
**Delhi Technological University (DTU) — Department of Information Technology**  
**B.Tech Project-I (7th Semester)**

---

# 📖 TABLE OF CONTENTS
1. [PART 1: The Master Story (EVERY Teammate Must Know This)](#part-1-the-master-story-everyone-must-know-this)
2. [PART 2: Teammate 1 (Harsh) — Ground-Truth Emulation, Kernel VRF & Cloud Bridge](#part-2-teammate-1-harsh--network-substrate--infrastructure)
3. [PART 3: Teammate 2 — Topology MCP Engine, Protocol Engineering & Benchmarking](#part-3-teammate-2--topology-mcp-engine-protocol-engineering--benchmarking)
4. [PART 4: Teammate 3 (Ishaan) — Cognitive Control-Plane, BM25 RAG & Mission Control UI](#part-4-teammate-3-ishaan--cognitive-control-plane-bm25-rag--mission-control-ui)
5. [PART 5: The 5-Minute Coordinated Viva Script & Demo Playbook](#part-5-the-5-minute-coordinated-viva-script--demo-playbook)
6. [PART 6: Master Cheat Sheet (Quick Numbers, Formulas & RFCs)](#part-6-master-cheat-sheet-quick-numbers-formulas--rfcs)

---

# PART 1: The Master Story (Everyone Must Know This)
*Every team member must be able to recite this 2-minute elevator pitch from memory if the examiner suddenly points at them.*

### 1.1 The Real-World Problem in Plain English
Imagine a modern cloud data center (like Google, Amazon AWS, or Microsoft Azure). Inside, thousands of computers are connected in a multi-tier hierarchy called a **Clos Leaf-Spine topology**. Switches constantly talk to each other using complex routing protocols like **BGP (Border Gateway Protocol)**.

When something breaks—a fiber optic cable is cut, a port drops to 1400 MTU, or a BGP neighbor times out—traffic suddenly stops. 
* **Today's Status Quo:** Human Network Operations Center (NOC) engineers spend **hours** reading logs, running `traceroute`, and guessing which switch is broken.
* **Why Basic AI Fails:** If you just give ChatGPT or Gemini standard terminal tools (`ping`, `traceroute`), it acts like a **blindfolded monkey**. It doesn't know how the switches are wired together! It tries random pings across all 10 devices, burns thousands of tokens, hits rate limits, and takes minutes to find simple cable drops.

### 1.2 Our Solution: The 3-Pillar Autonomous Diagnostic System
We built an autonomous, distributed, closed-loop network diagnostic platform composed of three engineering layers:

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                           THE THREE SYSTEM PILLARS                                │
├───────────────────────────────┬───────────────────────────┬───────────────────────┤
│    PILLAR 1: SUBSTRATE        │     PILLAR 2: REASONING   │  PILLAR 3: CONTROL    │
│    (Teammate 1 - Harsh)       │     (Teammate 2)          │  (Teammate 3 - Ishaan)│
├───────────────────────────────┼───────────────────────────┼───────────────────────┤
│ • Real Linux Kernel VRF       │ • Pure BFS FastMCP Server │ • WebSocket Dashboard │
│ • FRRouting BGP Kathará Nodes │ • Thought Signature Patch │ • BM25 RFC Runbook RAG│
│ • FastAPI Bridge Daemon       │ • NIKA Comparative Eval   │ • Hybrid Driver       │
│ • Cloudflare Zero-Trust Tunnel│ • -34.0% Latency Drop     │ • 1-Click Remediation │
└───────────────────────────────┴───────────────────────────┴───────────────────────┘
```

1. **Realistic Emulation Substrate (Harsh):** A live data center fabric running real Linux network namespaces, kernel VRF, and live FRRouting BGP routing daemons inside Docker containers on an ARM64 Ubuntu VM, bridged securely over a Cloudflare tunnel.
2. **Topology-Aware MCP Engine (Teammate 2):** A standardized Model Context Protocol (MCP) server providing graph-awareness primitives (`list_devices`, `list_neighbours`, `find_path`), powered by Google Gemini 3.5 Flash Lite with an in-house serialization patch.
3. **Cognitive Control-Plane & Mission Control (Ishaan):** An interactive WebSocket visualizer, grounded by an Okapi BM25 RAG engine indexing IETF RFC specifications, featuring human-in-the-loop one-click safe remediation.

### 1.3 The Grand Empirical Takeaway
When tested on identical network fault scenarios in the benchmark:
* **Diagnosis Speed:** Cut wall-clock diagnostic time from **64.4s down to 42.5s** (a **34.0% speedup**).
* **Token Efficiency:** Reduced input tokens by **9.1%** and output tokens by **17.5%**.
* **Diagnostic Precision:** **100% Root-Cause F1 score** and **0.0% entity hallucinations**.

---

# PART 2: Teammate 1 (Harsh) — Network Substrate & Infrastructure
**Role:** Systems & Infrastructure Engineer  
**Core Responsibility:** Ground-Truth Emulation Substrate, Linux Kernel VRF, BGP Clos Fabric, and Live Cloud Gateway.

---

### 2.1 The Layman Analogy (What to tell your family)
> *"I built the physical city and the roads. Before an AI can practice being a traffic police officer, you need real roads with real traffic lights that actually turn red and green. Because my Mac couldn't run Linux kernel network namespaces natively, I set up an ARM64 Ubuntu virtual machine, spawned multiple virtual network switches running enterprise BGP routing software, and built an encrypted bridge over the internet so my teammates could control my virtual switches from anywhere in the world."*

### 2.2 Technical Deep Dive (What to tell the Professor)
Harsh owns everything below the application layer:
1. **Linux Kernel Virtual Routing & Forwarding (VRF):**
   * macOS Darwin kernel does not support Linux network namespaces (`netns`) or the `vrf` kernel subsystem.
   * Harsh configured an **Ubuntu 26.04 LTS (aarch64)** virtual machine inside UTM on Apple Silicon.
   * Kernel VRF isolates routing tables per interface, preventing routing leakage across the multi-tenant Clos leaf-spine fabric.
2. **Kathará & Docker Multi-Container Architecture:**
   * Built a 2-Spine, 4-Leaf, 4-Host Clos fabric (`dc_clos`).
   * Spines (`spine1`, `spine2`) and Leaves (`leaf1`–`leaf4`) run **FRRouting (FRR)** daemons (`bgpd`, `zebra`).
   * BGP Peering: eBGP configuration with ASN 65001–65006, exchanging IPv4 loopback and interface prefixes over `/30` subnets.
   * Hosts (`host1`–`host4`) run containerized Linux with static default gateways pointing to their access leaf switch.
3. **On-Line LVM Storage Expansion:**
   * Docker image compilation (`nika/onos`, `nika/base`, `nika/frr`) exhausted the initial 12 GB virtual disk.
   * Dynamically expanded the root volume without reinstallation using Logical Volume Manager:
     ```bash
     sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
     sudo resize2fs /dev/ubuntu-vg/ubuntu-lv
     ```
     Expanded capacity from 12 GB to 24 GB while preserving all cached container layers.
4. **Live Hybrid Bridge Daemon (`src/nika_bridge_api.py`):**
   * High-performance FastAPI server running on port 8000 inside the VM.
   * Exposes REST endpoints:
     * `GET /health`: Heartbeat reporting active Kathará substrate.
     * `GET /api/topology`: Returns live nodes and link states from Kathará JSON metadata.
     * `POST /api/exec`: Dispatches commands via `docker exec <container> <cmd>`.
     * `POST /api/fault/inject`: Dynamically triggers interface drops (`ip link set eth1 down`), BGP session teardowns (`vtysh`), MTU reductions (1400), or netem jitter/packet loss (`tc qdisc`).
     * `POST /api/remediate`: Executes the synthesized fix and validates recovery via host ping.
5. **Cloudflare Zero-Trust Tunnel:**
   * Used `cloudflared` to establish an outbound QUIC tunnel (`trycloudflare.com`) from localhost:8000 to Cloudflare edge data centers.
   * Circumvents NAT, router firewall rules, and college Wi-Fi client isolation without opening insecure inbound router ports.

### 2.3 Key Code Files Owned
* `src/nika_bridge_api.py` (FastAPI bridge service)
* `/home/harsh_linux/nika/scenarios/dc_clos/` (Kathará topology and FRR configuration scripts)
* `docs/HARSH_CODEBASE_GUIDE.md`

### 2.4 Tough Examiner Questions & Bulletproof Answers

* **Q1: "Why did you use Kathará containers instead of Mininet?"**
  * **Answer:** *"Mininet runs processes inside lightweight network namespaces on a single shared host kernel and uses Open vSwitch. It does not provide realistic L3 enterprise routing protocol stacks. Kathará provides isolated Docker containers running authentic enterprise network daemons—specifically FRRouting running genuine BGP, OSPF, and zebra daemons. In our Clos setup, each switch has independent routing tables, interface buffers, and administrative domains."*

* **Q2: "What happens if a link goes down in your BGP fabric?"**
  * **Answer:** *"When `leaf1:eth1` is set down, the physical carrier is lost. FRR's `zebra` daemon detects the interface state change and informs `bgpd`. BGP withdraws the prefix advertised to `spine1` using a BGP UPDATE message. Traffic from `host1` destined to `host3` must now failover to `spine2` via Equal-Cost Multi-Path (ECMP). If both paths fail, ping returns 100% packet loss, triggering our diagnostic agent."*

* **Q3: "How does your Cloudflare tunnel differ from standard port forwarding?"**
  * **Answer:** *"Standard port forwarding requires administrative access to the physical Wi-Fi router to map public IP WAN ports to local LAN IP ports, which is impossible on institutional campus networks with carrier-grade NAT (CGNAT). Cloudflare Tunnel initiates an outbound encrypted TLS/QUIC connection to Cloudflare's nearest edge server (del06 in our logs). Cloudflare routes incoming requests down the tunnel to `localhost:8000`, completely bypassing inbound firewall restrictions."*

---

# PART 3: Teammate 2 — Topology MCP Engine, Protocol Engineering & Benchmarking
**Role:** Protocol & AI Reasoning Engineer  
**Core Responsibility:** Model Context Protocol (MCP) Topology Server, LLM Serialization Patching, and Empirical Benchmarking.

---

### 3.1 The Layman Analogy (What to tell your family)
> *"I gave the AI eyes and a GPS map, and I fixed a secret bug inside Google's communication system. Without me, the AI had to guess which switch connected to which switch by asking blind questions. I wrote a tool that instantly tells the AI the network map using shortest-path math. I also solved a critical software bug where Google's newest AI was crashing every time it tried to think twice, and I ran the official tests proving our method is 34% faster."*

### 3.2 Technical Deep Dive (What to tell the Professor)
Teammate 2 owns the interface between the LLM and the network:
1. **Model Context Protocol (MCP) Topology Server (`src/topology_server.py`):**
   * Built on Anthropic's open **Model Context Protocol (MCP)** specification using `FastMCP`.
   * Standardizes tool discovery and execution for LLM agents via JSON-RPC.
   * Exposes three strictly read-only tools:
     * `list_devices()`: Returns all network nodes and architectural roles (`spine`, `leaf`, `host`).
     * `list_neighbours(device_id)`: Returns physical layer adjacencies and link types (`fabric` vs `access`).
     * `find_path(source, destination)`: Calculates all shortest topological paths using **Breadth-First Search (BFS)** traversal.
   * **Zero-Dependency Standard Library Implementation:** Designed with pure Python `collections.deque` and graph adjacencies. Zero external C-dependencies (no NetworkX or SciPy), allowing it to boot in $<1\text{ms}$ with zero memory overhead inside isolated sandbox environments.
2. **Reverse-Engineering the Google Gemini "Thought Signature" Bug:**
   * **The Error:** Multi-turn tool execution with Google Gemini 3.5 Flash Lite failed on Turn 2 with:
     ```text
     BadRequestError: 400 Function call is missing a thought_signature in functionCall parts
     ```
   * **Root Cause Analysis:** Google's Gemini 3.x thinking models generate an internal cryptographic token (`extra_content.google.thought_signature`) along with the tool call. LangChain's OpenAI client adapter stripped this field during serialization when converting dictionary messages back into OpenAI-compatible payload schemas. When Turn 2 sent the conversation history back to Google AI Studio, Google rejected it because the expected thought signature was missing.
   * **The Solution (`src/thought_signature_patch.py`):** Authored an in-memory monkey-patch intercepting `_convert_dict_to_message` and `_lc_tool_call_to_openai_tool_call` in `langchain_openai.chat_models.base`. The patch preserves `extra_content` throughout the ReAct loop, unlocking stable multi-turn diagnosis.
3. **NIKA Benchmark Comparative Evaluation:**
   * Integrated our MCP server into the **NIKA benchmark** (`sands-lab/nika`) registry (`src/nika/mcp/registry.py`) controlled by the environment switch `ENABLE_TOPOLOGY_TOOL=1`.
   * Executed rigorous comparative evaluation across identical Clos network scenarios:
     * **Version (b) [Baseline]:** Standard diagnostic tools only (`exec_shell`, `pingmesh`, `packet_capture`). No topology knowledge.
     * **Version (c) [Proposed]:** Standard diagnostic tools + `topology_mcp_server`.

### 3.3 Key Empirical Results Table (Memorize These Exact Numbers!)

| Metric | Version (b): Baseline | Version (c): Topology-Aware | Performance Delta |
| :--- | :---: | :---: | :---: |
| **RCA Accuracy / F1 (`rca_f1`)** | 1.000 (100%) | 1.000 (100%) | **Parity (Both 100% Correct)** |
| **Localization Precision / Recall** | 1.000 | 1.000 | **Parity (Exact Link Pinpointed)** |
| **Wall-Clock Latency** | 64.4 seconds | **42.5 seconds** | **⚡ -21.9s (-34.0% Faster)** |
| **Input Tokens** | 66,524 | **60,448** | **📉 -6,076 (-9.1% Reduction)** |
| **Output Tokens** | 1,123 | **926** | **📉 -197 (-17.5% Reduction)** |
| **Reasoning Decision Steps** | 15 steps | **14 steps** | **-1 Step** |
| **Total Tool Calls** | 14 calls | **13 calls** | **-1 Tool Call** |
| **Tool Execution Errors** | 0 errors | **0 errors** | **Zero crash rate** |

### 3.4 Key Code Files Owned
* `src/topology_server.py` (FastMCP pure stdlib server)
* `src/thought_signature_patch.py` (LangChain monkey-patch)
* `results/version_b_smoke_test.json` & `results/version_c_smoke_test.json`
* Benchmark hooks in `registry.py`

### 3.5 Tough Examiner Questions & Bulletproof Answers

* **Q1: "Why did you implement BFS yourself instead of using NetworkX?"**
  * **Answer:** *"In production container environments and isolated network sandboxes, downloading external heavy wheels like NetworkX via pip can fail due to offline proxy policies or dependency conflicts. A leaf-spine Clos network is an unweighted bidirectional graph. Standard library BFS using `collections.deque` achieves optimal $O(V + E)$ time complexity, executes in microseconds, and requires zero external pip dependencies."*

* **Q2: "Does giving the agent the topology leak ground truth about the failure?"**
  * **Answer:** *"Absolutely not. The topology server provides static structural context—it reports the architectural cabling schematic (e.g., `leaf1` has links to `spine1` and `spine2`). It has zero access to runtime telemetry. It does not know whether an interface is administratively UP or DOWN, whether packets are dropping, or if BGP is peering. The agent must still actively interrogate the switches using CLI tools to discover the fault."*

* **Q3: "Why did input tokens decrease by 9.1% if you added extra topology tools?"**
  * **Answer:** *"Because without topology awareness, the baseline agent had to discover the path empirically. It ran repeated traceroutes and pings across arbitrary nodes, polluting the conversation context with verbose CLI routing tables and packet dumps. The topology-aware agent issued a single `find_path` query, immediately localized the candidate devices between source and destination, and focused its tool calls only on the relevant nodes—eliminating irrelevant terminal outputs from the prompt window."*

---

# PART 4: Teammate 3 (Ishaan) — Cognitive Control-Plane, BM25 RAG & Mission Control UI
**Role:** Cognitive Systems & Full-Stack Interface Engineer  
**Core Responsibility:** WebSocket Mission Control UI, BM25 RFC Runbook RAG, Hybrid Driver, and One-Click Remediation.

---

### 4.1 The Layman Analogy (What to tell your family)
> *"I built the cockpit, the flight manual library, and the emergency buttons. When an airplane has an engine warning, the pilot doesn't want to type raw computer code into a black screen; they want an instrument panel that turns red, shows what's wrong, pulls up the official Boeing manual, and gives them a button to fix it. I built the interactive website that visualizes our switches, streams the AI's thoughts live, looks up official internet engineering rules, and lets the teacher click one button to fix the network and watch it turn green."*

### 4.2 Technical Deep Dive (What to tell the Professor)
Teammate 3 owns the cognitive plane, knowledge retrieval, and human-in-the-loop interface:
1. **Glass-Box Mission Control Dashboard (`web/server.py` & `web/static/`):**
   * Built using **FastAPI 2.0**, WebSockets, HTML5 Canvas, and modern CSS glassmorphism.
   * **Real-Time Streaming ReAct Visualizer:** Streams the LLM's raw reasoning steps (`Thought` $\rightarrow$ `Action` $\rightarrow$ `Observation`) over WebSockets turn-by-turn. The examiner watches the AI "think" live on screen instead of waiting for a batch result.
   * **Interactive Network Canvas:** Renders nodes (spines, leaves, hosts) with dynamic color-coded link states (Green = Operational, Red = Fault/Down, Amber = Packet Loss).
2. **Dual-Substrate Hybrid Execution Driver (`src/sandbox/hybrid_driver.py`):**
   * Implements a universal proxy pattern wrapping `NetworkSandbox`.
   * **Active Remote Probing:** On startup, dynamically queries Harsh's Cloudflare bridge endpoint (`GET /health`).
   * **Automated Mode Switching:**
     * If Harsh's tunnel is online $\rightarrow$ Operates in **`LIVE_KATHARA` 🟢** mode, dispatching real pings, traceroutes, and faults to real Linux containers.
     * If the tunnel drops or Wi-Fi fails $\rightarrow$ Transparently falls back to **`LOCAL_SANDBOX` 🔵** mode (in-memory deterministic simulation), ensuring **zero demo-crash risk** during the viva!
3. **Domain Knowledge Grounding via Okapi BM25 RAG:**
   * General LLMs frequently hallucinate nonexistent CLI flags or forget Clos BGP state machines.
   * Indexed official **IETF RFC troubleshooting runbooks** inside `data/runbooks/`:
     * `clos_bgp_troubleshooting.md`: Encodes **RFC 7938** (Use of BGP in Large Data Centers), detailing Idle/Active states, peer loopbacks, and prefix advertisements.
     * `mtu_fragmentation_triage.md`: Encodes **RFC 1191** (Path MTU Discovery) and DF-bit fragmentation drop signatures.
   * Integrated an **Okapi BM25 retrieval engine**. When telemetry reveals BGP neighbor loss or packet drops, the top-$k$ relevant RFC operational procedures are dynamically injected into the LLM system prompt.
4. **Closed-Loop Safe Remediation Pipeline:**
   * Identifies that automated agents should **diagnose autonomously but remediate with human supervision** to prevent catastrophic routing flaps.
   * Once root cause is pinpointed, the agent synthesizes the remediation command (e.g., `ip link set eth1 up` or `vtysh -c 'router bgp 65001' ...`).
   * The UI displays an alert card with the exact proposed CLI command and an **`[ 🚀 Approve & Apply Live Fix ]`** button.
   * Clicking the button dispatches `POST /api/remediate` to Harsh's container, applies the fix, immediately triggers a post-repair pingmesh, and confirms **0% packet loss** with all links turning green.

### 4.3 Key Code Files Owned
* `src/sandbox/hybrid_driver.py` (Hybrid execution driver)
* `web/server.py` (FastAPI backend with WebSocket streaming)
* `web/static/index.html`, `app.js`, `style.css` (Frontend visualizer)
* `data/runbooks/` (`clos_bgp_troubleshooting.md`, `mtu_fragmentation_triage.md`)

### 4.4 Tough Examiner Questions & Bulletproof Answers

* **Q1: "Why did you use BM25 instead of a Vector DB with Dense Embeddings (like Chroma or FAISS)?"**
  * **Answer:** *"Dense vector embeddings are trained on semantic prose and struggle with exact keyword matching for technical networking tokens like `eth1`, `MTU 1400`, `Active/Idle`, or CLI error codes. Okapi BM25 uses probabilistic term frequency-inverse document frequency (TF-IDF) saturation. For structured RFC runbooks, BM25 provides superior exact-keyword retrieval with zero GPU embedding latency, zero vector DB memory footprint, and deterministic ranking."*

* **Q2: "What happens if Harsh's laptop shuts down during the live presentation?"**
  * **Answer:** *"Our system has built-in enterprise resilience. The `HybridNetworkDriver` checks the health endpoint with a 1.5-second timeout. If the remote connection times out, it immediately logs a fail-safe event and falls back to our local in-memory simulation engine. The examiner demo continues seamlessly with zero crash risk."*

* **Q3: "Why is Human-in-the-Loop necessary for remediation?"**
  * **Answer:** *"In autonomous systems, remediation carries operational risk. An unverified agent could execute `reload` or misconfigure BGP route-maps, causing network-wide routing loops or route flapping across neighboring autonomous systems. Our architecture enforces a 'Dual-Key' safety model: the agent conducts the exhaustive, complex investigation, but the final state-altering write operation requires explicit human cryptographic authorization."*

---

# PART 5: The 5-Minute Coordinated Viva Script & Demo Playbook
*Follow this exact schedule during your project demonstration. Practice this with a stopwatch!*

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        5-MINUTE PRESENTATION TIMELINE                  │
├─────────┬──────────────────────┬───────────────────────────────────────┤
│ TIME    │ SPEAKER              │ ACTION ON SCREEN                      │
├─────────┼──────────────────────┼───────────────────────────────────────┤
│ 0:00    │ Harsh (Teammate 1)   │ Slides / Architecture Diagram         │
│ 1:15    │ Teammate 2           │ Benchmark Comparison Table & Code     │
│ 2:30    │ Ishaan (Teammate 3)  │ Live Web Dashboard (Fault Injection)  │
│ 3:45    │ Ishaan & Team        │ ReAct Stream -> One-Click Remediation │
│ 4:30    │ All Members          │ Summary, Future Scope & Viva Q&A      │
└─────────┴──────────────────────┴───────────────────────────────────────┘
```

### [0:00 – 1:15] — Teammate 1: Harsh (Infrastructure & Problem Setup)
* **What Harsh says:**  
  *"Respected examiners, good morning. Our B.Tech project is **'Topology-Aware Tool-Using LLM Agent for Automated Network Fault Diagnosis'**.  
  Modern data centers run multi-tier Clos leaf-spine topologies. When unannounced link drops, BGP routing blackholes, or MTU mismatches occur, human diagnosis takes hours.  
  To solve this with real ground truth, I built an ARM64 Linux emulation environment using Kathará and Docker containers running the Linux kernel VRF subsystem and live FRRouting BGP daemons. To allow distributed collaboration, I created a FastAPI bridge daemon connected over a secure Cloudflare tunnel. Now, my teammate will explain how we gave the LLM structural topological awareness."*

### [1:15 – 2:30] — Teammate 2: (MCP Engine & Empirical Results)
* **What Teammate 2 says:**  
  *"Standard LLMs troubleshoot networks blindly by trial-and-error. We engineered a Model Context Protocol (MCP) Topology Server that provides read-only graph intelligence using standard-library Breadth-First Search (BFS).  
  During development, we also resolved an industry protocol incompatibility: Google Gemini 3.x thinking models return a cryptographic `thought_signature` that LangChain stripped during tool calling, causing 400 Bad Request crashes. We authored a runtime serialization patch preserving this signature across multi-turn reasoning loops.  
  When evaluated on the NIKA benchmark, our topology-aware agent achieved a **34% wall-clock latency reduction**, saved **9.1% input tokens**, and achieved **100% root-cause accuracy**. Now, Ishaan will demonstrate the live mission control dashboard."*

### [2:30 – 3:45] — Teammate 3: Ishaan (Live Demo: Fault Injection & Streaming ReAct)
* **What Ishaan does:** Opens `http://localhost:8000` on the projector.
* **What Ishaan says:**  
  *"This is our Glass-Box Mission Control Dashboard. Notice our hybrid status pill at the top: it is currently connected in real time over the Cloudflare tunnel to Harsh's live Linux containers.*  
  *(Action: Select `NET-SCN-001: Core Switch Trunk Link Drop` $\rightarrow$ Click **'Inject Fault'**)*  
  *We have injected a silent link failure on `spine1-eth1`. The link turns RED on our canvas, and host pingmesh drops to 100% packet loss.*  
  *(Action: Click **'Run Diagnostic Agent'**)*  
  *Watch the screen: over WebSockets, the Gemini agent is streaming its thoughts live. Instead of guessing random devices, it queries `find_path(host1, host3)`, localizes the path to `leaf1-spine1`, retrieves the RFC 7938 BGP troubleshooting runbook using our BM25 engine, and inspects `leaf1:eth1` with `ip link`. In just two steps, it confirms that `leaf1:eth1` is administratively DOWN!"*

### [3:45 – 4:30] — Teammate 3 & Team (One-Click Remediation & Verification)
* **What Ishaan does:** Points to the Root Cause Alert Card on screen.
* **What Ishaan says:**  
  *"The agent has synthesized the exact remediation command: `ip link set eth1 up`. Following our safety protocol of human-in-the-loop validation, I will now click **'Approve & Apply Live Fix'**.*  
  *(Action: Clicks the button)*  
  *The command is dispatched over the tunnel to Harsh's Docker container. The system autonomously triggers an immediate verification pingmesh. Look at the canvas: the link returns to GREEN, packet loss drops to 0%, and the incident is marked Resolved in under 45 seconds."*

### [4:30 – 5:00] — Team Conclusion
* **Harsh concludes:**  
  *"To summarize: we combined authentic Linux kernel emulation, MCP graph algorithms, RFC domain knowledge retrieval, and human-supervised remediation into a working, distributed cyber-physical system. Thank you, and we welcome your questions."*

---

# PART 6: Master Cheat Sheet (Quick Numbers, Formulas & RFCs)
*Keep this page printed or open on your phone before stepping into the viva room!*

### 🔑 Critical Acronyms
* **MCP:** Model Context Protocol (open protocol for exposing tools and prompts to LLMs via JSON-RPC).
* **VRF:** Virtual Routing and Forwarding (creates virtual routers with isolated routing tables in Linux kernel).
* **Clos Fabric:** Multi-stage switching network designed by Charles Clos (Leaf-Spine architecture used in cloud datacenters).
* **FRR:** FRRouting (open-source Linux routing protocol suite; runs `bgpd`, `ospfd`, `zebra`).
* **ECMP:** Equal-Cost Multi-Path routing (distributes packets across multiple spine switches).
* **BM25:** Best Matching 25 (probabilistic TF-IDF retrieval ranking algorithm).
* **ReAct:** Reasoning + Acting (prompting paradigm interleaving `Thought`, `Action`, and `Observation`).

### 📚 Official IETF Standards Used
* **RFC 7938:** *Use of BGP for Routing in Large-Scale Data Centers* (Standard Clos leaf-spine design).
* **RFC 1191:** *Path MTU Discovery* (Detection of fragmentation drops and ICMP Type 3 Code 4).
* **RFC 792:** *Internet Control Message Protocol (ICMP)* (Ping echo request/reply specification).

### 🔢 Exact Benchmark Metrics to Quote
* **34.0% Latency Reduction** (from 64.4s down to 42.5s).
* **9.1% Input Token Savings** (from 66,524 down to 60,448 tokens).
* **17.5% Output Token Savings** (from 1,123 down to 926 tokens).
* **100% Root-Cause F1 (`rca_f1: 1.000`)** across all benchmark runs.
* **0.0% Hallucinations** (Zero nonexistent device names generated).
* **$O(V + E)$ Time Complexity** for BFS shortest path calculation.
