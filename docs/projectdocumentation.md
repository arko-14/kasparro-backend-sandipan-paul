# Project Documentation: Kasparro Agentic Content System

## 1. Problem Statement
Design a modular, automated agentic system to transform raw product data (GlowBoost Serum) into structured content formats (FAQ, Product Page, Comparison) without manual intervention.

## 2. Solution Overview
I implemented a **Multi-Agent Orchestration Graph** using Python and LangChain. The system ingests raw JSON data, normalizes it into Pydantic models, and dispatches tasks to three specialized agentic workflows defined in `src/agents.py`.

## 3. System Design (Architecture)
The system follows a **Hub-and-Spoke Orchestration Pattern**. The `AgentOrchestrator` class manages three distinct agents:

1.  **FAQ Agent (`generate_faqs`)**: 
    * Internally chains two steps: first generating user questions, then answering them to create a complete Q&A set.
2.  **Product Page Agent (`generate_product_page`)**:
    * Uses a strict Pydantic parser to transform technical data into a marketing-ready JSON structure.
3.  **Comparison Agent (`generate_comparison`)**:
    * First invents a fictional competitor product, then runs a comparison logic block to generate a matrix.

### Execution Flow Diagram
```mermaid
sequenceDiagram
    participant Main as Orchestrator (main.py)
    participant FAQ as FAQ Agent
    participant Prod as Product Page Agent
    participant Comp as Comparison Agent
    participant File as File System

    Main->>Main: Ingest & Validate Data

    rect rgb(240, 248, 255)
    Note over Main, Comp: Parallel Agent Execution
    
    Main->>FAQ: generate_faqs(product)
    FAQ->>FAQ: Step 1: Generate Questions<br/>Step 2: Answer Questions
    FAQ-->>Main: Returns FAQPage JSON

    Main->>Prod: generate_product_page(product)
    Prod->>Prod: Draft Content & Format
    Prod-->>Main: Returns ProductPage JSON

    Main->>Comp: generate_comparison(product)
    Comp->>Comp: Step 1: Create Competitor<br/>Step 2: Build Matrix
    Comp-->>Main: Returns ComparisonPage JSON
    end

    Main->>File: Save .json files
