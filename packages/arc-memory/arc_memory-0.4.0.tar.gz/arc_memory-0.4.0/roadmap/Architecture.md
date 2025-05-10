# Technical Architecture

## Vision & Research Foundation

Arc's architecture is designed to transform every codebase into a continuously-evolving **world model**—a live, executable graph of architecture, rationale, and provenance that both humans and AI agents can query, update, and learn from.

Our research addresses a fundamental challenge: while frontier AI coding agents can already resolve over half of real-world GitHub issues and ingest massive context windows, they still struggle with a "transient-context ceiling." Complex software demands memory that is not only large but also:
- **Persistent** - maintaining knowledge over time
- **Structured** - organized in a queryable format
- **Semantically-aware** - supporting concurrent modifications by multiple agents

### Research Architecture Components

Our full research vision integrates three key components:

1. **Temporal Knowledge Graphs (TKGs)** - Provide a structured, queryable history of code artifacts, decisions, and agent actions, capturing the "why" over time.

2. **Causal CRDT Layer** - Extends Conflict-free Replicated Data Types with mechanisms to check software-specific invariants (like build dependencies or API contracts) derived from the TKG, enabling safe parallel edits that respect code semantics.

3. **Provenance-Driven RL** - Rewards agents not only for task completion but specifically for generating and consuming causal context within the TKG, fostering better coordination and documentation.

![Research Architecture](/public/arc-research-architecture.png)

## Current Implementation

### System Overview

The current Arc Memory implementation consists of several components that work together to provide a comprehensive solution:

1. **Arc Memory CLI/SDK**: Core Python package that builds and manages the knowledge graph
   - Temporal Knowledge Graph implementation
   - Simulation Engine for predicting change impact
   - Decision trail querying
   - Local SQLite Database

2. **Arc Daemon**: Lightweight HTTP service that exposes the knowledge graph to local clients
   - Core API with `/ping` and `/why` endpoints
   - Authentication and Build endpoints
   - Search endpoint with natural language capabilities

3. **Arc Memory for GitHub Extension**: Chrome extension that provides insights in GitHub UI
   - Hover Insight Card
   - Auto-index & graph build
   - Arc Search Palette

4. **Arc MCP Server**: Server that exposes the knowledge graph to AI assistants
   - Implements Anthropic's Model Context Protocol (MCP)
   - Provides access to the knowledge graph for contextual retrieval
   - Can be started directly from the CLI

![Product Architecture](/public/arc-vision-diagram.png)

## Component Relationships & Data Flow

### Data Ingestion
- **Sources**: Git commits, GitHub PRs/issues, ADRs, Linear tickets, Slack (future)
- **Process**:
  1. CLI or daemon ingests data from sources
  2. Data is processed and normalized
  3. Entities and relationships are extracted
  4. Data is stored in a local SQLite database

### Knowledge Graph Building
- **Process**:
  1. Ingested data is processed to build a temporal knowledge graph
  2. Relationships between entities are established (commits → PRs → issues → ADRs)
  3. Code entities are linked to decision records
  4. Temporal information is preserved

### Query and Retrieval
- **Process**:
  1. GitHub Extension queries the daemon for context
  2. Daemon retrieves information from the knowledge graph using efficient graph traversal
  3. Results are formatted and returned to the extension
  4. Extension displays the information in the GitHub UI

### AI Integration
- **Process**:
  1. MCP Server exposes the knowledge graph to AI assistants
  2. AI assistants query the MCP Server for context
  3. MCP Server retrieves and formats information from the knowledge graph
  4. AI assistants use the context to provide more accurate assistance

## Database Schema

The current implementation uses SQLite with the following core tables:

### Nodes Table
- `id`: Unique identifier
- `type`: Node type (commit, pr, issue, file, etc.)
- `data`: JSON blob with node-specific data
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Edges Table
- `id`: Unique identifier
- `source_id`: Source node ID
- `target_id`: Target node ID
- `type`: Edge type (references, modifies, etc.)
- `data`: JSON blob with edge-specific data
- `created_at`: Timestamp

### Build Manifest Table
- `id`: Unique identifier
- `source`: Data source name
- `last_run`: Timestamp of last build
- `status`: Build status
- `metadata`: JSON blob with build-specific data

## Key Technical Decisions

