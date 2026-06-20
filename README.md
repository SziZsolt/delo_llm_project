# Gloomhaven Agentic RAG System

## Overview

This project implements an agentic AI system capable of answering questions about gameplay situations in the board game **Gloomhaven**.

The solution combines:

- Retrieval-Augmented Generation (RAG)
- Local rulebook-based reasoning
- Web-search fallback
- Structured JSON responses
- Evaluation on a synthetic dataset

---

## Architecture

### High-Level Workflow

```text
User Question
       │
       ▼
      Agent
       │
       ▼
 Local Rulebook RAG
       │
       ▼
Retrieval Confidence Check
       │
 ┌─────┴─────┐
 │           │
 ▼           ▼
Sufficient   Insufficient
 Context      Context
 │             │
 ▼             ▼
Local RAG   Web RAG
 │             │
 └─────┬──────┘
       ▼
      LLM
       ▼
Structured JSON Answer
```

## Project Structure

```text
src/
└── gloomhaven_agent/
    ├── document_processing/
    ├── rag/
    ├── retrieval/
    └── tools/

data/
    ├── rulebook.pdf
    ├── eval_dataset.json
    └── eval_predictions.json
```

## Components

### Document Processing

- PDF parsing using PyPDF
- Text cleaning and normalization
- Fixed-size overlapping chunking

### Retrieval

- HuggingFace embeddings
- Vector similarity search using cosine similarity
- Top-k context retrieval

### RAG Engines

#### LocalRAGEngine

Uses the Gloomhaven rulebook as the primary source of knowledge.

#### WebRAGEngine

Uses online search results when the local rulebook cannot provide a reliable answer.

### Agent

1. Query the local rulebook RAG.
2. Evaluate retrieval confidence.
3. If necessary, perform web search.
4. Generate a structured answer.

## Output Format

```json
{
  "explanation": "...",
  "was_played_correctly": true,
  "category": "Combat",
  "source_type": "rulebook"
}
```

Categories:

- BoardGameSetup
- Combat
- Scenario
- Character

## Models

### Embedding Model

- Qwen/Qwen3-Embedding-0.6B

### Language Model

- Qwen/Qwen3-1.7B

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Evaluation

Metrics:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrices


## Conclusion

The developed system successfully combines:
- Retrieval-Augmented Generation
- Rulebook-based reasoning
- Web-search fallback

Evaluation results indicate that retrieval quality is strong, while most remaining errors originate from the reasoning limitations of the small local language model.