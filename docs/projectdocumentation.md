# Project Documentation: Kasparro Agentic Content System

## 1. Problem Statement
Design a modular, automated agentic system to transform raw product data (GlowBoost Serum) into structured content formats (FAQ, Product Page, Comparison) without manual intervention.

## 2. Solution Overview
I implemented a **Multi-Agent Orchestration Graph** using Python and LangChain. The system ingests raw JSON data, normalizes it into Pydantic models, and dispatches tasks to specialized agents (Insight Agent, Marketing Agent, Strategy Agent).

## 3. System Design (Architecture)
The system follows a **Hub-and-Spoke Orchestration Pattern**:

1.  **Data Layer:** Uses Pydantic to enforce type safety on Input and Output.
2.  **Logic Layer:** Stores reusable prompt logic.
3.  **Agent Layer:** Specialized agents for distinct content tasks.

### Execution Flow Diagram
```mermaid
sequenceDiagram
    participant Main as Orchestrator (Main.py)
    participant Data as Data Layer
    participant Agent1 as Insight Agent
    participant Agent2 as Marketing Agent
    participant Agent3 as Strategy Agent
    participant File as File System

    Main->>Data: Validate Raw Input (Pydantic)
    Data-->>Main: Structured Product Object

    par Parallel Execution potential
        Main->>Agent1: Request FAQs
        Agent1->>Agent1: Generate Qs -> Answer Qs
        Agent1-->>Main: FAQPage Object
        
        Main->>Agent2: Request Product Page
        Agent2->>Agent2: Draft Copy -> Format JSON
        Agent2-->>Main: ProductPage Object
        
        Main->>Agent3: Request Comparison
        Agent3->>Agent3: Invent Competitor -> Build Matrix
        Agent3-->>Main: ComparisonPage Object
    end

    Main->>File: Write faq.json
    Main->>File: Write product_page.json
    Main->>File: Write comparison_page.json
