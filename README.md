# TrabeculAI

**Composable AI infrastructure for healthcare.**

TrabeculAI is an open-source experimental framework for building modular, evidence-grounded and extensible AI systems for healthcare.

The project explores how generative AI, machine learning models, specialized healthcare tools, knowledge systems and regulatory policies can be composed into reliable AI applications.

> **Status:** Early research and development.

## Why TrabeculAI?

In anatomy, a **trabecula** is a small supporting structure. Multiple trabeculae form interconnected structures that provide support while remaining lightweight and adaptable.

TrabeculAI follows the same idea.

Rather than building a single monolithic "medical AI", the project aims to compose independent capabilities such as:

* Large Language Models and Small Language Models
* Clinical and scientific knowledge retrieval
* Medical imaging models
* Classical machine learning models
* Deep learning models
* External healthcare tools and services
* Regulatory and policy knowledge
* Specialized AI agents
* Evaluation and safety systems

These components should be replaceable and independently evaluated whenever possible.

## Vision

TrabeculAI aims to become both:

1. **A practical healthcare AI system**, initially exploring the Brazilian healthcare context.
2. **A reusable framework** for experimenting with and composing healthcare AI capabilities.

The Brazilian implementation may include knowledge about local regulations, professional guidelines and healthcare practices, while keeping those concerns modular so other jurisdictions and implementations can be added independently.

## Design principles

### Capability over provider

Applications should depend on **what a system can do**, not on the specific vendor or model implementing it.

For example:

```text
CT Lung Nodule Detection
          |
          +-- Provider A
          +-- Provider B
          +-- Open-source model
```

### Replaceable components

Models, tools, retrievers, policies and knowledge sources should be independently replaceable.

### Evaluation first

A new model, retriever, agent or provider should be introduced because measurable evidence shows that it improves the system.

### Evidence-grounded AI

Healthcare responses should be grounded in explicit and traceable sources whenever appropriate.

### Safety by design

Healthcare AI requires stronger evaluation, observability, uncertainty handling and safeguards than general-purpose applications.

### Learn by building

TrabeculAI is also an engineering laboratory for exploring the complete lifecycle of machine learning systems:

```text
data
  ↓
experimentation
  ↓
modeling
  ↓
evaluation
  ↓
serving
  ↓
monitoring
  ↓
iteration
```

## Architecture

The architecture is intentionally evolving.

The current direction is based on a small core capable of composing:

```text
                  TrabeculAI
                       |
               Core / Runtime
                       |
       +---------------+---------------+
       |               |               |
    Agents        Capabilities       Policies
       |               |               |
       |          +----+----+          |
       |          |         |          |
       |       Models     Tools      Knowledge
       |          |         |          |
       +----------+---------+----------+
                       |
                    Evals
```

Concrete abstractions will be introduced only when supported by real use cases.

## Engineering roadmap

The project will evolve through incremental vertical slices covering different areas of Machine Learning Engineering, including:

* Machine learning fundamentals
* Information retrieval and embeddings
* Deep learning
* LLM engineering
* Agentic systems
* Evaluation
* MLOps
* Model serving
* Monitoring
* Cloud architecture

See [`docs/roadmap.md`](docs/roadmap.md).

## Disclaimer

TrabeculAI is an experimental research and engineering project.

It is **not a medical device**, has not been clinically validated, and must not be used to diagnose, treat or make clinical decisions about patients.

Any future clinical use would require appropriate validation, governance, regulatory assessment and professional oversight.

## License

TrabeculAI is licensed under the Apache License 2.0.
