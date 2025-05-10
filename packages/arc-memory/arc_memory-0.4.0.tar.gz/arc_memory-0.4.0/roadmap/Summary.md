# Product Roadmap

## Vision & Research Foundation

Arc transforms every codebase into a continuously-evolving **world model**—a live, executable graph of architecture, rationale, and provenance that both humans and AI agents can query, update, and learn from.

Our research addresses a fundamental challenge: while frontier AI coding agents can already resolve over half of real-world GitHub issues and ingest massive context windows, they still struggle with a "transient-context ceiling." Complex software demands memory that is not only large but also:
- **Persistent** - maintaining knowledge over time
- **Structured** - organized in a queryable format
- **Semantically-aware** - supporting concurrent modifications by multiple agents

### Core Thesis

Treat the codebase as a living graph of artifacts, dependencies, and decisions, then enforce semantic rules when agents propose changes. With that foundation, we can train agents to act like reliable teammates, not reckless auto-complete engines.

Our approach integrates three key components:

1. **Temporal Knowledge Graphs (TKGs)** - Provide a structured, queryable history of code artifacts, decisions, and agent actions, capturing the "why" over time.

2. **Causal CRDT Layer** - Extends Conflict-free Replicated Data Types with mechanisms to check software-specific invariants (like build dependencies or API contracts) derived from the TKG, enabling safe parallel edits that respect code semantics.

3. **Provenance-Driven RL** - Rewards agents not only for task completion but specifically for generating and consuming causal context within the TKG, fostering better coordination and documentation.

## The Problem We're Solving

Software engineering is fundamentally a collaborative, knowledge-intensive process. Yet the tools we use to build software are primarily focused on the "what" and "how" of code, leaving the crucial "why" scattered across pull requests, issues, documentation, and team communications.

This fragmentation creates significant challenges:

- **Knowledge loss** when team members leave or switch projects
- **Onboarding friction** for new developers trying to understand existing code
- **Decision amnesia** where teams repeat past mistakes or reinvent solutions
- **Context switching** as developers hunt for information across multiple tools
- **Agent limitations** where AI assistants lack the historical context to provide truly helpful guidance

Arc Memory addresses these challenges by creating a unified, temporal knowledge graph that connects code to its full context and history.

## Current Stage & Focus

Arc is a pre-seed, pre-launch startup focused on building momentum through the Arc Memory for GitHub Chrome extension as our point of entry. While our research vision is ambitious, our immediate product focus is on delivering tangible value to developers through:

1. **Arc Memory SDK** - Our core Python toolkit that embeds a local, bi-temporal knowledge graph in every developer's workspace
2. **Arc Daemon** - A lightweight HTTP service that exposes the knowledge graph to local clients
3. **Arc Memory for GitHub Extension** - A Chrome extension providing instant intelligence inside the developer's existing PR workflow

## Key Metrics

We're tracking the following metrics to measure our success:

- Extension installs
- Repositories with memory built
- Hover card views per PR
- Reduction in PR review time (<2 min "Aha!" from install to first contextual insight; ≥20% drop in median review latency)
- User feedback and testimonials

## How to Use This Roadmap

This roadmap provides a comprehensive view of Arc Memory's journey, current focus, and future direction. It serves as a strategic overview for team members, advisors, and potential investors.

- **Product Journey**: Understand what we've built, what we're building, and where we're headed
- **Current Focus**: Get details on our primary focus area
- **Technical Architecture**: Understand how our components fit together
- **Go-to-Market Strategy**: Learn how we plan to acquire and retain users
- **Metrics & Success Criteria**: See how we measure success
- **Resources & References**: Find links to repositories, projects, and documentation

![Arc Product Suite](/public/arc-vision-diagram.png)