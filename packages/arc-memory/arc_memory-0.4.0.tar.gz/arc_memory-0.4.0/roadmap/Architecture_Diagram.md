# Arc Memory Architecture & Roadmap Diagrams

## System Architecture Diagram

This diagram shows how all components of Arc Memory connect together, from current implementation to research vision.

```mermaid
graph TB
    %% Current Implementation Components
    subgraph "Current Implementation"
        CLI["Arc Memory CLI/SDK<br>(Core Python Package)"]
        DB[(Local SQLite<br>Knowledge Graph)]
        Daemon["Arc Daemon<br>(HTTP Service)"]
        GHExt["GitHub Chrome Extension<br>(Primary Focus)"]
        MCP["Arc MCP Server<br>(AI Assistant Integration)"]

        %% Data Sources
        subgraph "Data Sources"
            Git["Git Repository"]
            GitHub["GitHub<br>(PRs, Issues)"]
            ADRs["Architecture<br>Decision Records"]
            Linear["Linear<br>(Issues, Projects)"]
        end

        %% Connections between current components
        Git --> CLI
        GitHub --> CLI
        ADRs --> CLI
        Linear --> CLI

        CLI --> DB
        DB --> Daemon
        Daemon --> GHExt
        DB --> MCP
    end

    %% Research Vision Components
    subgraph "Research Vision"
        TKG["Temporal Knowledge Graph<br>(Enhanced)"]
        CRDT["Causal CRDT Layer"]
        RL["Provenance-Driven RL"]
        Agents["Multi-Agent<br>Orchestration"]

        %% Connections between research components
        TKG --> CRDT
        CRDT --> RL
        RL --> Agents
    end

    %% Evolution Path
    DB -.-> TKG
    GHExt -.-> TKG

    %% User Interfaces
    subgraph "User Interfaces"
        PR["PR Review<br>(Current Focus)"]
        CLI_UI["Command Line<br>Interface"]
        Future_IDE["Future IDE<br>Integration"]
    end

    %% Connection to User Interfaces
    GHExt --> PR
    CLI --> CLI_UI
    Agents -.-> Future_IDE

    %% Business Value
    subgraph "Value Delivery"
        ProductivityValue["Team Productivity<br>($10-20/user/month)"]
        IncidentValue["Incident Response<br>($20-30/user/month)"]
        AIValue["AI Enhancement<br>($20-30/user/month)"]
    end

    %% Connection to Business Value
    PR --> ProductivityValue
    TKG --> IncidentValue
    RL --> AIValue

    %% Target Personas
    subgraph "Target Personas"
        MidMarket["Mid-Market<br>(50-100 engineers)"]
        EarlyStage["Early-Stage Startups<br>(5-10 developers)"]
    end

    %% Connection to Target Personas
    ProductivityValue --> MidMarket
    IncidentValue --> MidMarket
    AIValue --> MidMarket
    ProductivityValue --> EarlyStage

    %% Design Partners
    subgraph "Design Partners"
        Quicknode["Quicknode"]
        ProtocolLabs["Protocol Labs"]
        NEAR["NEAR Protocol"]
    end

    %% Connection to Design Partners
    MidMarket --> Quicknode
    MidMarket --> ProtocolLabs
    MidMarket --> NEAR

    %% Legend
    classDef current fill:#d4f1f9,stroke:#05728f,stroke-width:2px
    classDef research fill:#ffe6cc,stroke:#d79b00,stroke-width:2px
    classDef sources fill:#d5e8d4,stroke:#82b366,stroke-width:2px
    classDef interfaces fill:#e1d5e7,stroke:#9673a6,stroke-width:2px
    classDef value fill:#fff2cc,stroke:#d6b656,stroke-width:2px
    classDef personas fill:#f8cecc,stroke:#b85450,stroke-width:2px
    classDef partners fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px

    class CLI,DB,Daemon,GHExt,MCP current
    class TKG,CRDT,RL,Agents research
    class Git,GitHub,ADRs,Linear sources
    class PR,CLI_UI,Future_IDE interfaces
    class ProductivityValue,KnowledgeValue,AIValue value
    class MidMarket,EarlyStage personas
    class Quicknode,ProtocolLabs,NEAR partners
```

## Product Roadmap Timeline

This diagram shows the evolution of Arc Memory from current focus to long-term vision.

```mermaid
gantt
    title Arc Memory Product Roadmap
    dateFormat  YYYY-MM
    axisFormat %b %Y

    section Current Focus (0-3 months)
    Arc Daemon Implementation       :active, daemon, 2025-01, 3M
    GitHub Extension MVP            :active, gh_ext_mvp, 2025-01, 3M
    Hover Card Functionality        :active, hover, 2025-01, 2M
    Graph Building UI               :active, graph_build, 2025-02, 2M
    Basic Search Interface          :search, 2025-03, 1M

    section Near-Term (3-6 months)
    Extension Refinement            :ext_refine, after gh_ext_mvp, 3M
    Enhanced Search                 :after search, 2M
    Simulation Capabilities         :sim, 2025-04, 3M
    Community Building              :community, 2025-04, 3M
    Data Flywheel Refinement        :flywheel, 2025-05, 2M

    section Mid-Term (6-12 months)
    Single-Agent Assistance         :agent, after flywheel, 3M
    Predictive Insights             :predict, after sim, 3M
    Cross-Repository Context        :cross_repo, 2025-07, 3M
    Team Collaboration Features     :collab, 2025-08, 4M

    section Long-Term Vision (12+ months)
    Temporal Knowledge Graph Enhancements :tkg, 2026-01, 6M
    Causal CRDT Implementation      :crdt, after tkg, 6M
    Provenance-Driven RL Framework  :rl, after crdt, 6M
    Multi-Agent Orchestration       :multi_agent, after rl, 6M

    section Monetization Path
    Team Productivity ($10-20/user/month)    :milestone, m1, 2025-04, 0d
    Incident Response ($20-30/user/month) :milestone, m2, 2025-10, 0d
    AI Enhancement ($10-20/user/month)      :milestone, m3, 2026-07, 0d
```

## Data Flywheel Diagram

This diagram illustrates how Arc Memory creates a reinforcing data flywheel.

```mermaid
flowchart TD
    %% Data Flywheel
    A["Users adoptGitHub Extension"] --> B["Knowledge graphs are built"]
    B --> C["Decision trails become richer"]
    C --> D["Data quality improves"]
    D --> E["RL agents learn from this data"]
    E --> F["User trust increases"]
    F --> A

    %% Stages of Evolution
    S1["Stage 1: Ambient Context<br>(Current)"]
    S2["Stage 2: Predictive Insights"]
    S3["Stage 3: Agent Assistance"]
    S4["Stage 4: Multi-Agent Collaboration<br>(Research Vision)"]

    S1 --> S2
    S2 --> S3
    S3 --> S4

    %% Connections between flywheel and stages
    A --> S1
    C --> S2
    E --> S3
    F --> S4

    %% Styling
    classDef flywheel fill:#d4f1f9,stroke:#05728f,stroke-width:2px
    classDef stages fill:#ffe6cc,stroke:#d79b00,stroke-width:2px

    class A,B,C,D,E,F flywheel
    class S1,S2,S3,S4 stages

    %% Group nodes into subgraphs
    subgraph Flywheel["Data Flywheel"]
        A
        B
        C
        D
        E
        F
    end

    subgraph Evolution["Stages of Evolution"]
        S1
        S2
        S3
        S4
    end
```