### Local-First Architecture
- **Current Implementation**: All data stays on the user's machine in a SQLite database
- **Rationale**: Privacy-first approach, no proprietary code leaves the environment
- **Future Evolution**: Hybrid model with optional cloud sync for team collaboration

### Lightweight Components
- **Daemon**: FastAPI + Uvicorn with minimal dependencies
- **Extension**: Manifest V3 + WXT for TypeScript build
- **Performance**: Total wheel size <3 MB for daemon, p95 latency ≤150 ms on a 10k-node graph

### Performance Optimization
- **Caching**: In-memory caching for frequently accessed data
- **Prefetching**: Predictive loading of hover card data
- **Async Processing**: Async handlers with thread pool for heavy operations
- **Indexing**: Strategic database indexes for common query patterns

## Scaling to Enterprise

While our current implementation is local-first for speed and privacy during the experimentation phase, we have a clear path to enterprise scale:

### Database Evolution
- **Current**: SQLite for local-first operation
- **Near Future**: Optional PostgreSQL backend for team-wide graphs
- **Enterprise**: Distributed graph database (Neo4j, TigerGraph) for organization-scale deployment

### Multi-User Collaboration
- **Current**: Single-user, local-first
- **Near Future**: Read-only sharing via daemon API
- **Enterprise**: Full multi-user collaboration with access controls

### Cloud Integration
- **Current**: Fully local
- **Near Future**: Optional cloud sync for backup and sharing
- **Enterprise**: Hybrid model with on-premise or cloud deployment options

### Security & Compliance
- **Current**: Local-only, inherits filesystem security
- **Near Future**: API authentication and encryption
- **Enterprise**: Role-based access control, audit logging, compliance reporting

## Path to Full Research Vision

Our roadmap to realize the full research vision includes:

1. **Temporal Knowledge Graph Enhancements**
   - Richer semantic relationships between entities
   - Improved causality tracking
   - Cross-repository linking

2. **Causal CRDT Implementation**
   - Develop conflict resolution strategies for code semantics
   - Implement dependency checking for safe parallel edits
   - Create APIs for agent interaction

3. **Provenance-Driven RL Framework**
   - Design reward functions for collaborative behavior
   - Implement offline RL training on graph data
   - Create agent playground for experimentation

4. **Multi-Agent Orchestration**
   - Develop agent coordination protocols
   - Implement task allocation and dependency management
   - Create monitoring and evaluation framework

## Technical Challenges & Research Questions

1. **Graph Scalability**: How to efficiently query and update graphs with millions of nodes?
   - Investigating partitioning strategies and distributed query optimization

2. **Semantic Consistency**: How to ensure code semantics are preserved during concurrent edits?
   - Researching program analysis techniques for dependency extraction

3. **Agent Coordination**: How to enable effective collaboration between multiple agents?
   - Exploring multi-agent reinforcement learning approaches

4. **Privacy & Security**: How to balance collaboration with data privacy?
   - Developing federated learning techniques for private knowledge sharing

## From Product to Research Vision: The Data Flywheel

Our path from the current product implementation to the full research vision is guided by a clear thesis:

> Build a wedge product (code review) to create a data flywheel that informs RL agents over graphs of codebases → Use that environment to act as a "world model" for more accurate output and predict technical debt/security risk based on historical changes (especially if AI-generated).

### The Flywheel Effect

This approach creates a reinforcing flywheel where:

1. **Users adopt the GitHub Extension** for immediate value in code review
2. **Knowledge graphs are built** as a side effect of normal development workflows
3. **Decision trails become richer** with each PR, commit, and issue
4. **Data quality improves** as more connections are established
5. **RL agents learn from this data** to provide increasingly valuable insights
6. **User trust increases** as insights become more accurate and valuable
7. **More users adopt the tool**, feeding more data into the system

![Data Flywheel](/public/data-flywheel.png)

### Stages of Evolution

#### Stage 1: Ambient Context (Current)
- **Focus**: GitHub Extension providing hover insights during code review
- **Value**: Immediate context for PR reviewers, reducing cognitive load
- **Data Collection**: Building knowledge graphs from Git, GitHub, ADRs, Linear
- **Technical Foundation**: Local SQLite database, fast graph traversal algorithms

