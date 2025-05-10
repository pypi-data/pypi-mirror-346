# Metrics & Success Criteria

## North Star Metrics

Our primary North Star metrics focus on the value we deliver to users and the growth of our data flywheel, refined based on mid-market success patterns:

1. **Engineering Velocity Impact**: Composite metric combining PR review acceleration and development speed
   - PR Review Time: ≥20% drop in median review latency on partner repos
   - Development Acceleration: Increase in code implementation speed with Arc context
   - Target: 30% overall velocity improvement across development lifecycle
   - *Rationale*: Captures both immediate review benefits and broader development acceleration

2. **Active Adoption Rate**: Percentage of eligible engineers using Arc Memory weekly
   - Weekly Active Usage: Target of 50%+
   - Feature Engagement: Usage of hover cards, search, and other key features
   - Viral Spread: New users onboarded through team referrals
   - *Rationale*: Directly measures product-market fit and sustainable growth

3. **Knowledge Graph Effectiveness**: Composite metric combining graph density and practical utility
   - Graph Density: Average connections per entity in the graph
   - Citation Accuracy: Percentage of citations that correctly reference source material (target: 95%+)
   - Coverage: Percentage of codebase with complete decision trails
   - *Rationale*: Measures both the richness and reliability of your data flywheel

4. **Incident Resolution Acceleration**: Reduction in time spent investigating production issues
   - Investigation Time: Target of 40-80% reduction
   - Context Availability: Percentage of incidents where Arc provides relevant context
   - Root Cause Identification: Speed of identifying underlying causes
   - *Rationale*: Addresses critical pain point with measurable business impact

5. **AI Augmentation Multiplier**: Effectiveness improvement of AI tools when paired with Arc Memory
   - Code Quality: Improvement in correctness of AI-generated code
   - Context Relevance: Reduction in hallucinations when using Arc's verifiable citations
   - Suggestion Acceptance: Increase in AI suggestion acceptance rates
   - Target: 2x improvement in AI suggestion relevance
   - *Rationale*: Captures long-term AI enhancement value proposition

## Segment-Specific Success Metrics

### Mid-Market Companies (Primary Focus)
- **Team Adoption Rate**: Percentage of eligible team members who install and use the extension
- **Cross-Repository Insights**: Number of insights that connect multiple repositories
- **Knowledge Retention Score**: Measure of how effectively knowledge is preserved during team changes
- **PR Review Efficiency**: Time from PR creation to approval, normalized by PR size

### Early-Stage Startups
- **Onboarding Time**: Time for new team members to make meaningful contributions
- **Context Switch Recovery**: Time to regain context when switching between projects
- **Documentation Coverage**: Percentage of code with associated decision trails
- **Developer Satisfaction**: Survey-based measure of tool satisfaction

## Funnel Metrics

### Activation Metrics
- **Extension Installs**: Total number of extension installations
- **Repositories with Memory Built**: Number of repositories with knowledge graphs
- **Time to First Hover Insight**: Time from installation to first hover card view
- **Success Rate for Graph Building**: Percentage of successful graph builds
- **"Aha!" Moment**: <2 minutes from install to first contextual insight

### Engagement Metrics
- **Hover Card Views per PR**: Average number of hover card views during PR review
- **Search Queries per User**: Number of search queries per active user
- **Feature Usage Distribution**: Usage patterns across different features
- **Session Duration**: Time spent using the extension per session
- **Citation Click-Through Rate**: Percentage of hover cards where citations are clicked

### Retention Metrics
- **Weekly Active Users (WAU)**: Users who perform at least one action per week
- **Monthly Active Users (MAU)**: Users who perform at least one action per month
- **Retention Rate**: Percentage of users who remain active after 1, 7, 30 days
- **Uninstall Rate**: Percentage of users who uninstall the extension
- **Feature Stickiness**: Ratio of DAU to MAU for specific features

