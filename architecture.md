# Architecture

```mermaid
flowchart TD
    A[ICSR CSV Dataset] --> B[Loader]
    B --> C[Validation and Normalization]
    C --> D[Deterministic Analysis]

    D --> E[Evidence Builder]
    E --> F[Section Context Builder]
    F --> G[LLM]

    G --> H[Generated Sections]
    H --> I[Validation / Grounding Check]
    I --> J{Human Review}

    J -->|Approve| K[Final PADER-style Report]
    J -->|Flag| L[Regenerate / Revise]
    L --> F

    D --> M[analysis.json]
    E --> N[evidence.json]
    I --> O[validation.json]
```

## Core design decision

Python owns arithmetic and data aggregation. The LLM receives only scoped,
approved evidence for the section it is writing.

The raw CSV is never sent directly to the LLM.