#### Stage 2: Predictive Insights
- **Focus**: Using historical patterns to predict impact of changes
- **Value**: Risk assessment, technical debt identification, security vulnerability prediction
- **Data Collection**: Adding telemetry on PR outcomes, bug reports, performance metrics
- **Technical Foundation**: Simple ML models trained on graph features

#### Stage 3: Agent Assistance
- **Focus**: Single-agent assistance for specific tasks
- **Value**: Automated code review, documentation generation, test creation
- **Data Collection**: Agent actions, outcomes, and user feedback
- **Technical Foundation**: Supervised learning from human feedback

#### Stage 4: Multi-Agent Collaboration (Research Vision)
- **Focus**: Multiple agents collaborating on complex tasks
- **Value**: Autonomous maintenance, refactoring, and evolution of codebases
- **Data Collection**: Inter-agent communication, task allocation, conflict resolution
- **Technical Foundation**: Full Causal CRDT layer, Provenance-Driven RL

### Key Hypotheses

1. **Context Hypothesis**: Providing verifiable context at the point of decision will significantly improve code review quality and speed.
   - **Validation Metric**: ≥20% drop in median review latency on dog-food repos

2. **Flywheel Hypothesis**: The value of the knowledge graph increases non-linearly with the number of connections.
   - **Validation Metric**: Correlation between graph density and user engagement metrics

3. **Agent Learning Hypothesis**: Agents trained on rich, structured knowledge graphs will outperform those trained on flat text corpora.
   - **Validation Metric**: Performance on code understanding and modification benchmarks

4. **Provenance Hypothesis**: Explicitly rewarding agents for generating and consuming causal context will lead to better collaboration.
   - **Validation Metric**: Quality of documentation and decision trails in agent-modified code

## What We Believe Won't Change in the Next Five Years

Our approach is anchored in three human constants that won't change over the next five-plus years:

### 1. Human Accountability for Changes

Even as AI coders accelerate generation, **code reviews remain the control checkpoint**—industry predictions through 2030 emphasize human-guided, AI-assisted reviews instead of replacement. This is why we focus on enhancing the review process first, rather than replacing human judgment.

**Implications for Arc**:
- The GitHub Extension must provide clear, verifiable context that enhances human judgment
- Simulation results must be explainable and traceable to source data
- Human reviewers should remain the final decision-makers, with Arc providing decision support

### 2. Need for Verifiable Provenance

Regulators, security teams, and senior engineers are converging on provenance requirements for AI-generated code. ADRs are already a de-facto best practice, and AWS and other major platforms are formalizing them into governance workflows.

**Implications for Arc**:
- Every insight must be backed by clickable citations to source material
- The knowledge graph must maintain a complete audit trail of decisions and their rationale
- Attestations for simulations must be cryptographically verifiable
- AI-generated content must be clearly marked and linked to its inputs

### 3. Engineers Shifting from Coding to Orchestration

Thought-leadership pieces predict engineers acting as **system orchestrators**—defining intent, reviewing output, enforcing constraints. That role amplifies the need for fast, trustworthy context to make decisions, not for typing speed.

**Implications for Arc**:
- Tools must support the orchestration workflow, not just the coding workflow
- Context must be available at the point of decision, not just the point of coding
- Insights must be actionable and relevant to architectural decisions
- The system must support cross-service and cross-repository understanding

## Research Challenges and Opportunities

The path from our current product to the full research vision presents several challenges:

1. **Scaling Knowledge Representation**: How do we efficiently represent and query increasingly complex knowledge graphs?
   - **Opportunity**: Develop novel graph compression and indexing techniques

2. **Causal Learning**: How do we extract causal relationships from observational data in codebases?
   - **Opportunity**: Apply causal inference techniques to software engineering data

3. **Multi-Agent Coordination**: How do we enable effective collaboration between specialized agents?
   - **Opportunity**: Develop new coordination protocols and incentive structures

4. **Human-Agent Collaboration**: How do we design interfaces that enable effective collaboration between humans and agents?
   - **Opportunity**: Create new interaction paradigms for ambient intelligence

5. **Evaluation Metrics**: How do we measure the quality of agent contributions to a codebase?
   - **Opportunity**: Develop new metrics for code quality, maintainability, and architectural coherence

By addressing these challenges, we can bridge the gap between our current product and the full research vision, creating a system that transforms how software is developed, maintained, and evolved.