### Business Metrics
- **User Growth Rate**: Month-over-month growth in active users
- **Conversion to Paid Tiers**: Percentage of users who upgrade to paid plans (future)
- **Customer Acquisition Cost (CAC)**: Cost to acquire a new customer (future)
- **Lifetime Value (LTV)**: Projected revenue from a customer over their lifetime (future)
- **Net Revenue Retention**: Revenue retained from existing customers over time (future)

## Data Flywheel Metrics

These metrics measure the health and growth of our data flywheel:

- **Graph Size**: Total number of nodes and edges in the knowledge graph
- **Graph Growth Rate**: Month-over-month growth in graph size
- **Entity Coverage**: Percentage of codebase entities represented in the graph
- **Connection Density**: Average number of connections per entity
- **Provenance Quality**: Measure of the quality and completeness of decision trails
- **Cross-Repository Linkage**: Number of connections spanning multiple repositories
- **Semantic Richness**: Depth and quality of relationship types in the graph
- **Temporal Depth**: Average historical depth (in time) of decision trails
- **Citation Accuracy**: Percentage of citations that correctly reference source material
- **Knowledge Graph ROI**: Estimated value created per node in the graph

## Current Targets

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Time to first hover insight | <2 minutes | - | Not measured |
| Reduction in PR review time | ≥20% | - | Not measured |
| Repos with memory built / installs | >70% | - | Not measured |
| Hover card views / PR | ≥3 | - | Not measured |
| Weekly active users / installs | >50% | - | Not measured |
| Graph build success rate | >90% | - | Not measured |
| Citation accuracy | >95% | - | Not measured |

## SDLC Impact Metrics

These metrics measure Arc Memory's impact across the full software development lifecycle:

### Planning & Design Phase
- **Decision Quality**: Reduction in design revisions after implementation
- **Historical Context Utilization**: Frequency of referencing past decisions during planning
- **Architecture Consistency**: Adherence to established patterns and principles

### Development Phase
- **Context Switch Recovery**: Time to regain context when switching between tasks
- **AI Code Assistance Quality**: Accuracy and relevance of AI-generated code with Arc context
- **Documentation Automation**: Percentage of code with automatically generated context

### Review Phase (Current Focus)
- **Review Depth**: Number of substantive comments per PR
- **Review Confidence**: Reviewer confidence in understanding code changes
- **Context Availability**: Percentage of PR lines with available decision context

### Testing Phase
- **Test Coverage Guidance**: Effectiveness of test strategy based on historical patterns
- **Defect Prediction**: Accuracy of defect predictions based on change patterns
- **Test Efficiency**: Reduction in test-related questions during development

### Deployment Phase
- **Change Risk Assessment**: Accuracy of predicted risk scores for deployments
- **Rollback Prediction**: Ability to predict deployment issues before they occur
- **Deployment Confidence**: Team confidence in deployments with Arc insights

### Maintenance Phase
- **Knowledge Retention**: Preservation of context during team transitions
- **Maintenance Efficiency**: Time to understand and modify existing code
- **Technical Debt Visibility**: Accuracy of technical debt identification

## Success Criteria by Phase

### Phase 1: Validation (Current)
- ≥20% drop in median review latency on partner repos
- >70% of repos with memory built / installs
- <2 minutes from install to first contextual insight
- Positive qualitative feedback from design partners
- Initial measurement of Decision Confidence Index

### Phase 2: Limited Release
- >50% weekly active users / installs
- >80% retention after 30 days
- >90% graph build success rate
- Net Promoter Score (NPS) > 40
- 25% reduction in onboarding time for new team members
- Measurable improvement in AI code suggestion quality

### Phase 3: Market Expansion
- >1,000 active organizations
- >10,000 active users
- >95% citation accuracy
- Positive unit economics
- Growing open-source community
- 2x AI Augmentation Multiplier
- Demonstrable impact across multiple SDLC phases

