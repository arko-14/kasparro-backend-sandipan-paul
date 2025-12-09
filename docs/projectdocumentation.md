# Project Documentation: Kasparro Agentic Content System

## 1. Problem Statement
Design a modular, automated agentic system to transform raw product data (GlowBoost Serum) into structured content formats (FAQ, Product Page, Comparison) without manual intervention.

## 2. Solution Overview
I implemented a **Multi-Agent Orchestration Graph** using Python and LangChain. The system ingests raw JSON data, normalizes it into Pydantic models, and dispatches tasks to three specialized agentic workflows.

## 3. System Design (Architecture)
The system follows a **Hub-and-Spoke Orchestration Pattern** with three primary agents defined in `src/agents.py`:

1.  **The FAQ Agent:**
    * **Role:** Simulates customer curiosity and support.
    * **Workflow:** First acts as a user to generate relevant questions, then switches roles to answer them based strictly on product facts.
2.  **The Product Page Agent:**
    * **Role:** Acts as a Marketing Copywriter.
    * **Workflow:** Transforms dry technical specs into persuasive, benefit-driven copy formatted for a landing page.
3.  **The Comparison Agent:**
    * **Role:** Acts as a Competitor Analyst.
    * **Workflow:** Hallucinates a realistic fictional competitor node, then builds a row-by-row comparison matrix against the main product.

### Execution Flow Diagram
```mermaid
sequenceDiagram
    participant Main as Orchestrator
    participant FAQ as FAQ Agent
    participant Prod as Product Page Agent
    participant Comp as Comparison Agent
    participant File as File System

    Main->>Main: Ingest & Validate Data

    par Parallel Execution
        Main->>FAQ: Task: Generate Q&A
        FAQ->>FAQ: Generate Qs -> Answer Qs
        FAQ-->>Main: Return FAQPage Object
        
        Main->>Prod: Task: Create Landing Page
        Prod->>Prod: Draft Copy -> Format JSON
        Prod-->>Main: Return ProductPage Object
        
        Main->>Comp: Task: Compare Products
        Comp->>Comp: Create Competitor -> Matrix
        Comp-->>Main: Return ComparisonPage Object
    end

    Main->>File: Save json files
