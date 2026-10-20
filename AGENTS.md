# Agent Instructions

## Project Overview

**Project:** Databricks Certification Study Agent  
**Repository:** `databricks-certification-study-agent`

Build a Databricks-native retrieval-augmented generation (RAG) study assistant focused initially on the Databricks Certified Data Engineer Associate certification.

The project is both a functional application and a hands-on learning experience for Databricks data engineering, software engineering, and AI/ML concepts.

The application should help users study certification material by retrieving relevant information from an indexed knowledge base and generating grounded answers with source references.

## Development Philosophy

- Prioritize understanding over implementation speed.
- Keep the architecture simple, modular, and maintainable.
- Prefer native Databricks capabilities over unnecessary third-party frameworks.
- Avoid adding abstractions, services, or dependencies without a clear reason.
- Implement functionality incrementally, with tests where appropriate.
- Explain significant architectural decisions and tradeoffs.
- Do not generate large amounts of implementation code without explicit authorization.
- When guiding implementation, provide explanations, relevant documentation, and small learning objectives rather than complete solutions by default.
- Do not repeat completed milestones or implementation steps.
- Do not replace existing implementations without first reviewing them.
- Distinguish between implemented functionality, agreed architecture, and future plans.

## Learning-First Workflow

This project follows a mandatory learning-first development process.

When introducing a new concept, technology, or significant design decision:

1. Explain the concept and why it matters to this project.
2. Provide relevant official documentation or learning resources.
3. Ask at least three relevant assessment questions.
4. Wait for the developer's answers before proceeding.
5. Evaluate each answer individually and explain any misunderstandings.
6. Ask follow-up questions when necessary.
7. Once understanding is demonstrated, assign a small implementation task.
8. Allow the developer to write the implementation independently.
9. Review the submitted implementation for correctness, maintainability, and alignment with the architecture.
10. Request appropriate tests and validation.
11. Explicitly identify the next Git checkpoint.
12. Continue to the next substep only after the current step is complete.

Do not provide full copy-paste implementations unless explicitly requested.

Avoid repeatedly assessing concepts the developer has already demonstrated understanding of unless new requirements introduce meaningful differences.

## Technology Stack

- **Language:** Python 3.12
- **Development environment:** macOS, Neovim, WezTerm
- **Cloud platform:** Databricks Free Edition
- **Data storage:** Unity Catalog and Delta tables
- **File ingestion:** Auto Loader
- **Orchestration:** Lakeflow Jobs
- **Declarative pipelines:** Lakeflow Spark Declarative Pipelines
- **Retrieval:** Databricks-managed vector search capabilities, subject to availability
- **LLM inference:** Databricks Foundation Model APIs, subject to availability
- **Application:** Streamlit deployed through Databricks Apps, subject to availability
- **Experiment tracking and evaluation:** MLflow
- **CI:** GitHub Actions
- **Deployment configuration:** Databricks Declarative Automation Bundles
- **Testing:** pytest
- **Linting and formatting:** Ruff
- **Packaging:** setuptools with a `src/` layout

Verify service availability and Free Edition limitations before implementing Databricks-dependent features.

## Architecture

The intended application follows a retrieval-augmented generation workflow:

1. Ingest certification study documents.
2. Preserve raw source documents and metadata.
3. Extract and normalize document content.
4. Split documents into retrievable chunks.
5. Generate embeddings and configure retrieval.
6. Retrieve relevant chunks for a user question.
7. Generate answers grounded in retrieved context.
8. Present answers and source references through the application.
9. Evaluate retrieval quality and answer quality.

Prefer clear boundaries between ingestion, retrieval, generation, evaluation, and application components.

### Medallion Architecture

**Bronze**

- `documents_raw`: Original document bytes, source information, and observed document versions.
- `document_metadata`: Logical document identity and source metadata.

**Silver**

- `documents_processed`: Extracted and normalized document text, associated with document identity and the relevant source version.

**Gold**

- `document_chunks`: Retrieval-ready text chunks and associated metadata.

