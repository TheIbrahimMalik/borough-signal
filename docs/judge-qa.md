# BoroughSignal Judge Q&A

## Why is this a knowledge graph project?

We model proposals, issues, segments, responses, and evidence as structured entities in SurrealDB, and we use graph relationships like:

- proposal -> AFFECTS -> issue
- segment -> CARES_ABOUT -> issue
- response -> CITES -> evidence

That lets us explain not just the result, but the structured path behind the result.

## Why support / oppose?

Overall sentiment is computed from the distribution of segment-level reactions.

Each segment gets a structured score based on:

- proposal features
- borough context
- issue sensitivities

The final support / mixed / oppose label is an aggregate of those segment outcomes.

## Why can a proposal be oppose with high signal strength?

Signal strength does not mean support. It reflects how much structured evidence and modeled context the system has for a proposal.

A proposal can have strong signal but still score negatively if the segment-level tradeoffs are unfavorable.

## Why use LangGraph?

LangGraph gives us a stateful workflow rather than a one-shot response.

Our workflow is:

1. parse proposal
2. retrieve context
3. simulate segments
4. persist run

That makes the system inspectable, repeatable, and easier to trace in LangSmith.

## Why use SurrealDB?

SurrealDB stores both structured records and graph relationships in one place.

We use it to persist:

- proposals
- simulation runs
- responses
- recommendations
- issues
- evidence
- graph edges between them

## What makes this useful in the real world?

Planning teams often need a fast way to pressure-test proposals before formal consultation.

BoroughSignal helps them simulate likely reactions, understand which issues drive those reactions, and compare an original proposal against an improved version.

## What is the difference between overall sentiment and signal strength?

Overall sentiment is the aggregate direction of audience reaction: support, mixed, or oppose.

Signal strength is separate. It reflects how much structured evidence and modeled context the system had for the analysis.

So a proposal can be oppose with high signal strength if the system found strong structured evidence for a negative reaction.

## What is the difference between overall sentiment and signal strength?

Overall sentiment is the aggregate direction of audience reaction: support, mixed, or oppose.

Signal strength is separate. It reflects how much structured evidence and modeled context the system had for the analysis.

So a proposal can be oppose with high signal strength if the system found strong structured evidence for a negative reaction.

## What are the numerical mappings?

At the segment level:

- `score >= 0.75` means support
- `0.50 <= score < 0.75` means mixed
- `score < 0.50` means oppose

At the overall level, BoroughSignal aggregates segment stances using:

- support = +1
- mixed = 0
- oppose = -1

Signal strength is different. It is a `0–1` measure of how much structured signal the system had for the analysis, not a probability that the result is support.
