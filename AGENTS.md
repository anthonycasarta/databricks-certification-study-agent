# Agent Instructions

## Project Overview

**Project:** Databricks Certification Study Agent

Build a Databricks-native, retrieval-augmented generation (RAG) study assistant focused initially on the Databricks Certified Data Engineer Associate certification.

The project is both a functional application and a hands-on learning experience for Databricks data engineering, software engineering, and AI/ML concepts.

The application should help users study certification material by retrieving relevant information from an indexed knowledge base and generating grounded answers.

## Development Philosophy

- Prioritize understanding over implementation speed.
- Keep the architecture simple, modular, and maintainable.
- Prefer native Databricks capabilities over unnecessary third-party frameworks.
- Avoid adding abstractions, services, or dependencies without a clear reason.
- Implement functionality incrementally, with tests where appropriate.
- Explain significant architectural decisions and tradeoffs.
- Do not generate large amounts of implementation code without explicit authorization.
- When guiding implementation, provide explanations, relevant documentation, and small learning objectives rather than complete solutions by default.

## Technology Stack

- **Language:** Python 3.12
- **Development environment:** macOS, Neovim, WezTerm
- **Cloud platform:** Databricks Free Edition
- **Data storage:** Unity Catalog and Delta tables
- **Orchestration:** Lakeflow Jobs
- **Declarative pipelines:** Introduce where useful and supported
- **Retrieval:** Databricks-managed vector search capabilities, subject to availability
- **LLM inference:** Databricks Foundation Model APIs, subject to availability
- **Application:** Streamlit deployed through Databricks Apps, subject to availability
- **Experiment tracking and evaluation:** MLflow
- **CI:** GitHub Actions
- **Deployment configuration:** Declarative Automation Bundles
- **Testing:** pytest
- **Linting and formatting:** Ruff
- **Packaging:** setuptools with a `src/` layout

Verify service availability and Free Edition limitations before implementing Databricks-dependent features.

## Architecture

The intended application follows a retrieval-augmented generation workflow:

1. Ingest certification study documents.
2. Extract and normalize document content.
3. Split documents into retrievable chunks.
4. Store processed content in Delta tables.
5. Generate embeddings and configure retrieval.
6. Retrieve relevant chunks for a user question.
7. Generate answers grounded in retrieved context.
8. Present answers and source references through the application.
9. Evaluate retrieval quality and answer quality.

Prefer clear boundaries between ingestion, retrieval, generation, evaluation, and application components.

The architecture may evolve as implementation and platform constraints become clearer.

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

GitHub Actions contains independent Test and Lint workflows. Both must pass before merging into `main`.

## Git Workflow

The `main` branch is protected.

For new work:

1. Update the local `main` branch.
2. Create a descriptive branch, such as `feature/document-ingestion`, `fix/...`, `docs/...`, or `chore/...`.
3. Make small, logically related changes.
4. Commit using clear, descriptive messages, preferably following Conventional Commits.
5. Push each commit to the remote feature branch.
6. Open a pull request using the repository's PR template.
7. Verify required CI checks.
8. Squash merge after validation.

Do not push directly to `main` or bypass repository protections.

## Databricks Development

- Prefer developing and maintaining source files locally in Neovim.
- Use the Databricks CLI and declarative configuration where practical.
- Prefer repeatable deployments over manual workspace configuration.
- Use Lakeflow Jobs for orchestration.
- Introduce declarative pipelines only when they provide meaningful benefits.
- Use Unity Catalog for supported data governance and storage workflows.
- Avoid hardcoding workspace paths, catalog names, or environment-specific identifiers.
- Distinguish local Python execution from Databricks runtime execution.
- Validate compatibility with the Python versions available in the relevant Databricks environments.
- Do not assume that a Databricks feature is supported in Free Edition without verification.

## Security and Data Handling

- Never hardcode secrets.
- Do not commit local authentication profiles or credentials.
- Follow least-privilege principles.
- Use authorized certification study materials.
- Preserve source metadata to support citations and traceability.
- Do not present generated answers as verified facts without appropriate grounding.

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