## Measurement and Reporting

- **Weekly Metrics Review**: Internal review of key metrics
- **Monthly Partner Reviews**: Share metrics with design partners
- **Quarterly Roadmap Alignment**: Adjust roadmap based on metrics
- **Automated Dashboards**: Real-time visibility into key metrics
- **User Feedback Loops**: Regular surveys and interviews to supplement quantitative data

## ARR Growth Potential

Our metrics are designed to track progress toward three key monetization vectors:

### 1. Team Productivity ($50-100/user/month)
- Measured via PR review time reduction
- Quantified through time savings and improved decision quality
- Initial ARR driver through productivity gains

### 2. Incident Response ($150-300/user/month)
- Measured via incident investigation time reduction and resolution speed
- Quantified through reduced MTTR (Mean Time To Resolution) and business impact
- Mid-term ARR driver addressing critical operational risk with proven enterprise willingness to pay

### 3. AI Enhancement ($200-500/user/month)
- Measured via AI Augmentation Multiplier
- Quantified through improved AI code quality and reduced hallucinations
- Long-term ARR driver as competitive advantage in AI-assisted development

As we progress through our phases, we'll track the evolution from productivity metrics to incident response and AI enhancement metrics, reflecting our growing ARR potential.

## Mid-Market Impact Metrics (Ramp-Inspired)

Based on Ramp's success with AI-powered development, we've identified key metrics that resonate with our mid-market target personas:

### Engineering Velocity Metrics
- **AI-Augmented Code Implementation**: Lines of code implemented with Arc Memory context (target: 30% increase)
- **Weekly Active Usage**: Percentage of engineering team using Arc Memory weekly (target: 50%+)
- **Incident Investigation Time**: Reduction in time spent investigating production issues (target: 40-80%)

### Incident Response Metrics (Incident.io Benchmark)
- **Mean Time To Resolution (MTTR)**: Reduction in average time to resolve incidents (target: 60%+)
- **Context Availability**: Percentage of incidents where Arc provides relevant historical context (target: 90%+)
- **Root Cause Identification**: Speed of identifying underlying causes (target: 3x faster)
- **Repeat Incident Prevention**: Reduction in similar incidents occurring multiple times (target: 80%)

### Engineering Leadership Metrics
- **Knowledge Graph Coverage**: Percentage of codebase with complete decision trails
- **Cross-Team Collaboration**: Frequency of insights spanning multiple teams' repositories
- **Architectural Decision Confidence**: Measured improvement in confidence when making architectural decisions

### Business Impact Metrics
- **Feature Delivery Acceleration**: Reduction in time from concept to production
- **Engineering Onboarding Efficiency**: Reduction in time to productivity for new team members
- **Technical Debt Visibility**: Improved identification and prioritization of technical debt

### For Our Target Personas

For senior staff engineers and engineering leads who:
- Review 5-20 PRs per week → **50% reduction in context-gathering time during reviews**
- Own domain services → **80% faster understanding of cross-service dependencies**
- Care about architectural integrity → **30% improvement in architectural decision quality**
- Value speed and safety → **40% reduction in regressions from misunderstood context**
- Struggle with context-switching → **60% faster context recovery when switching tasks**

## Hypergrowth Company Success Stories (Future)

As we build our customer base, we'll track success stories similar to Ramp's experience:

| Company | Before Arc Memory | With Arc Memory | Business Impact |
|---------|-------------------|----------------|-----------------|
| [Future] | Manual context gathering across tools | Instant context via hover cards | 40% faster PR reviews |
| [Future] | Slow incident investigation and resolution | Contextual insights during incidents | 70% faster incident resolution |
| [Future] | Limited AI code quality | AI enhanced by knowledge graph | 2x better AI suggestions |

These success stories will demonstrate Arc Memory's impact on engineering velocity, incident response, and AI enhancement—the three pillars of our ARR growth strategy.