# Architecture

MedTwin Student is organized as a modular monorepo so the MVP can grow without forcing early architectural churn.

## Backend Modules

- Student Profile Engine: stores cycle, strengths, vulnerabilities, preferences, and concept-level mastery estimates.
- Curriculum Knowledge Graph: represents concepts and prerequisite edges across basic sciences, clinical sciences, and internship.
- Clinical Case Generator: starts with static chest pain seed cases; later can generate variants with an AI provider and validation rubric.
- Socratic Tutor Agent: produces a next-question prompt based on detected gaps and bias risk.
- Assessment Engine: analyzes learner responses against case requirements and expected reasoning steps.
- Learning Simulation Engine: emits projected mastery deltas after an attempt.
- Teacher Dashboard: exposes summarized gaps, bias risks, and recommended activities to the frontend.

## AI Strategy

The MVP reasoning engine is deterministic for traceability. The `OpenAICompatibleClient` isolates model-provider details and can enrich feedback, generate case variants, or produce Socratic dialogue while preserving the same API contracts.

## Data Model

The database schema uses JSONB for flexible MVP attributes and pgvector columns for later semantic search over concepts and cases. As usage stabilizes, high-value JSON fields can be normalized.

## Expansion Path

1. Persist attempts and simulation deltas after each analysis.
2. Add authentication and teacher cohort management.
3. Replace static case seeds with a validated case-generation workflow.
4. Add embedding search for remediation resources and similar prior attempts.
5. Introduce longitudinal mastery models by concept, cycle, and rotation.

