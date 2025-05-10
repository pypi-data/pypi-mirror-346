# Product Journey

## Past Experiments & Learnings

### VS Code Extension (Initial Approach)
- **Status**: Pivoted
- **Timeline**: Early development phase
- **Description**: Our original thesis was to start with a VS Code Extension that provided hover state directly in the IDE.
- **Key Learnings**: 
  - For our target persona of senior staff engineers and engineering leads, code review still happens primarily in the browser, not the IDE.
  - We needed to surface insights at the point of decision or context refresh within their actual workflow.
  - Value delivery needed to happen where decisions are made (GitHub PR review), not just where code is written.
- **Outcome**: Pivoted to focus on GitHub Chrome extension as primary interface.

### CLI-only Approach
- **Status**: Active, but insufficient alone
- **Timeline**: Initial product
- **Description**: Command-line interface for building and querying the knowledge graph.
- **Key Learnings**:
  - The CLI provides a strong foundation and core functionality.
  - However, there's no visualization or actualization of the graph for users to truly understand why this is better than existing solutions.
  - Users need to see the connections to appreciate the value.
- **Outcome**: Maintained as core infrastructure, but supplemented with visual interfaces.

### MCP Server for AI Assistants
- **Status**: Active, but early adoption
- **Timeline**: Ongoing development
- **Description**: Server exposing the knowledge graph to AI assistants via Anthropic's Model Context Protocol.
- **Key Learnings**:
  - AI assistants benefit greatly from structured knowledge graph access.
  - However, users need to see direct value before investing in building the graph.
- **Outcome**: Maintained as part of the ecosystem, but not the primary focus for initial adoption.

## Current Products

### Arc Memory CLI
- **Status**: Active
- **Description**: Command-line interface and underlying SDK for graph building, simulation, and querying
- **Key Features**:
  - Temporal Knowledge Graph
  - Simulation Engine
  - Decision trail querying
  - Local SQLite Database
- **GitHub**: [arc-memory](https://github.com/Arc-Computer/arc-memory)
- **Current Focus**: Maintaining and improving core functionality

### Arc Daemon
- **Status**: In Development (Critical Infrastructure)
- **Description**: Lightweight HTTP service that exposes the Arc SDK's temporal knowledge graph to local clients
- **Key Features**:
  - Core API with `/ping` and `/why` endpoints
  - Authentication and Build endpoints
  - Search endpoint with natural language capabilities
- **GitHub Issues**: [#42](https://github.com/Arc-Computer/arc-memory/issues/42), [#39](https://github.com/Arc-Computer/arc-memory/issues/39), [#40](https://github.com/Arc-Computer/arc-memory/issues/40), [#41](https://github.com/Arc-Computer/arc-memory/issues/41)
- **Linear Project**: [Arc Daemon](https://linear.app/arc-computer/project/arc-daemon-85bdc9f0f299)
- **Rationale**: Enables the Chrome extension to access the knowledge graph while maintaining our local-first, privacy-focused approach.

### Arc Memory for GitHub Extension
- **Status**: In Development (Primary Focus)
- **Description**: Chrome extension providing instant intelligence inside the developer's existing PR workflow
- **Key Features**:
  - Hover Insight Card
  - Auto-index & graph build
  - Arc Search Palette
- **GitHub Issues**: [#43](https://github.com/Arc-Computer/arc-memory/issues/43), [#44](https://github.com/Arc-Computer/arc-memory/issues/44), [#45](https://github.com/Arc-Computer/arc-memory/issues/45), [#46](https://github.com/Arc-Computer/arc-memory/issues/46)
- **Linear Project**: [Arc Memory for GitHub](https://linear.app/arc-computer/project/arc-memory-for-github-9a5c6dd2ad89)
- **Rationale**: Provides an ambient, unobtrusive interface that delivers value at the exact moment of need during code review.

### Arc MCP Server
- **Status**: Active
- **Description**: MCP server exposing the knowledge graph to AI assistants
- **Key Features**:
  - Implements Anthropic's Model Context Protocol (MCP)
  - Provides access to the knowledge graph for contextual retrieval
  - Can be started directly from the CLI
- **GitHub**: [arc-mcp-server](https://github.com/Arc-Computer/arc-mcp-server)

## Current Thesis and Future Roadmap

Our current thesis is to:
1. Build a wedge product (code review) to build a data flywheel
2. Inform RL agents over graphs of codebases
3. Use that environment to act as a "world model" for more accurate output
4. Predict technical debt/security risk based on historical changes (especially if AI generated)

### Near-term (0-3 months)
- Complete Arc Daemon implementation
- Launch Arc Memory for GitHub Extension (MVP)
- Collect user feedback and iterate
- Improve search capabilities

### Mid-term (3-6 months)
- Expand GitHub Extension features
- Improve simulation capabilities
- Build community and gather testimonials
- Refine the data flywheel

### Long-term (6+ months)
- Develop RL agents that leverage the knowledge graph
- Create predictive models for technical debt and security risks
- Explore VS Code integration (revisited with learnings)
- Consider enterprise features and team collaboration