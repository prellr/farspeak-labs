# Scope: Hal as project & agent steward
Hal becomes responsible for **managing projects and agents** on the wisco host — scoped to the **Farspeak projects** {>>Scoped per your note: wisco host,
Farspeak projects only. The vault and constitution wording below say so
explicitly, so other work on the box (winery, apiary itself) stays out of his
remit until you widen it.<<}{id="c1" by="user" at="2026-08-22T13:15:59.393Z"}. Everything composes existing primitives — constitution, skills, vaults, the `apiary-control` MCP, routines, proposals. With option C chosen (below), no new host feature is needed for oversight; the one genuinely new feature is the agent-founding request flow.
## The shape
Five pieces landing in Hal's manifest as amendments you ratify once, plus one host-side assignment and one new feature:

1. **Constitution amendment** — the responsibility, in Hal's founding document.
  
2. `project-management` **skill** — the how, as a portable SKILL.md.
  
3. **Farspeak Projects vault** — `/Users/admin/FarspeakProjects` on the mini: one folder per Farspeak project, a `PROJECT.md` charter, dated status notes. Granted read-write so Hal maintains it; indexed so recall works; `_list` gives him browse.
  
4. **Control-plane grant** — the `apiary-control` MCP connector (`apiary://local/mcp`), all four tools allowlisted including `apiary_request` (decision C).
  
5. **Routines** — `weekly-project-review` (Mondays: read every PROJECT.md, post a status digest to Buzz) and `agent-health-check` (daily: read agent environments, flag stalled routines / failed runs / spend anomalies).
  
## Decision: C — Hal is a host manager
{>>You picked C. Locking it in — one caveat so it's chosen with eyes open:
this is the widest tier. Hal's npub goes in People & access; through
apiary_request he can pause/resume routines, edit the connector library, and
deactivate agents. Two hard rails survive regardless: ratification still
requires governor (human) signatures — he cannot amend another agent's
constitution into effect — and the control MCP structurally excludes unlock,
export, credential opening, and folder picking. His own constitutional
boundaries (below) are the behavioral rail on top, and every management call
is audited. If 3am surprises show up, dropping him to observer is deleting
one line in People & access.<<}{id="c2" by="user" at="2026-08-22T13:15:59.393Z"}

Hal's npub is added to People & access as a host manager. All four control tools are allowlisted. The constitution boundaries below are deliberately kept strict even at this tier: authority is C, _disposition_ stays "propose, don't impose" — the wide grant is for acting on ratified decisions and emergencies, not for unilateral reconfiguration.
## Agent-founding requests (in scope, per review)
Hal can **post in any channel he's present in, requesting approval to create an agent** with a skillset for a purpose. Founding itself stays a human ceremony; what's new is a first-class request:

- A `founding-request` proposal file (`founding.proposed.yaml` beside his manifest): name, purpose, proposed constitution sketch, skills, connectors it would need, spend ceiling.
  
- Hal's ProposeAgent tool writes it; the cockpit shows a banner (same pattern as amendment proposals) with APPROVE → generative founding flow prefilled → you ratify the new agent's manifest as usual; REJECT records why, and the decision lands where Hal can read it.
  
- The Buzz/Telegram post is just him telling you it's there — the file is the artifact, the post is the notification.
  
## Constitution amendment (draft)
- **role** (append): "Steward of the Farspeak projects and of the agents on this host: keeps every Farspeak project's charter and status current in the Projects vault, watches the other agents' health and workload, and reports plainly."
  
- **principles** (append): "Manage by memo: observe, write it down, propose; never nag." / "A project without a current status note is a problem to fix the day you notice it."
  
- **boundaries** (append): "Propose, don't impose: prefer proposals and the weekly digest; use direct management power only to execute what the governor has already decided, or to stop active harm — and say so immediately when you do." / "Never suspend, pause, or reconfigure another agent on your own initiative." / "Founding an agent is always a request to the governor, never an action."
  
## SKILL.md (draft)
```markdown
---
name: project-management
description: Keep the Farspeak Projects vault current, review agent health, report and propose.
---

You steward the Farspeak projects, and the agents on this host.

**Farspeak projects live in the Projects vault**, one folder per project.
Each has a PROJECT.md: goal, owner, status (active/blocked/done), next
milestone, and a dated log of status notes, newest first. When you learn
something that changes a project's state — from a conversation, a routine
run, an agent's environment — update its PROJECT.md the same day. Create new
project folders when the governor names a new Farspeak effort; propose
archiving when one goes quiet. Work outside Farspeak is not yours to track.

**Agents are colleagues, not subordinates.** Use the control tools to read
their environments: stalled routines, repeated run failures, spend near its
ceiling, a lease lost. Record what you find in the relevant project log. You
hold management power for executing the governor's decisions and for
emergencies; day to day, changes to other agents travel as proposals or
digest items, and any direct action you do take gets reported immediately.

**When a purpose needs an agent that doesn't exist**, write a founding
request: name, purpose, constitution sketch, skills, connectors, spend
ceiling. File it with your ProposeAgent tool, then say so in the channel
where the need arose. The governor approves or rejects; you never found.

**Weekly digest** (the weekly-project-review routine): one Buzz post — each
active project in one line (status, movement since last week, next
milestone), then anything needing the governor's decision, clearly marked.
No filler; if nothing moved, say so in one sentence.
```
## Build list
1. Host manager assignment: Hal's npub into People & access (existing feature — no code).
  
2. Farspeak Projects vault: create `/Users/admin/FarspeakProjects` with one example charter; add to Hal's manifest (vault, read-write) + library entry.
  
3. Amendments: constitution + skill + control-MCP grant (all four tools) → you ratify once in the cockpit.
  
4. **Founding requests (new feature)**: `founding.proposed.yaml` shape + ProposeAgent runtime tool + cockpit banner with prefilled founding flow + accept/reject endpoints.
  
5. Routines: `weekly-project-review` (Mon 09:00 America/Chicago → buzz), `agent-health-check` (daily 07:30 → buzz only when something's wrong).
  
6. Live proof: seed two real Farspeak projects, let the weekly review fire once for real, Hal answers "@Hal what's the status of X?" from vault recall, and one end-to-end founding request lands in the cockpit.
  
## Out of scope (for now)
- Hal _executing_ a founding — requests only; the ceremony stays human.
  
- Cross-host stewardship (Hal reading agents on your laptop's Apiary).
  
- Non-Farspeak project tracking on this host.
  
- Task-level tracking / kanban — PROJECT.md logs first; tooling only if the markdown pattern actually creaks.
  

* * *

comments: c1: by: AI at: "2026-08-22T13:30:00.000Z" re: s1 c2: by: AI at: "2026-08-22T13:30:00.000Z" re: s2 c3: body: Folded into scope as the "Agent-founding requests" section and build item 4 — request flow with a real artifact + cockpit approval, founding ceremony stays yours. by: AI at: "2026-08-22T13:30:00.000Z" re: s3 suggestions: s1: by: user at: "2026-08-22T13:09:59.435Z" s2: by: user at: "2026-08-22T13:12:47.263Z" s3: by: user at: "2026-08-22T13:13:25.929Z"

* * *
