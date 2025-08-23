# ADR 0001: Adopt Declarative Config and Copier

- Status: Accepted
- Date: 2025-08-19
- Decision Drivers: upgradeability, multi-stack reuse, DX consistency, automation

## Context

We need a way to:

- Scaffold new repositories across multiple ecosystems with shared defaults.
- Re-apply evolving standards to existing repositories.
    - Optionally, orchestrate provider actions (Git hosting, CI) and language bootstraps.
      Traditional one-shot generators don’t provide safe updates.
      We need a declarative approach with repeatable updates and
      clear conditions for features.

## Decision

Adopt a declarative YAML answers file as the source of truth and use Copier as the template engine for both initial
generation (copy) and updates (update).
Model optional capabilities as features and use conditions in templates to include or exclude files and content.
Provide curated presets for common stacks.

## Consequences

- Positive:
    - Versionable, reviewable configuration.
    - Repeatable updates with conflict handling.
    - Composable features and provider-guarded hooks.
    - Faster onboarding through presets.
- Negative:
    - Some complexity in managing conditions and feature interactions.
    - Potential update conflicts if users modify generated sections without markers.

## Alternatives Considered

- Cookiecutter: popular and simple, but weaker update story.
- Custom engine: full control but would duplicate existing, mature functionality.

## Implementation Notes

- Keep answers in `.copier-answers.yml` at project root.
- Provide presets in `presets/*.yml`.
- Use small, idempotent hooks for side effects (e.g., VCS creation).
- Prefer discrete files per feature to reduce merge conflicts.
- Document feature compatibility and validation rules.
