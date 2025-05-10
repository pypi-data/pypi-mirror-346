# Resources & References

## GitHub Organization
- [Arc Computer GitHub Organization](https://github.com/Arc-Computer)

## GitHub Repositories
- [Arc Memory CLI/SDK](https://github.com/Arc-Computer/arc-memory) - Core Python package for building and querying the knowledge graph
- [Arc MCP Server](https://github.com/Arc-Computer/arc-mcp-server) - Server exposing the knowledge graph to AI assistants via Anthropic's MCP

## Linear Projects
- [Arc Daemon](https://linear.app/arc-computer/project/arc-daemon-85bdc9f0f299) - HTTP service exposing the knowledge graph to local clients
- [Arc Memory for GitHub](https://linear.app/arc-computer/project/arc-memory-for-github-9a5c6dd2ad89) - Chrome extension for GitHub PR insights

## Documentation
- [Arc Memory CLI Documentation](https://docs.arc.computer) - Official documentation for the CLI and SDK
- [Architecture Decision Records](https://github.com/Arc-Computer/arc-memory/tree/main/docs/adr) - Technical design decisions
- [API Documentation](https://github.com/Arc-Computer/arc-memory/tree/main/docs/api) - API reference for developers

## Design Partners
- [Quicknode](https://www.quicknode.com/) - Blockchain infrastructure provider
- [Protocol Labs](https://protocol.ai/) - Open-source focused organization (Filecoin, IPFS)
- [NEAR Protocol](https://near.org/) - Blockchain platform with complex architecture

## Research and Competitive Analysis

### Direct Competitors

| Competitor | Focus | Strengths | Weaknesses | Our Differentiation |
|------------|-------|-----------|------------|---------------------|
| [Graphite Diamond](https://diamond.graphite.dev/) | AI code review | Codebase-aware AI reviews, GitHub integration, immediate feedback | Focuses on code quality not decision context, cloud-based | We provide historical decision trails with verifiable provenance, not just code quality feedback |
| [Greptile](https://www.greptile.com/) | AI PR review bot | Full codebase understanding, automated PR reviews, bug detection | Focused on code correctness rather than decision context | We focus on the "why" behind changes with temporal context, not just detecting bugs or issues |
| [Sourcegraph Cody](https://sourcegraph.com/cody) | Code search & generation | Cross-repository context, enterprise focus, integrations with Notion/Linear | Cloud-based, requires setup, primarily focused on code generation | Local-first, privacy-focused temporal knowledge graph that preserves the "why" behind code changes |
| [Zep Memory](https://www.getzep.com/) | AI memory & context | Temporal knowledge graph, entity extraction, context retrieval | General-purpose AI memory, not code-specific | Purpose-built for software development with Git/GitHub/Linear integration and PR-specific insights |
| [GitHub Copilot](https://github.blog/2023-06-20-how-github-copilot-is-getting-better-at-understanding-your-code/) | AI PR comments | Native GitHub integration, code suggestions | Limited to current PR context, no historical decision trails | We connect current changes to historical decisions and provide cross-repository context |

### Adjacent Tools & Potential Integrations

| Tool | Category | Relevance to Arc |
|------|----------|------------------|
| [Linear](https://linear.app/) | Project management | Integration source for tickets and planning context; provides issue metadata for our knowledge graph |
| [GitHub](https://github.com/) | Code hosting & review | Primary integration point for our Chrome extension; source of PR/commit data for knowledge graph |
| [Incident.io](https://incident.io/) | Incident management | Benchmark for incident response value ($150-300/seat); our temporal knowledge graph can enhance incident investigation with code context |
| [Anthropic Claude](https://www.anthropic.com/claude) | AI assistant | Integration via MCP for enhanced context; benefits from our structured knowledge graph |
| [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) | AI coding agent | Terminal-based coding assistant that could be enhanced with Arc's temporal knowledge graph for deeper codebase understanding |
| [Windsurf](https://windsurf.com/) | AI-native IDE | Advanced AI coding editor that could leverage Arc's knowledge graph for better context on code history and decisions |
| [Augment Code](https://www.augmentcode.com/) | Developer AI | AI coding tool for large codebases that could be complemented by Arc's decision trails and historical context |
| [Cognition Labs (Devin)](https://devin.ai/) | AI software engineer | Autonomous coding agent that could benefit from Arc's knowledge graph for better understanding of architectural decisions |
| [OpenHands](https://github.com/All-Hands-AI/OpenHands) | Open-source AI agent | Open-source coding assistant that could integrate with Arc's knowledge graph for enhanced context |
| [CodeSee](https://www.codesee.io/) | Code visualization | Complementary to our approach; they show code structure while we provide decision context |
| [Cursor](https://cursor.sh/) | AI-powered IDE | Potential integration target; could benefit from our knowledge graph for better context |
| [Warp](https://www.warp.dev/) | Terminal | Example of minimal, high-performance developer UX we aspire to match |

### Emerging Competitors

| Competitor | Focus | Current State | Potential Threat |
|------------|-------|--------------|------------------|
| [LlamaPReview](https://news.ycombinator.com/item?id=41996859) | AI PR reviewer | Early stage | Building repository knowledge graph for code relationships |
| [Repobeats](https://repobeats.axiom.co/) | Repository analytics | Analytics focus | Could expand into context for PRs with their existing data |
| Custom LLM solutions | In-house AI tools | Varies by company | Companies building internal tools with similar functionality |

### AI Agent Frameworks

These frameworks provide building blocks for creating AI coding agents but lack the specialized temporal knowledge graph that Arc Memory offers:

| Framework | Focus | Memory Features | Relevance to Arc's Vision |
|-----------|-------|----------------|---------------------------|
| [LangChain](https://www.langchain.com/) | General-purpose agent framework | Basic conversation memory, vector stores for RAG | Could integrate with Arc's knowledge graph for richer historical context beyond simple conversation history |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Agent orchestration | State management, error recovery, time travel debugging | Could leverage Arc's temporal knowledge graph for more informed agent decision-making |
| [AutoGen](https://microsoft.github.io/autogen/) | Multi-agent collaboration | Conversation history, shared context | Could benefit from Arc's decision trails to improve agent collaboration on complex codebases |
| [CrewAI](https://www.crewai.com/) | Role-based agent teams | Task-specific memory | Could use Arc's knowledge graph to provide agents with architectural context and decision history |
| [LlamaIndex](https://www.llamaindex.ai/) | Data framework for LLMs | Document stores, knowledge graphs | Has basic knowledge graph capabilities but lacks the temporal dimension and software-specific context of Arc |
| [Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/overview/) | AI orchestration | Memory stores, skill libraries | Could integrate with Arc's knowledge graph for more contextual code generation |

### Path to RL Coding Agents

Arc Memory's temporal knowledge graph provides the foundation for reinforcement learning in code agents:

1. **Current Focus**: Code review context through temporal knowledge graph
2. **Near-Term Evolution**: Predictive insights based on historical patterns
3. **Medium-Term Vision**: Single-agent assistance with decision context
4. **Long-Term Research**: Multi-agent RL framework using our temporal knowledge graph as the environment

Our differentiation from agent frameworks:
- **Domain-Specific**: Purpose-built for software development lifecycle
- **Temporal Dimension**: Captures evolution of code and decisions over time
- **Verifiable Provenance**: All insights have traceable sources
- **Software-Specific Semantics**: Understands relationships between commits, PRs, issues, and ADRs

## Market Research

### Mid-Market Success Stories
- [Ramp + Anthropic Case Study](https://www.anthropic.com/case-studies/ramp) - Demonstrates the value of AI-powered development in mid-market companies
- Key metrics from Ramp: 1M+ lines of AI-suggested code in 30 days, 50% weekly active usage, 80% reduction in incident investigation time

### Industry Reports
- [State of DevOps 2024](https://cloud.google.com/devops/state-of-devops) - DORA metrics benchmarks
- [GitHub Octoverse](https://octoverse.github.com/) - Developer productivity trends
- [Stack Overflow Developer Survey](https://insights.stackoverflow.com/survey) - Developer tool adoption patterns

## Roadmap Resources

### Vision & Strategy
- [Summary](./Summary.md) - Overview of Arc Memory's vision and strategy
- [Product Journey](./Product_Journey.md) - Evolution of Arc Memory products
- [Architecture](./Architecture.md) - Technical architecture and research vision
- [GTM Strategy](./GTM.md) - Go-to-market approach and target segments

### Execution
- [Current Focus](./Current_Focus.md) - Immediate priorities and implementation phases
- [Metrics & Success](./Metrics_Success.md) - Key metrics and success criteria
- [User Persona](./User_Persona.md) - Target persona and user research findings