These table responsibilities are agreed architectural intentions. Do not assume every table has already been implemented.

### Document Identity

The agreed logical identity design is:

- A document receives a UUID4 when first registered.
- The same logical document retains its UUID when its contents change at the same source path.
- `file_path` is the V1 logical document lookup key.
- `document_metadata` is the authoritative source of the `file_path` to `document_id` mapping.
- `documents_raw` preserves raw source information and observed versions.
- Reprocessing an existing document must not create another logical document identity.
- A renamed or moved document may be treated as a new document in V1.
- `content_hash` identifies source content, not logical document identity.

The registration mechanism is **not yet implemented**.

### Document Versioning

The intended behavior is:

- Preserve observed document versions in Bronze.
- Reuse the logical document ID when the file changes.
- Use content hashes to distinguish changed content.
- Maintain current document metadata separately from raw version history.
- Avoid unnecessary downstream reprocessing of unchanged content.

Auto Loader does not automatically guarantee preservation of every overwrite or intermediate file version. Version discovery, ordering, and retention behavior must be designed and validated.

### Timestamps

Distinguish:

- `ingested_at`: When an observed document version enters Bronze.
- `registered_at`: When the logical document is first registered.
- `last_ingested_at`: When the latest observed version entered Bronze.
- `modification_time`: The source file's modification timestamp.

Use timezone-aware UTC timestamps.

The existing Python metadata model still contains `ingested_at`. Its reconciliation with the updated architecture is pending.

### Processing and Orchestration

Use Lakeflow Jobs for:

- Task orchestration and dependencies.
- Conditional execution when appropriate.
- Transient task failure retries.
- Coordinating ingestion, registration, and downstream processing.

Use Lakeflow Spark Declarative Pipelines for:

- Incremental data ingestion.
- Spark transformations.
- Managed data dependencies.
- Data quality expectations where useful.

Do not create a custom Python document-status state machine unless a concrete requirement justifies it.

The existing `DocumentStatus` enum is retained for now, but its future use is undecided.

Distinguish task-level failures from individual document-processing failures.

### CDC and AUTO CDC

- Delta Change Data Feed and AUTO CDC are not automatically required simply because Bronze preserves document versions.
- An append-only history of observed files is not automatically a semantic document CDC event stream.
- AUTO CDC may be considered if properly keyed and sequenced change events are introduced.
- Prefer the simplest reliable approach that satisfies V1 requirements.
- Do not implement AUTO CDC without first demonstrating why it is needed.

## Repository Conventions

- Keep application code inside `src/study_agent/`.
- Keep automated tests inside `tests/`.
- Use Python modules (`.py`) for application logic.
- Avoid notebooks unless they provide a clear Databricks-specific benefit.
- Keep configuration separate from application logic.
- Never commit credentials, access tokens, secrets, or environment-specific private data.
- Avoid committing generated datasets, large artifacts, or temporary files.
- Use `pyproject.toml` for Python project configuration.

## Python Development

- Target Python 3.12.
- Use a local virtual environment for development.
- Install the project in editable mode during development.
- Prefer Python standard-library functionality when sufficient.
- Introduce dependencies only when justified.
- Use type hints where they improve clarity and maintainability.
- Write readable code with descriptive names and focused functions.

## Testing and Code Quality

Before committing changes, run the relevant checks:

- `python -m pytest`
- `python -m ruff check .`
- `python -m ruff format --check .`

Add or update tests when changing application behavior.

Do not modify tests merely to hide implementation failures.

GitHub Actions contains independent Test and Lint checks. Both must pass before merging into `main`.

## Git Workflow

The `main` branch is protected.

For new work:

1. Update the local `main` branch when beginning a new branch.
2. Create a descriptive feature, fix, documentation, or chore branch.
3. Make small, logically related changes.
4. Commit using clear messages, preferably Conventional Commits.
5. **Push immediately after every commit.**
6. Open a pull request using the repository's PR template.
7. Verify required CI checks.
8. Squash merge after validation.

