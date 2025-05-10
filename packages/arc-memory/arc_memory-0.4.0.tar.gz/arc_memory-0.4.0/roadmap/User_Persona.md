# User Research & Persona

## Target Persona: Senior Staff Engineers & Engineering Leads

Our primary target persona is senior staff engineers and engineering leads who:

- Review 5-20 PRs per week
- Own domain services or critical infrastructure
- Care deeply about code quality and architectural integrity
- Value speed and safety in the review process
- Struggle with context-switching and knowledge fragmentation
- Are enthusiastic about "extra eyes" on risk
- Are skeptical of local fine-tunes
- Want zero configuration

## User Research Findings

From our research with developers, we've identified key pain points:

### PR Review Workflow Challenges

| Theme | Evidence snippet | What it signals |
| --- | --- | --- |
| **Manual narrowing + keyword search** | "Use keywords related to the issue in your repo's search." | Context retrieval = ad-hoc string search → huge recall gaps. |
| **Heavy dependency on PR descriptions/comments** | "Lack of detailed descriptions makes it difficult to understand the changes." | Quality of upstream documentation dictates mean-time-to-resolution; brittle. |
| **Git-blame as final resort** | "Use git blame to trace code to a PR." | Linear history helps, but blame ≠ rationale; still requires hop to PR. |
| **Biggest drags: PR volume & merge complexity** | "Sifting through a large number of PRs can be overwhelming… complex merge histories." | Time sink grows non-linearly with repo age & micro-service sprawl → Arc's temporal graph fits. |
| **Patchy mitigations: branch envs, feature flags, CI templates** | "We spin up an env per branch… feature flags to isolate changes." | Teams invest effort in *prevention*, not *diagnosis*; shows appetite for complementary tooling. |

> Pattern: Investigation is still search-and-scroll across GitHub UI, Slack, and git blame. Highest friction: reconstructing the "why" behind merged code when docs/comments are thin.

### Incident Response Challenges

| Theme | Evidence snippet | What it signals |
| --- | --- | --- |
| **Heavy reliance on vanilla Git commands** | "`git log` + `git blame` get me 80 % there." | Manual ≠ scalable; context is scattered. |
| **Structured—but labor-intensive—RCA rituals** | "Monthly *major-incident reviews* with cross-team write-ups." | High coordination cost → good wedge for automation. |
| **Git-ops rule: infra-as-code & DB migrations tracked** | "Everything lives in Git, even Flyway scripts." | Arc can hook into a single source-of-truth without new workflow adoption. |
| **Logging/observability gaps** | "We built a mini logging tool because vendor pricing got insane." | Budget sensitivity + DIY pain → willingness to adopt cheaper, smarter context. |
| **OTel momentum** | "Rolling out OTEL after enshittification of legacy vendors." | Opportunity to integrate Arc spans with OTEL traces for causal graphs. |

> Early pattern: Process is documented but still slow, multi-person, and brittle—classic "hair-on-fire" signals if we quantify time/people.

## Trust in Design: Core Principles

Our product design is guided by the understanding that trust is proven in every micro-interaction. For our users, trust is a cumulative, subconscious assessment shaped by subtle design cues in every interaction.

### Key Interaction Points that Shape Trust:

1. **First Hover Interaction (The "Wow" Card)**
   - First impressions deeply influence subconscious trust
   - Citations as clickable "truth-links"
   - Instant (<500ms) loading

2. **Consistent, Minimalistic UI**
   - Complexity and noise create doubt
   - Simplicity subconsciously implies mastery and confidence
   - Minimal chrome with subtle affordances

3. **Clarity in Provenance Trails**
   - Users subconsciously evaluate visual clarity as truthfulness
   - Chronological, linear timelines
   - Explicit, familiar icons immediately recognized

4. **Micro-interaction Responsiveness**
   - Human brains equate speed and responsiveness to reliability
   - Instantaneous micro-prompt answers with streaming text
   - Visual confirmations for critical actions

5. **Graceful Handling of Errors or Unknowns**
   - Transparent handling of limitations actually builds trust
   - Clearly labeled fallbacks
   - Option to manually enrich context if Arc doesn't have it

### Subconscious Trust-Building Mental Model:

| User Thought (Subconscious) | Arc's Design Response |
| --- | --- |
| "Is this info reliable?" | Clear citations and direct source linking |
| "Does it respect my time?" | Instant response, <500ms loads |
| "Does Arc actually understand?" | Concise, relevant answers without fluff |
| "Can I trust this tool in critical reviews?" | Graceful error handling, fallback options |

### What Users Will Remember and Tell Others

Your user won't rave to peers simply about having "good context" or "citation links." They'll tell a peer something more emotional and resonant:

> "Arc just gets it. It shows me exactly why code changed—Slack conversations, ADR docs, PR history—right where I need it. Feels like magic, and it's always spot-on. Now I honestly don't know how I reviewed code without it."

That's the subconscious win you're after—**effortless certainty.**

## Ambient Interface Philosophy

Our approach embodies the "ambient interface" philosophy:

1. **Unintrusive presence**: Systems live in the periphery until summoned, complementing rather than competing with the primary task.
2. **Context made visible, not verbose**: Surface only the minimum information required to sustain flow, then disappear.
3. **Verifiability as a trust pillar**: In an AI-generated world, provenance (traceable origin) is the currency of credibility.

### How Arc embodies the ambient interface thesis

| **Ambient principle** | **Concrete UX element** | **Subconscious signal** |
| --- | --- | --- |
| **Peripheral until needed** | Gutter dot + <500 ms hover card | "Arc is there when I look for it, never shouting." |
| **Context, not clutter** | 3-item timeline & micro-prompt; no sidebar chat by default | "I see exactly enough to unblock me." |
| **Always provable** | Click-through citations to Slack, ADR, PR | "Arc's claims are audit-ready." |

These choices match best-in-class dev-tool minimalism (Warp's sparse chrome, Linear's clear hierarchy, Cursor's inline context) while adding the one thing the others lack: deep decision provenance.