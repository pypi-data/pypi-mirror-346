# Arc Memory V1 Implementation Plan

## Overview

This document outlines a focused implementation plan for Arc Memory V1, which will power the PR bot - our initial product wedge. The plan prioritizes features that directly enhance the quality of context provided during code review, with a focus on preserving the "why" behind code changes and predicting the blast-radius of changes before they're merged.

## Core Problem Statement

> "Engineering teams ship AI-generated code faster than they can understand, verify, or coordinate it, because the 'why' behind each change vanishes at merge, driving up risk and dragging down velocity."

## Competitive Differentiation

Arc Memory differentiates from competitors (Letta, Mem0, Zep, WhyHow.AI, Unblocked) through:

1. **Vertical Data Model**: We capture specific causal edges (decision → implication → code-change) rather than offering a horizontal memory solution
2. **Workflow Integration**: We embed directly into the PR review process rather than requiring teams to adopt a new tool
3. **Blast-Radius Prediction**: We treat the repo as an RL environment to predict impacts before merge
4. **High-Stakes Focus**: We target fintech, blockchain, and payment-rail providers where downtime costs ~$15k/min
5. **Future-Ready**: We're building for a future where multiple agents modify code simultaneously

## Success Criteria for V1

1. **Causal Edge Fidelity**: Accurately capture and represent decision → implication → code-change relationships
2. **Blast-Radius Prediction**: Identify potential impacts of changes before merge
3. **PR Bot Integration**: Export optimized graph slices for LLM reasoning during PR reviews
4. **Build Time vs. Accuracy**: Achieve high accuracy in retrieval, even at the cost of longer build times
5. **Usability**: Two-click setup in CI environments

## Implementation Timeline

**Total Duration: 3 Weeks**

### Week 1: Core Retrieval Optimization

Focus on the essential components that directly impact PR bot effectiveness.

#### 1. Causal Edge Representation (2 days)

**Goal**: Implement robust representation of decision → implication → code-change relationships.

**Tasks**:
- Enhance schema models to represent causal edges
- Implement extraction of causal relationships from:
  - Commit messages and PR descriptions
  - Linear tickets and their relationships
  - ADRs and technical documentation
- Create visualization of causal chains for debugging

**Definition of Done**:
- Schema supports causal edge representation
- Extraction correctly identifies decision points and their implications
- Causal chains are preserved in the knowledge graph
- Unit tests verify causal edge integrity

#### 2. Knowledge Graph of Thoughts (KGoT) Enhancement (2 days)

**Goal**: Complete the KGoT implementation to capture comprehensive decision trails.

**Tasks**:
- Enhance `process/kgot.py` to capture complete reasoning chains
- Implement robust extraction of:
  - Decision points
  - Alternatives considered
  - Evaluation criteria
  - Decision implications
- Add confidence scores for inferred reasoning

**Definition of Done**:
- KGoT processor generates reasoning nodes and edges for key decisions
- Unit tests verify reasoning structure integrity
- Integration tests confirm reasoning chains are preserved in exports

#### 3. Export Optimization for PR Bot (2 days)

**Goal**: Enhance the export functionality to provide optimal context for PR reviews.

**Tasks**:
- Enhance `optimize_export_for_llm` in `export.py`
- Implement PR-specific context filtering
- Structure JSON payload for efficient LLM reasoning
- Add metadata to guide LLM through the reasoning process

**Definition of Done**:
- Export function produces optimized JSON for PR context
- Export includes all relevant nodes and edges within specified hops
- Unit tests verify export structure and content

#### 4. Blast-Radius Prediction Paths (1 day)

**Goal**: Implement specialized reasoning paths for predicting change impact.

**Tasks**:
- Enhance `generate_common_reasoning_paths` in `export.py` with focus on blast-radius
- Implement specialized paths for:
  - Component impact analysis
  - Service dependency tracing
  - Security-critical path identification
  - Data flow impact assessment

**Definition of Done**:
- Blast-radius prediction paths are included in exports
- Paths provide clear guidance for impact assessment
- Unit tests verify path generation logic

### Week 2: Semantic and Temporal Enhancement

Focus on improving the semantic understanding of code and its evolution over time.

#### 5. Code Analysis Ingestor Enhancement (3 days)

**Goal**: Enhance code analysis to extract rich semantic relationships.

**Tasks**:
- Enhance `ingest/code_analysis.py` to extract:
  - Function and method relationships
  - Class hierarchies
  - Module dependencies
  - API contracts
- Implement language-specific analyzers for Python, JavaScript, and TypeScript
- Add fintech/blockchain-specific code pattern recognition

**Definition of Done**:
- Code analysis extracts semantic relationships from multiple languages
- Industry-specific patterns are identified (payment flows, security checks)
- Relationships are properly stored in the graph
- Unit tests verify extraction accuracy

#### 6. Architecture Detection Implementation (2 days)

**Goal**: Implement basic architecture detection to understand system structure.

**Tasks**:
- Implement `detect_architecture` in `process/semantic_analysis.py`
- Add heuristics for:
  - Service boundary detection
  - Component relationship mapping
  - Dependency flow analysis
- Add specific detection for financial transaction flows

**Definition of Done**:
- Architecture detection identifies system components and services
- Financial transaction flows are properly identified
- Component relationships are properly represented in the graph
- Unit tests verify detection accuracy

#### 7. Change Pattern Analysis (2 days)

**Goal**: Enhance temporal analysis to identify patterns of change and predict blast radius.

**Tasks**:
- Enhance `ingest/change_patterns.py` to identify:
  - Co-changing files
  - Refactoring patterns
  - Feature evolution patterns
  - High-risk change patterns in financial systems
- Implement temporal edge creation for related changes
- Add risk scoring for changes based on historical patterns

