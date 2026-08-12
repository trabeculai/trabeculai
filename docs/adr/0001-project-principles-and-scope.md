# ADR 0001: Project Principles and Scope

- Status: Accepted
- Date: 2026-08-11

## Context

TrabeculAI is an experimental open-source project for building and studying
composable AI systems for healthcare.

The project has two complementary goals:

1. Build practical healthcare AI applications.
2. Provide a reusable framework for composing and evaluating AI capabilities.

Healthcare AI systems may combine multiple forms of intelligence and external
resources, including large language models, small language models, classical
machine learning models, deep learning models, medical imaging systems,
retrieval systems, external tools, regulatory knowledge, and specialized
agents.

Some of these capabilities may be implemented directly by TrabeculAI, while
others may be provided by third-party systems.

The project will initially explore the Brazilian healthcare context, including
local scientific, professional, legal, and regulatory sources. However,
jurisdiction-specific knowledge must not become a hard dependency of the core
framework.

TrabeculAI is also intended to serve as an engineering laboratory for studying
the complete lifecycle of machine learning systems, including data,
experimentation, modeling, evaluation, serving, observability, and MLOps.

Because the project is in an early research stage, prematurely defining a large
framework architecture would create abstractions without evidence that they are
necessary.

## Decision

TrabeculAI will follow the principles below.

### 1. Capabilities are more important than providers

Applications should depend on what the system is capable of doing rather than
on the specific implementation that performs the task.

For example, a medical imaging capability may eventually be implemented by:

- a model developed inside TrabeculAI;
- an open-source model;
- a commercial healthcare AI provider;
- or another external service.

Providers should therefore be replaceable whenever practical.

### 2. Architecture will emerge from vertical slices

TrabeculAI will not attempt to define the complete framework architecture
upfront.

New abstractions such as agents, providers, capabilities, packs, runtimes, or
plugin interfaces should be introduced only when concrete use cases demonstrate
their necessity.

Each major architectural abstraction should preferably originate from at least
one working implementation.

### 3. Evaluation comes before abstraction

New models, retrievers, agents, routing strategies, or providers should not be
introduced only because they are technically interesting.

Whenever possible, changes involving AI behavior should answer a measurable
question or hypothesis.

Examples include comparing:

- retrieval strategies;
- embedding models;
- classical ML models;
- deep learning architectures;
- LLMs and SLMs;
- routing approaches;
- single-agent and multi-agent architectures;
- local and external capability providers.

Evaluation should be treated as a core part of the system rather than an
afterthought.

### 4. Machine learning must remain a first-class concern

TrabeculAI must not become only a backend framework that orchestrates external
AI APIs.

The project should include capabilities in which models are trained, evaluated,
versioned, deployed, and monitored as part of the repository's learning and
engineering goals.

Generative AI and agentic systems are a primary specialization of the project,
but they should coexist with broader Machine Learning Engineering practices.

### 5. Domain knowledge is modular

Scientific evidence, clinical guidelines, regulations, professional rules, and
jurisdiction-specific knowledge should be independently replaceable or
extensible.

The Brazilian healthcare context will be the first practical implementation,
but the core architecture should not assume that Brazil is the only supported
jurisdiction.

### 6. Safety and traceability are architectural concerns

Healthcare applications require stronger controls than general-purpose AI
applications.

Where appropriate, the system should make it possible to trace:

- which model produced a result;
- which provider implemented a capability;
- which evidence or knowledge was retrieved;
- which tools were called;
- which configuration was active;
- and which version of a component participated in a decision.

Safety, uncertainty, observability, and evaluation should influence
architecture from the beginning.

### 7. TrabeculAI is experimental software

TrabeculAI is not a medical device and is not clinically validated.

The project must not present experimental outputs as approved medical diagnosis
or treatment recommendations.

Any future use in clinical environments would require appropriate technical,
clinical, legal, regulatory, and governance assessment.

## Consequences

This decision intentionally favors evolutionary architecture over upfront
framework design.

Early versions of TrabeculAI may contain fewer abstractions and more concrete
implementations than a mature framework.

Some components may be refactored or replaced as experiments reveal better
boundaries.

The project will prioritize measurable learning, reproducibility, and
engineering evidence over feature count.

Future ADRs should document significant architectural decisions as they emerge
from real project requirements.
