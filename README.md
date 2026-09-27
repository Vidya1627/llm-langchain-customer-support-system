# AI Customer Support Ticket Triage & Response Router

An AI-powered customer support workflow that automatically analyzes incoming support tickets, determines their topic, sentiment, and urgency, routes them to an appropriate response flow, and refines the final response based on urgency.

The project demonstrates how multiple LLM-powered steps can be composed into a structured workflow instead of relying on a single prompt-response interaction.

## Overview

```text
Customer Support Ticket
          │
          ▼
   ┌───────────────┐
   │ Ticket Input  │
   └───────┬───────┘
           │
           ▼
   ┌─────────────────────┐
   │ Parallel Analysis   │
   │                     │
   │ • Topic             │
   │ • Sentiment         │
   │ • Urgency           │
   └─────────┬───────────┘
             │
             ▼
   ┌─────────────────────┐
   │ Conditional Routing │
   └─────────┬───────────┘
             │
             ▼
   ┌─────────────────────┐
   │ Response Generation │
   │ based on Topic      │
   └─────────┬───────────┘
             │
             ▼
   ┌─────────────────────┐
   │ Response Refinement │
   │ based on Urgency    │
   └─────────┬───────────┘
             │
             ▼
       Final Response
```

## What the System Does

Given a customer support ticket, the system:

1. Classifies the ticket topic.
2. Analyzes customer sentiment.
3. Determines the urgency level.
4. Performs the analysis steps in parallel.
5. Uses the classification result for conditional routing.
6. Generates a response using a topic-specific prompt.
7. Refines the response based on the ticket's urgency.
8. Prints the final response to the terminal.

## Key Concepts Demonstrated

### Prompt Templates

Different stages of the workflow use dedicated prompts instead of relying on one large prompt.

This makes each step easier to reason about and modify independently.

### Parallel Processing

Topic classification, sentiment analysis, and urgency detection are independent operations and can therefore be executed in parallel.

```text
                 ┌──► Topic
                 │
Ticket ──────────┼──► Sentiment
                 │
                 └──► Urgency
```

### Conditional Routing

Once the ticket topic is identified, the workflow routes the ticket to the corresponding response-generation flow.

```text
Topic
 │
 ├── Billing ───────► Billing Response
 │
 ├── Technical ────► Technical Response
 │
 ├── Account ──────► Account Response
 │
 └── General ──────► General Response
```

### Sequential Refinement

The initial response is generated first and then refined based on the urgency of the ticket.

```text
Initial Response
       │
       ▼
Urgency Information
       │
       ▼
Tone Refinement
       │
       ▼
Final Response
```

## Example

### Input

```text
I've been charged twice for my subscription and I need this fixed immediately.
```

### Workflow

```text
Topic      → Billing
Sentiment  → Negative
Urgency    → High
```

The ticket is then routed to the billing response flow and the generated response is refined to reflect the high urgency.

## Tech Stack

- Python
- LangChain
- LLM
- Prompt Templates
- Parallel Chains
- Conditional Routing
- Sequential Refinement
- Terminal / CLI

## Workflow Design

Instead of asking the model to perform everything in one prompt:

```text
Ticket → One Large Prompt → Response
```

the workflow separates the responsibilities:

```text
Ticket
  │
  ├── Topic Classification
  │
  ├── Sentiment Analysis
  │
  └── Urgency Detection
          │
          ▼
   Conditional Routing
          │
          ▼
   Response Generation
          │
          ▼
    Response Refinement
          │
          ▼
     Final Response
```

This makes the workflow easier to understand, test, and extend.

## Possible Extensions

The current project focuses on the core workflow. It could be extended with:

- Persistent ticket storage
- REST API integration
- Human-in-the-loop approval
- Retrieval-Augmented Generation (RAG) using a support knowledge base
- Conversation history
- Ticket prioritization and queue management
- Observability and LLM tracing
- Evaluation datasets for measuring classification and response quality

## Why I Built This

This project was built to explore how individual LLM capabilities can be combined into a structured AI application.

The goal wasn't to build a complete production support platform, but to understand the engineering patterns involved in designing multi-step LLM workflows.

## Author

**Vidya Paliwal**

Built as part of my hands-on exploration of Generative AI and LLM application development.
