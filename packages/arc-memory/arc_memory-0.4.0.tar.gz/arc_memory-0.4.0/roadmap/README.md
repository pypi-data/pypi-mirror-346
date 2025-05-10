# Arc Memory Roadmap

This directory contains the strategic roadmap for Arc Memory, a local-first knowledge graph that connects code changes to context, enabling multi-hop reasoning to show why decisions were made and their predicted impact.

## Overview

Arc Memory transforms every codebase into a continuously-evolving **world model**—a live, executable graph of architecture, rationale, and provenance that both humans and AI agents can query, update, and learn from.

Our thesis is to build a code review wedge product to create a data flywheel for RL agents over graphs of codebases, ultimately serving as a "world model" to predict technical debt and security risks.

## Roadmap Documents

### Vision & Strategy

| Document | Description |
|----------|-------------|
| [Summary.md](./Summary.md) | High-level overview of Arc Memory's vision, research foundation, and current focus |
| [Architecture.md](./Architecture.md) | Technical architecture, from current implementation to research vision |
| [Architecture_Diagram.md](./Architecture_Diagram.md) | Visual diagrams of system architecture, product roadmap timeline, and data flywheel |
| [GTM.md](./GTM.md) | Go-to-market strategy, target segments, and acquisition channels |
| [Metrics_Success.md](./Metrics_Success.md) | Key metrics and success criteria for measuring progress |

### Product & Execution

| Document | Description |
|----------|-------------|
| [Current_Focus.md](./Current_Focus.md) | Detailed information on our current focus area (GitHub Extension) |
| [Product_Journey.md](./Product_Journey.md) | History of Arc Memory products and lessons learned |
| [User_Persona.md](./User_Persona.md) | Target user personas and their needs |
| [Resources.md](./Resources.md) | Links to repositories, projects, documentation, and competitive analysis |

## Key Components

Arc Memory consists of several components that work together to provide a comprehensive solution:

1. **Arc Memory CLI/SDK**: Core Python package that builds and manages the knowledge graph
2. **Arc Daemon**: Lightweight HTTP service that exposes the knowledge graph to local clients
3. **Arc Memory for GitHub Extension**: Chrome extension that provides insights in GitHub UI
4. **Arc MCP Server**: Server that exposes the knowledge graph to AI assistants

## Target Segments

We're pursuing a two-path approach to market validation:

1. **Mid-Market Companies (Primary Focus)**: Engineering teams of 50-100 engineers experiencing coordination challenges
   - Design Partners: Quicknode, Protocol Labs, NEAR Protocol

2. **Early-Stage Startups**: Engineering teams of 5-10 developers experiencing context drift due to rapid development

## North Star Metrics

Our primary North Star metrics focus on the value we deliver to users and the growth of our data flywheel:

1. **Engineering Velocity Impact**: Composite metric combining PR review acceleration and development speed
2. **Active Adoption Rate**: Percentage of eligible engineers using Arc Memory weekly
3. **Knowledge Graph Effectiveness**: Composite metric combining graph density and practical utility
4. **Incident Response Acceleration**: Reduction in time spent investigating production issues
5. **AI Augmentation Multiplier**: Effectiveness improvement of AI tools when paired with Arc Memory

## Monetization Path

Our metrics are designed to track progress toward three key monetization vectors:

1. **Team Productivity** ($50-100/user/month)
2. **Incident Response** ($150-300/user/month)
3. **AI Enhancement** ($200-500/user/month)

## Research Vision

Our full research vision integrates three key components:

1. **Temporal Knowledge Graphs (TKGs)** - Provide a structured, queryable history of code artifacts, decisions, and agent actions, capturing the "why" over time.

2. **Causal CRDT Layer** - Extends Conflict-free Replicated Data Types with mechanisms to check software-specific invariants derived from the TKG, enabling safe parallel edits that respect code semantics.

3. **Provenance-Driven RL** - Rewards agents not only for task completion but specifically for generating and consuming causal context within the TKG, fostering better coordination and documentation.

## What We Believe Won't Change

Our approach is anchored in three human constants that won't change over the next five-plus years:

1. **Human accountability for changes** - Code reviews remain the control checkpoint
2. **Need for verifiable provenance** - Especially for AI-generated code
3. **Engineers shifting from coding to orchestration** - Defining intent, reviewing output, enforcing constraints

## How to Use This Roadmap

This roadmap provides a comprehensive view of Arc Memory's journey, current focus, and future direction. It serves as a strategic overview for team members, advisors, and potential investors.

- Start with [Summary.md](./Summary.md) for a high-level overview
- Explore [Architecture_Diagram.md](./Architecture_Diagram.md) for visual representations
- Dive into specific areas based on your interests (technical, product, go-to-market, etc.)

## GitHub Organization

For code repositories and implementation details, visit our [GitHub Organization](https://github.com/Arc-Computer).