Do not commit directly to protected `main` or bypass repository protections.

The agent must explicitly tell the developer when to commit and push.

Do not recommend committing every tiny edit. Use logical atomic commits.

Do not commit, push, merge, or deploy on the developer's behalf without explicit authorization.

## Databricks Development

- Prefer developing and maintaining source files locally in Neovim.
- Use the Databricks CLI and declarative configuration where practical.
- Prefer repeatable deployments over manual workspace configuration.
- Use Lakeflow Jobs for orchestration.
- Use declarative pipelines where their functionality is appropriate.
- Use Unity Catalog for supported data governance and storage workflows.
- Avoid hardcoding workspace paths, catalog names, or environment-specific identifiers.
- Distinguish local Python execution from Databricks runtime execution.
- Validate compatibility with the Python versions available in the relevant Databricks environments.
- Do not assume a Databricks feature is supported in Free Edition without verification.

### Existing Databricks Resources

The project has established:

- Catalog: `study_agent`
- Schemas: `bronze`, `silver`, `gold`
- Managed Volume: `study_agent.bronze.source_documents`
- SQL Warehouse-based catalog bootstrap
- Databricks Declarative Automation Bundle configuration
- A deployed Bronze ingestion pipeline using Auto Loader

Catalog creation is handled separately from bundle deployment because of an encountered metastore storage configuration limitation.

Do not recreate these resources without reviewing the existing implementation.

## Security and Data Handling

- Never hardcode secrets.
- Do not commit local authentication profiles or credentials.
- Follow least-privilege principles.
- Use authorized certification study materials.
- Preserve source metadata to support citations and traceability.
- Do not present generated answers as verified facts without appropriate grounding.

## Existing Implementation

The following functionality has already been implemented and validated.

### Repository and Infrastructure

- Python project configuration using `pyproject.toml`.
- `src/` package layout.
- Local Python development environment.
- pytest and Ruff configuration.
- GitHub Actions Test and Lint checks.
- CI status badges.
- Pull request template.
- Protected `main` branch.
- Databricks authentication and SDK bootstrap.
- Unity Catalog resource configuration.
- Databricks bundle validation and deployment.
- Bronze Auto Loader ingestion pipeline.

### Document Models

Existing Python models include:

- `DocumentMetadata`
- `DocumentStatus`
- `DocumentFileType`

The current `DocumentMetadata` model contains:

- `document_id`
- `file_name`
- `file_path`
- `file_type`
- `file_size_bytes`
- `content_hash`
- `ingested_at`
- `status`

Do not recreate these models.

Their fields may be revised after reconciling the newer metadata architecture.

### Metadata Utilities

The following utilities are implemented and tested:

- `determine_file_type()`
- `calculate_content_hash()`
- `generate_document_id()`
- `extract_file_name()`
- `generate_ingestion_timestamp()`

Implementation details:

- File type detection supports PDF and Markdown.
- File path parsing uses `PurePosixPath`.
- Content hashing uses SHA-256.
- Document ID generation uses UUID4.
- Timestamp generation uses timezone-aware UTC datetimes.

Do not reimplement these utilities.

## Milestone Tracking

This section is the primary continuation checkpoint.

Update it whenever a meaningful step or milestone is completed.

### Milestone 1 — Repository and Databricks Setup

**Status: COMPLETE**

- [x] Repository initialization and Python packaging
- [x] Local development environment
- [x] Testing and linting
- [x] GitHub Actions CI
- [x] PR template and branch protection
- [x] Databricks authentication and SDK setup
- [x] Unity Catalog bootstrap
- [x] Declarative Automation Bundle configuration
- [x] Initial Databricks resource deployment

Do not restart Milestone 1.

### Milestone 2 — Document Ingestion

**Status: IN PROGRESS**

