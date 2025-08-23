# ADR 0002: Module Composition via Hidden Directories

- Status: Proposed
- Date: 2025-08-20
- Decision Drivers: composability, forkability, internal extensibility, single-source-of-truth validation

## Context

We want a composable system where:

- The root directory defines a control plane (single venv, validation, planning, and apply).
- Child directories can contribute their own template files, schema fragments, automation hooks, and dependencies.
- One answers YAML remains the single source of truth, validated against a generated schema composed of all
  participating modules.
- Automation is Python-based, idempotent, and runs from a single, top-level virtual environment.

The goal is to support internal/company overlays and domain-specific modules without central rewrites and to make it
easy to fork, extend, or constrain practices.

## Decision

Adopt a module composition model using hidden directories to declare module metadata, schema fragments, templates, and
automation:

- Root control plane:
    - A hidden root folder (e.g., .pal/) hosts a single venv, requirements, schema composition output, presets,
      and optional state/registry.
    - Root orchestrates discovery, dependency resolution, schema composition, planning, validation, and execution.

- Module definition (per child directory):
    - A hidden module folder (e.g., <module>/.pal/) containing:
        - module.yaml — manifest: name, version, owned answer paths, requires/conflicts, Python deps, and hook entry
          points.
        - schema/*.json — JSON Schema fragments validating the module’s owned answers keys.
        - templates/ — Copier-compatible template files for this module.
        - automation/ — Python hooks implementing idempotent side effects.

- Schema composition:
    - The root composes a generated JSON Schema from all module fragments and validates the single answers file against
      it.

- Planning and execution:
    - Build a unified plan with two parts from the same answers:
        - File plan: merge module templates deterministically and run Copier (prefer a single pass).
        - Automation plan: order module hooks by dependency graph and phase (pre_plan, post_render, post_apply).
    - Execute plans with idempotency, clear logs, and an optional resource registry.

- Single venv:
    - Aggregate module Python dependencies at plan time and install them into the root .pal/.venv.

## Scope

In scope:

- Root-level control plane and per-module manifests.
- Module discovery, DAG resolution, schema composition, and validation.
- Unified planning and phase-ordered execution.
- Optional lock/state files for module versions and resource tracking.

Out of scope (for this ADR):

- Exact CLI UX.
- Deep provider abstractions beyond a minimal hooks interface.
- Complex migration framework (can be added later).

## Architecture Overview

- Root
    - .pal/
        - .venv/
        - requirements.txt
        - schema/generated.schema.json
        - presets/*.yml
        - state/lock.yml
        - state/registry.yml (optional)
        - logs/ (optional)

- Modules (examples)
    - ci.github/
        - templates/...
        - .pal/
            - module.yaml
            - schema/ci.github.json
            - automation/hooks.py
    - docs.mkdocs/
        - templates/...
        - .pal/
            - module.yaml
            - schema/docs.mkdocs.json
            - automation/hooks.py

## Module Contract

- Manifest (module.yaml)
    - name: unique module name (e.g., ci.github)
    - version: semver
    - owns: list of answer subtrees (e.g., ["ci.github"])
    - requires: a list of module names
    - conflicts: list of module names
    - python:
        - requires: Python version constraint
        - pip: list of pip requirements
    - templates.root: path to module’s Copier template files
    - automation:
        - entry_point: Python module path (e.g., automation.hooks)
        - hooks: list of named callables with phases (e.g., pre_plan, post_render, post_apply)

- Schema fragments
    - Validate only the keys under the subtrees declared in `owns`.
    - Must provide $id and use draft 2020-12 or later.

- Automation hooks
    - Must be idempotent (check/apply).
    - Must accept a shared context (answers, paths, env) and return structured results or raise structured errors.

## Schema Composition

- Discovery loads all module schema fragments.
- The root generates a single top-level schema (schema/generated.schema.json) using $defs and $ref to compose fragments 
  or by merging fragments under their owned paths.
- Validation:
    - Run before planning; fail fast with actionable errors (missing required keys, conflicts, unmet dependencies).

## Planning and Execution

- Build a dependency DAG of modules (requires/conflicts).
- Phased execution:
    1) pre_plan hooks (sanity checks, credentials, discovery of ambient state).
    2) Render files:
        - Prefer a single Copier pass over a deterministic staging area that merges module templates.
    3) post_render hooks (provision resources, configure CI, set branch protection).
    4) post_apply hooks (verification, health checks).

- Lock/state:
    - lock.yml: records module names/versions, template commit(s), and hashes.
    - registry.yml (optional): records external resources (e.g., created repo, protections) for drift detection.

## Versioning and Upgrades

- Module versions:
    - Modules declare their own version; changes to owned schema or file layout increment minor/major accordingly.
- Answers schema:
    - Top-level schemaVersion governs breaking changes across the composed schema.
- Upgrades:
    - copier update re-renders files; automation re-runs idempotently.
    - Incompatible module changes should ship migration notes and optional migration hooks.

## Security

- No secrets in answers or manifests.
- Use environment variables or system credential stores.
- Hooks must guard against missing credentials and fail with precise remediation guidance.

## Alternatives Considered

- Monolithic template:
    - Simpler initial implementation but poor extensibility and internal adoption story.
- Only Copier hooks:
    - Works for simple side effects but lacks structured composition, validation, and resource tracking.

## Consequences

- Positive:
    - High composability and internal extensibility.
    - Clear ownership boundaries via owned answer paths.
    - Single answers file with unified validation and planning.
    - Easy to fork for organizations; modules can be added/removed with minimal coupling.

- Negative:
    - More moving parts (schema composition, module discovery, DAG resolution).
    - Requires conventions and documentation to keep module interactions healthy.

## Repository Strategy (Template Storage)

- Start co-located (template + modules + orchestration in one repo) for speed and coherence.
- Optionally, split template content into a separate repo when:
    - You need an independent release cadence or access control.
    - Multiple control planes reuse the same module/template set.
- If split:
    - Pin the template repo via URL/tag in the lockfile.
    - Use submodule/subtree or a fetch-on-plan mechanism to assemble modules/templates at run time.

## Rollout Plan

1) Implement discovery + DAG + schema composition + validation.
2) Deliver two modules (e.g., ci.github, docs.mkdocs) to prove composition.
3) Add a lockfile and minimal registry.
4) Document module authoring: manifest, schema, templates, automation.
5) Evaluate whether to split template storage into a separate repo after initial adoption.

## Decision

Proceed with the module composition approach using hidden directories at both root and module levels, with a single venv
at the root and a unified answers file.
Beginning co-located; revisit splitting template storage once modules stabilize and
reuse demands it.
