# Current Focus: GitHub Extension

## Problem Statement
Developers reviewing PRs struggle with context-switching and understanding the rationale behind code changes, leading to slower reviews and missed issues. As code complexity grows and AI-generated code becomes more common, the need for verifiable provenance and clear decision trails becomes critical.

## Target Persona
**Staff / senior product engineer** (IC4-IC6) reviewing 5-20 PRs a week, owns a domain service, uses GitHub UI for review comments, cares about speed and safety. These engineers are enthusiastic about "extra eyes" on risk, skeptical of local fine-tunes, and want zero configuration.

## Value Proposition
| Driver | Pain Today | Arc V0 Win |
|--------|-----------|------------|
| **PR overload** in mid-market teams (40-150 engrs) | Reviewers drown in context-switching and AI-generated diffs | *One-hover* recall of "why" + predicted blast-radius; cuts review time, raises confidence |
| **Low visibility of Arc SDK** | Local graph quietly builds, but users rarely open the MCP | Chrome ext exposes that graph at the moment of decision—where perceived value is highest |
| **Bottom-up GTM** | Individual engs adopt, org standardises later | Extension installs > active seats → qualified expansion pipeline |

## Current Thesis
Build a wedge product (code review) to create a data flywheel for RL agents over graphs of codebases. Use that environment to act as a "world model" for more accurate output and predict technical debt/security risk based on historical changes (especially if AI generated).

## Design Philosophy: Ambient Interface
Our approach embodies the "ambient interface" philosophy:
1. **Unintrusive presence**: The extension lives in the periphery until needed
2. **Context made visible, not verbose**: Only the minimum information required to sustain flow
3. **Verifiability as a trust pillar**: Provenance is the currency of credibility

## Success Metrics
- **<2 min "Aha!"** from install to first contextual insight
- **≥20% drop in median review latency** on dog-food repos
- **>70%** of repos with memory built / installs
- Median **hover_card_views / PR ≥ 3**

## Implementation Phases

### Phase 1: Minimal Viable Extension
- Core hover card functionality with <150ms response time
- GitHub PR page integration with shadow DOM isolation
- Daemon connectivity and basic error handling
- Focus on the "wow" moment with accurate, verifiable citations
- [GitHub Issue #44](https://github.com/Arc-Computer/arc-memory/issues/44)
- [Linear Issue ARC-25](https://linear.app/arc-computer/issue/ARC-25)

### Phase 2: Graph Building
- Repository detection and status checking
- "Build Memory" banner with clear call-to-action
- One-click build process with progress indicators
- User guidance and onboarding
- [GitHub Issue #45](https://github.com/Arc-Computer/arc-memory/issues/45)
- [Linear Issue ARC-26](https://linear.app/arc-computer/issue/ARC-26)

### Phase 3: Search & Polish
- Basic search interface with natural language capabilities
- Experience refinement based on user feedback
- Error handling improvements and recovery options
- Usage hints and keyboard shortcuts
- [GitHub Issue #46](https://github.com/Arc-Computer/arc-memory/issues/46)
- [Linear Issue ARC-27](https://linear.app/arc-computer/issue/ARC-27)

## Dependencies and Risks

### Dependencies
- Arc Daemon implementation (critical path)
- GitHub API access for repository and PR data
- Chrome Web Store approval process
- Local SQLite database performance

### Risks
- Daemon performance on large repositories
- GitHub UI changes breaking content scripts
- User adoption friction and configuration challenges
- Citation accuracy and trust erosion if provenance is incorrect

### Mitigation Strategies
- Implement aggressive caching in the daemon
- Use robust selectors and shadow DOM for GitHub UI integration
- Focus on zero-configuration setup and clear onboarding
- Prioritize citation accuracy over completeness