**Definition of Done**:
- Change patterns are identified and stored in the graph
- Risk scores are assigned to change patterns
- Temporal relationships between changes are established
- Unit tests verify pattern detection and risk scoring logic

### Week 3: Integration and Testing

Focus on integrating components, optimizing performance, and ensuring reliability.

#### 8. LLM Integration Optimization (2 days)

**Goal**: Optimize LLM integration for reasoning quality.

**Tasks**:
- Evaluate Phi-4 Mini vs. Qwen3:4b for reasoning tasks
- Implement model switching in `llm/ollama_client.py`
- Enhance system prompts for PR review scenarios

**Definition of Done**:
- LLM integration uses the optimal model for reasoning
- System prompts guide the LLM effectively for industry-specific contexts
- Unit tests verify LLM response quality
- Performance benchmarks show acceptable reasoning time

#### 9. GraphRAG Implementation (2 days)

**Goal**: Implement basic GraphRAG structures for improved retrieval.

**Tasks**:
- Enhance export functionality with GraphRAG structures
- Add graph-aware retrieval paths
- Optimize for LLM reasoning efficiency
- Implement causal edge traversal optimizations

**Definition of Done**:
- Exports include GraphRAG structures
- Retrieval paths are optimized for graph traversal
- Causal edges are prioritized in retrieval
- Unit tests verify GraphRAG structure integrity

#### 10. Agent Attribution Framework (1 day)

**Goal**: Lay groundwork for future multi-agent scenarios.

**Tasks**:
- Implement basic agent attribution metadata
- Add conflict detection for overlapping changes
- Create framework for agent-specific reasoning paths
- Document extension points for future agent capabilities

**Definition of Done**:
- Agent attribution metadata is included in the graph
- Basic conflict detection is implemented
- Documentation explains how to extend for multi-agent scenarios
- Unit tests verify attribution integrity

#### 11. Integration Testing and Performance Optimization (2 days)

**Goal**: Ensure all components work together reliably and efficiently.

**Tasks**:
- Implement end-to-end tests for the complete pipeline
- Optimize build process for CI environments
- Benchmark and optimize performance
- Create documentation for users and contributors
- Add fintech/blockchain-specific test cases

**Definition of Done**:
- End-to-end tests pass reliably
- Build process completes within acceptable time limits (< 2 minutes)
- Documentation is clear and comprehensive
- CI integration is verified
- Industry-specific test cases validate specialized features

## Implementation Recommendations

To ensure efficient implementation and maximize the value of the knowledge graph for LLM reasoning, we recommend the following approaches:

### 1. Leverage Existing Fields
- Use the `extra` field in nodes to store additional metadata rather than creating new fields
- Use the `properties` field in edges to store relationship metadata
- This approach maintains schema compatibility while allowing for rich metadata

### 2. Optimize for Export Performance
- The export functionality is critical for the PR bot
- Add indices to improve query performance for common export patterns
- Consider caching frequently accessed subgraphs for high-value files

### 3. Focus on Extraction Quality
- The database structure is solid; focus on improving the quality of extraction
- Prioritize accurate identification of causal relationships and industry-specific patterns
- Implement robust error handling to ensure partial extraction succeeds even when some aspects fail

### 4. Enhance the `optimize_export_for_llm` Function
- This function is already implemented but should be enhanced
- Structure the JSON payload for optimal LLM reasoning
- Include explicit reasoning paths and metadata to guide the LLM

## Scope Boundaries

To prevent scope creep, the following features are explicitly **out of scope** for V1:

1. **Full-Text Search**: Will be implemented in a future version
2. **Documentation Analysis Plugin**: Not critical for initial PR bot functionality
3. **Developer Workflow Analysis**: Can be added in a future enhancement
4. **Browser Extension Integration**: Focus on GitHub App PR bot only
5. **Advanced Visualization**: Text-based insights are sufficient for V1
6. **Full Multi-Agent Orchestration**: Only foundational attribution framework for V1

## Risk Mitigation

1. **Build Time Risk**: If build times exceed 2 minutes, implement selective processing of high-value files
2. **LLM Integration Risk**: If Ollama integration proves unstable, fall back to rule-based reasoning for V1
3. **CI Integration Risk**: Provide detailed troubleshooting documentation for common CI issues
4. **Competitive Risk**: Monitor Unblocked's post-Series A moves and adjust messaging if needed

## Success Metrics

1. **Causal Edge Quality**: >90% of decision → implication → code-change relationships correctly identified
2. **Blast-Radius Accuracy**: Correctly predict >75% of impacted components in test scenarios
3. **Build Time**: Complete graph build in <2 minutes for standard repositories
4. **User Satisfaction**: Positive feedback from initial fintech/blockchain users on context quality
5. **Technical Debt**: <10% of code marked as technical debt or requiring refactoring

## Competitive Advantage Metrics

1. **Vertical Depth**: Demonstrate 2x more accurate predictions for fintech/blockchain codebases vs. general tools
2. **Causal Understanding**: Show 3x more complete decision trails than vector-based approaches
3. **Workflow Integration**: Achieve <5 minute setup time in CI environments

## Conclusion

This focused implementation plan prioritizes the features that directly contribute to Arc Memory's differentiated value proposition: capturing causal edges between decisions, implications, and code changes, and predicting blast-radius before merge. By emphasizing our vertical focus on high-stakes industries and preparing for a multi-agent future, we can deliver a compelling V1 product that stands apart from horizontal memory solutions.

The plan maintains a tight 3-week timeframe while incorporating the key elements that differentiate Arc from competitors like Letta, Mem0, Zep, WhyHow.AI, and Unblocked. By adhering to this plan and respecting the scope boundaries, we can establish Arc Memory as the premier vertical memory layer for engineering teams in high-stakes industries.