- [x] 2.1 — Document models and enums
- [x] 2.2 — Ingestion architecture
- [x] 2.3 — Bronze Auto Loader pipeline
- [x] 2.4.1–2.4.3 — Initial metadata utility design and setup
- [x] 2.4.4 — SHA-256 content hashing
- [x] 2.4.5 — UUID4 document ID generation
- [x] 2.4.6 — Filename extraction
- [x] 2.4.7 — UTC ingestion timestamp generation
- [x] 2.4.8 — Status handling architecture decision; custom FSM deferred
- [ ] **2.4.9 — Metadata integration (CURRENT)**
- [ ] 2.5 — PDF and Markdown text extraction
- [ ] 2.6 — Text normalization and chunking
- [ ] 2.7 — Silver processing tables
- [ ] 2.8 — Incremental processing and version handling
- [ ] 2.9 — End-to-end ingestion validation

### Milestone 3 — Embeddings and Retrieval

**Status: NOT STARTED**

Planned work includes:

- Embedding strategy and model selection
- Embedding generation
- Vector Search configuration
- Retrieval testing and evaluation

### Milestone 4 — RAG Question Answering

**Status: NOT STARTED**

Planned work includes:

- Retrieval orchestration
- Prompt construction
- Grounded answer generation
- Source citations
- Error and insufficient-context handling

### Milestone 5 — Private Application

**Status: NOT STARTED**

Planned work includes:

- User-facing study interface
- Databricks Apps integration
- Document and question workflows
- Application deployment

### Milestone 6 — Evaluation and Deployment

**Status: NOT STARTED**

Planned work includes:

- Retrieval and answer evaluation
- MLflow integration
- Automated workflows
- Deployment documentation
- Final validation and reproducibility

## Current Development Checkpoint

**Current milestone:** 2 — Document Ingestion  
**Current step:** 2.4.9 — Metadata Integration  
**Current branch:** `feature/document-ingestion`

The latest completed implementation is Step 2.4.7, UTC ingestion timestamp generation.

The latest completed design decision is Step 2.4.8, which deferred custom document-status state machine implementation in favor of Databricks-native orchestration and monitoring.

### Current Task

Reconcile the existing `DocumentMetadata` Python model with the agreed Bronze metadata architecture.

Specifically, review:

- Whether `ingested_at` should become `registered_at`.
- Whether `last_ingested_at` belongs in current document metadata.
- Whether `status` should remain in the model.
- How `documents_raw` and `document_metadata` will relate.
- How UUID4 values will be assigned and persisted reliably.
- How observed document versions will be represented.

These are pending implementation decisions. Do not treat them as completed code.

After reconciling the model, proceed incrementally with the metadata Delta table and registration logic.

### Latest Git Checkpoint

The UTC ingestion timestamp utility and its tests were committed and pushed successfully.

No additional implementation has been committed since that checkpoint, based on the latest conversation.

Before beginning new implementation, review the current branch and working tree.

## Continuation Rules

When continuing this project in another conversation:

1. Read `AGENTS.md` and relevant source files.
2. Identify the current milestone and substep.
3. Check whether the requested functionality already exists.
4. Do not restart completed milestones.
5. Do not repeat completed implementation tasks.
6. Do not assume a design discussion means the code has been implemented.
7. Preserve previously agreed architecture unless there is a justified reason to revisit it.
8. Explain proposed architectural changes before making them.
9. Follow the learning-first assessment process.
10. Review developer-written code before approving it.
11. Require tests and quality checks before commits.
12. Explicitly instruct when to commit and immediately push.
13. Update milestone tracking after meaningful progress.
14. Resume from the latest incomplete step rather than generating a new project plan.

## Agent Behavior

When assisting with this repository:

- Read this file and relevant project configuration before proposing changes.
- Respect the current development milestone.
- Avoid implementing future milestones prematurely.
- Explain the reasoning behind important decisions.
- Ask before introducing significant dependencies or architectural changes.
- Prefer small, reviewable changes over large rewrites.
- Preserve existing tests and working functionality.
- Do not commit, push, merge, or deploy without explicit authorization.
- When providing educational guidance, allow the developer to implement the solution independently unless code is requested.
