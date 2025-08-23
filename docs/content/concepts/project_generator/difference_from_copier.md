# Palimpsest Positioning: How It Differs from Copier and Where It Fits

This document explains how this project relates to Copier, what value it adds, and how it is layered technically.

## TL;DR

- Palimpsest is a template-plus-orchestrator, not a templating engine.
- Copier is the engine that renders files and enables updates.
- This project adds:
    - A curated, multi-stack template with features/presets.
    - Orchestrated automation (bootstrapping, provisioning, integrations) that runs alongside templating.
    - A resource tracking model that treats scripts, tools, and external entities as first-class, idempotent resources.
    - An opinionated, forkable structure teams can adopt internally.

## How This Differs from Copier

- Scope:
    - Copier: a generic file rendering and update engine driven by answers, with hooks.
    - Palimpsest: a reusable template plus automation orchestration, designed to standardize repos across multiple
      stacks (Python/Rust/Node/etc.), CI providers, and hosts.

- Responsibilities:
    - Copier:
        - Renders files from Jinja templates based on answers.
        - Supports updates via “re-apply” semantics.
        - Offers pre- / post-hooks for optional side effects.
    - Palimpsest:
        - Defines a schema and presets for multi-ecosystem scaffolds (features, providers, CI, docs).
        - Provides structured automation (e.g., create/link VCS repo, initialize envs, set up docs/CI) beyond pure file
          generation.
        - Tracks side-effectful actions as resources with idempotency rules and drift checks where possible.
        - Supplies opinionated defaults and composition patterns that are easy to fork and evolve.

- Outcomes:
    - Copier alone: great for templating and updating files.
    - Palimpsest: consistent, end-to-end project bootstrap and lifecycle management (files and integrations), with a
      declarative config as a single source of truth.

## Where This Fits on Top of Copier (Technical Layering)

Think of Palimpsest as the control plane and Copier as the execution engine for file changes.

- Input:
    - Answers YAML (the declarative config) drives both file generation and automation.
    - Presets further speed up common stacks and organizational standards.

- Planning:
    - Split the plan into two parts derived from the same Answers:
        - File Plan (Copier plan): which files/partials will be created/updated/deleted.
        - Automation Plan: which side-effectful operations will be executed (e.g., gh/glab/tea calls, environment setup,
          documentation bootstrap).
    - Both plans are previewable (pretend/plan) before application.

- Execution:
    - File Plan is executed by Copier (copy/update).
    - Automation Plan is executed by orchestrated scripts/hooks with guards and idempotency checks.
    - Ordering rules ensure correctness (e.g., create remote repo before pushing CI files if needed).

- State and Tracking:
    - Answers file: the declared desired state.
    - Optional resource registry: records which automation resources have been created/configured (e.g., “vcs:github:
      org/repo created at time T”).
    - Idempotency: each automation step checks the existing state before acting; failed steps will surface actionable
      remediation.

- Extensibility:
    - Providers: adapters for GitHub/GitLab/Gitea CLIs and language bootstraps (python/rust/node).
    - Features: composable modules that own files and automation fragments (e.g., docs, CI, codeowners, release
      automation).
    - Validation: schema and compatibility checks before planning.

## Repository Layout Convention (Forkable by Teams)

- Template root compatible with Copier:
    - copier.yml (questions, defaults, and hook wiring)
    - templated files and feature partials
    - presets/ (curated answers for common stacks)
- Automation layer colocated with the template:
    - automation/ (scripts, provider adapters, resource definitions)
    - docs/ (this documentation)
- Optional wrapper CLI (thin):
    - Pal (the Palimpsest CLI) enhances UX (init/list-presets/plan/apply/validate).
    - It writes answers, invokes the templating engine, and runs automation plans.

This structure is intentionally easy to fork:

- A company can fork the repo, set organization-specific defaults, keep internal presets, and add proprietary automation
  under automation/.
- Teams point the CLI (or Copier directly) at their fork to adopt company standards.

## Company/Team Adoption Scenarios

- Central template fork with org defaults:
    - Presets encode “official” stacks (python-lib, service, frontend, infra-module).
    - Features and providers reflect approved tools and CI.
- Controlled evolution:
    - Changes to the forked template are versioned; teams pull updates via Copier’s update flow.
- Guardrails:
    - Validation enforces org rules (e.g., required CI checks, license policy).
    - Automation ensures repos are created with correct permissions and protections.

## Automation Model (Beyond Copier Hooks)

- Why not only hooks?
    - Copier hooks are powerful but unstructured; complex orchestration benefits from a first-class plan with resource
      tracking.
- Resource-oriented approach:
    - Each external action (e.g., “create GitHub repo”) is a resource with:
        - Desired state (from answers)
        - Check functionality (is it already created/configured?)
        - Apply function (create/update)
        - Log/record in a registry (to support drift detection and retries)
- Idempotency and safety:
    - All steps must be re-runnable; failures should be resumable after fixing credentials or policy issues.

## What Remains in Copier vs. What Moves Up

- Stays in Copier:
    - Rendering and updating files.
    - Lightweight hooks for small, quick actions gated by answers.
- Moves up into this project’s orchestration:
    - Multistep provisioning, conditional dependencies between actions, retries, richer logging, and a unified
      plan/preview for both files and side effects.

## When to Use Only Copier

- If you only need file templating and occasional updates, Copier alone is enough.
- Move to this project’s orchestration when you want:
    - Consistent bootstrapping across stacks.
    - Provider integrations (VCS/CI) with guardrails.
    - Feature-driven composition and org presets.
    - A unified plan and resource tracking for reproducible repo setup.

## Summary

- Copier is the engine. This project is the standardized, forkable template plus an orchestration layer that:
    - Converts a single Answers YAML into both a file plan (Copier) and an automation plan.
    - Executes them safely with previews, validation, and idempotency.
    - Helps individuals and teams converge on evolving best practices across many stacks.
