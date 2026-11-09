# 🚀 RELAY — Evidence-Linked Knowledge Handover Platform

> **CodersInPune Hackathon 2026 • Round 2 (The Build)**  
> **Team:** SoloStack (Solo Developer Track)  
> **Author:** Anshika Aggarwal (B.Tech 1st Year, Dr. Akhilesh Das Gupta Institute of Professional Studies - ADGIPS, New Delhi)  
> **Track:** Knowledge Handover & Project Continuity  

---

## 📌 Executive Summary

When developers, team leads, or student coordinators leave a project, the vital tacit context—why architectural decisions were made, which dependencies are fragile, what unresolved blockers linger, and who owns key components—disappears with them.

**Relay** is a lightweight, high-trust knowledge-handover platform engineered to reconstruct project reality from authorized artifacts (git commits, PR threads, task boards, and team notes). Rather than generating unreliable AI summaries, Relay enforces **bi-directional evidence citations**, explicitly flags uncertainty and contradictions, and incorporates a **human-in-the-loop review canvas** before producing role-tailored onboarding packages for incoming developers and leads.

---

## ⚡ Quick-Start for Judges (Run in 10 Seconds)

### Option 1: Instant Browser Evaluation (Zero-Install)
Simply open `frontend/index.html` directly in any web browser (Google Chrome, Microsoft Edge, Safari, Firefox).  
* Features an **Autonomous In-Browser State Engine** with built-in benchmark data, letting you evaluate all 5 stages end-to-end without touching a terminal!

### Option 2: Full-Stack Local Server (FastAPI + React)
```bash
# 1. Clone repository
git clone https://github.com/Anshika-Aggarwal/relay-knowledge-handover.git
cd relay-knowledge-handover

# 2. Run the unified FastAPI server
python backend/app/main.py
```
* **Interactive Web App:** Open [http://localhost:8000](http://localhost:8000)
* **Interactive Swagger API Docs:** Open [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔄 The Central Workflow (The 5-Stage Transition Engine)

```
[01. CONNECT]    Upload Git commit logs, PR discussions, Task markdown, and standup notes.
       │         (Pre-ingestion regex filter redacts API keys, tokens, and secrets)
       ▼
[02. RECONSTRUCT] FastAPI backend invokes Google Gemini 1.5 Flash structured JSON schema:
       │         • Architectural Decisions  • Fragile Gotchas  • Blockers  • Ownership
       ▼
[03. VERIFY]     Verification Engine anchors each claim to an exact source excerpt [PR #14].
       │         Flags temporal contradictions (e.g. task marked Done, but commit rolled back).
       ▼
[04. REVIEW]     Dual-Pane Interactive Review Canvas (React + Tailwind):
       │         Left pane: Raw Source Snippets  |  Right pane: Editable Handover Cards.
       │         The departing developer reviews, adjusts flags, and locks the handover.
       ▼
[05. HANDOVER]   Generates Role-Tailored Onboarding Packages:
                 • Developer View: Code architecture, setup quirks, and Day-1 task list.
                 • Lead View: Milestones, risk matrix, and external stakeholder directory.
```

---

## 🛠️ Technology Stack & Architecture

| Layer | Technology | Purpose in Relay |
| :--- | :--- | :--- |
| **Frontend** | React 18, Tailwind CSS, Lucide Icons | Responsive 5-stage stepper, dual-pane review canvas, and role switcher. |
| **Backend API** | Python, FastAPI, Pydantic v2 | Asynchronous REST endpoints with auto-generated OpenAPI documentation. |
| **Database** | SQLite + SQLAlchemy ORM | Zero-config, deterministic local database for 100% evaluation reliability. |
| **AI Extraction** | Google Gemini 1.5 Flash API | 1M+ token context window ingests full commit histories without chunk loss. |
| **Fallback Engine** | Deterministic Semantic Analyzer | Guarantees instant sub-second responses even during API outages/rate limits. |
| **Security** | Python Regex Sanitizer | Intercepts and scrubs API keys, Bearer tokens, and passwords prior to display. |

---

## 🌟 3 Substantial Improvements Committed for Round 3

1. **Cross-Source Temporal Timeline Slider:** An interactive chronological scrub bar that displays when decisions were made across all sources on a synchronized timeline (Discord &rarr; Task Card &rarr; Git Commit).
2. **Cryptographic Handover Seal & Tamper-Proof Audit Manifest:** Generates an immutable SHA-256 hash upon approval and produces a cryptographically signed handover dossier.
3. **Interactive Handover Q&A Agent with Strict Citation Guardrails:** Embedded conversational assistant for incoming developers, strictly restricted via RAG to cite only verified claims from the sealed handover manifest.

---

## 📄 Submission Files

* **Round 1 Proposal PDF:** [`SoloStack_Anshika_Aggarwal_Round1_Proposal.pdf`](SoloStack_Anshika_Aggarwal_Round1_Proposal.pdf)
* **Round 2 Project Documentation PDF:** [`SoloStack_Round2_Project_Documentation.pdf`](SoloStack_Round2_Project_Documentation.pdf)
* **Live Demo / Web Client:** [`frontend/index.html`](frontend/index.html)
* **FastAPI Backend Entrypoint:** [`backend/app/main.py`](backend/app/main.py)
