# TrabeculAI Engineering Roadmap

TrabeculAI is developed incrementally through vertical slices.

Each milestone should produce a working capability while exploring and evaluating a specific area of Machine Learning Engineering.

The roadmap is intentionally evolutionary. Architecture should emerge from working systems and measured experiments rather than upfront abstraction.

---

## Phase 0 — Foundation

### Goal

Establish the minimum engineering foundation for the project.

### Deliverables

* Python package
* Automated tests
* Linting and type checking
* CI pipeline
* Basic documentation
* Architecture Decision Records (ADRs)

### Engineering concepts

* Python packaging
* Software design
* Testing
* Reproducibility
* CI/CD fundamentals

---

## Phase 1 — Evidence Retrieval

### Goal

Build the first useful healthcare AI capability: retrieving relevant scientific and clinical evidence.

### Initial system

```text
Question
   ↓
Retrieval
   ↓
Relevant documents
   ↓
LLM
   ↓
Grounded answer + sources
```

### Experiments

Compare:

* lexical retrieval (BM25)
* dense retrieval
* different embedding models
* hybrid retrieval
* reranking strategies

### Evaluation

Explore metrics such as:

* Recall@K
* Precision@K
* MRR
* NDCG
* citation correctness
* groundedness

### ML concepts

* Embeddings
* Information retrieval
* Transformers
* Ranking
* Representation learning
* Offline evaluation

---

## Phase 2 — Classical Machine Learning

### Goal

Introduce the first ML capability trained inside TrabeculAI.

Use a public healthcare dataset to build a supervised prediction problem.

### Experiments

Compare models such as:

* Logistic Regression
* Decision Trees
* Random Forest
* Gradient Boosting

### Evaluation

Study:

* train / validation / test strategy
* cross-validation
* class imbalance
* precision and recall
* ROC-AUC
* PR-AUC
* calibration
* threshold selection
* data leakage
* bias and variance

### ML concepts

* Supervised learning
* Feature engineering
* Model selection
* Statistical evaluation
* Explainability

---

## Phase 3 — Deep Learning

### Goal

Introduce a deep-learning-based healthcare capability.

An initial candidate is medical imaging using a public dataset.

### Experiments

Explore:

* CNN architectures
* Vision Transformers
* transfer learning
* freezing and fine-tuning
* data augmentation
* different losses and optimizers

### Evaluation

Study:

* learning curves
* overfitting
* calibration
* class imbalance
* inference latency
* model size
* GPU utilization

### ML concepts

* Neural networks
* Optimization
* Backpropagation
* Representation learning
* Transfer learning
* GPU inference

---

## Phase 4 — LLM Engineering

### Goal

Turn the language layer into an evaluated ML system rather than a simple API integration.

### Experiments

Compare:

* different LLMs
* large vs small models
* zero-shot vs few-shot prompting
* retrieval-augmented generation
* structured outputs
* fine-tuning when justified

### Evaluation

Measure:

* task success
* factual correctness
* groundedness
* hallucination rate
* latency
* token usage
* cost

### ML concepts

* Transformer inference
* Prompt experimentation
* Model selection
* Fine-tuning
* Evaluation of non-deterministic systems

---

## Phase 5 — Agentic Systems

### Goal

Introduce orchestration only after individual capabilities can be independently evaluated.

### Possible components

* planner
* clinical agent
* evidence agent
* regulatory agent
* safety agent

### Experiments

Compare:

* deterministic routing
* LLM routing
* classifier-based routing
* single-agent systems
* multi-agent systems
* sequential execution
* parallel execution
* handoffs

### Evaluation

Measure:

* tool selection accuracy
* routing accuracy
* task completion
* unnecessary tool calls
* latency
* cost
* failure recovery

### ML concepts

* Agent architecture
* Tool use
* Routing
* Decision systems
* LLM evaluation

---

## Phase 6 — Extensible Capabilities

### Goal

Turn proven components into replaceable implementations.

Example:

```text
Capability
    |
    +-- Provider A
    +-- Provider B
    +-- Local model
```

Possible capabilities include:

* medical imaging
* laboratory analysis
* risk prediction
* evidence retrieval
* regulatory knowledge

### Engineering concepts

* Contracts
* Dependency inversion
* Plugin architecture
* Model/provider abstraction
* Service boundaries

---

## Phase 7 — ML Lifecycle and MLOps

### Goal

Operationalize models developed by the project.

### Pipeline

```text
Data ingestion
      ↓
Data validation
      ↓
Preprocessing
      ↓
Training
      ↓
Evaluation
      ↓
Model registry
      ↓
Deployment
      ↓
Monitoring
```

### Topics

* dataset versioning
* experiment tracking
* model registry
* model lineage
* reproducibility
* automated training
* model promotion
* rollback
* batch inference
* online inference

### ML concepts

* MLOps
* ML pipelines
* Model lifecycle
* Reproducibility
* Production ML

---

## Phase 8 — Monitoring and Continuous Evaluation

### Goal

Evaluate both traditional ML and generative AI after deployment.

### Monitor

* input distributions
* prediction distributions
* data drift
* concept drift
* model performance
* retrieval quality
* agent behavior
* latency
* errors
* cost

### Advanced topics

* human feedback
* evaluation datasets
* production traces
* champion/challenger models
* shadow deployments
* automated regression evaluation

---

## Phase 9 — Production Architecture

### Goal

Design and deploy TrabeculAI as a production-grade ML system.

### Topics

* AWS architecture
* infrastructure as code
* model serving
* autoscaling
* asynchronous inference
* GPU workloads
* observability
* reliability
* security
* privacy
* cost optimization

---

## Long-term research directions

Potential areas include:

* multimodal models
* medical vision-language models
* small language models
* encoder-based routing
* fine-tuning
* distillation
* quantization
* model optimization
* human-in-the-loop systems
* uncertainty estimation
* explainability
* federated learning
* privacy-preserving ML
* reinforcement learning
* regulatory-aware AI systems

---

## Guiding question

Every new feature should answer:

> **What ML or system hypothesis are we testing?**

The project should prefer measurable experiments over adding technology for its own sake.
