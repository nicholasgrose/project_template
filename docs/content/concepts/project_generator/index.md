# Project Generator: Vision and Design Overview

This document explains the motivation, goals, and high-level design for a cross-stack project generator that uses a
declarative configuration and a reusable template.
It is a single source of truth for scaffolding new projects and updating existing projects to converge on shared,
evolving standards.

## Background

I maintain many kinds of projects (CLI tools, web apps, small work scripts, game engine experiments, homelab automation,
system setup scripts) across multiple ecosystems.
Over time, I’ve developed conventions that I want to:

- Apply on day 0 when creating a new repository.
- Re-apply and upgrade later as best practices evolve.
- Share and reuse across stacks (Python, Rust, Node, etc.).
- Integrate with hosting providers (GitHub/GitLab/Gitea) and CI systems.

Traditional one-shot generators don’t address the “upgrade and converge” need.
Developer tooling like dev containers helps with environment consistency,
but not with cross-repo scaffolding or lifecycle updates of templates.
A declarative, template-driven approach with planned updates better fits these goals.

## Goals

- Single source of truth for project configuration via a versioned YAML declaration (answers).
- Consistent scaffolding across multiple language ecosystems and CI providers.
- Safe, repeatable updates to existing repos as standards evolve.
- Modularity via feature flags (e.g., docs, CI, code quality, release automation).
- Optional provider orchestration (e.g., create/link repos via gh/glab/tea CLIs).
- Good team and AI-coder ergonomics: well-documented intent, non-ambiguous decisions.

## Non-Goals

- Not a package manager or build system.
- Not a secrets manager (tokens are referenced via environment, not stored).
- Not a replacement for per-language tools (cargo, npm, etc.); it orchestrates them.

## Core Approach (TL;DR)

- Use a declarative answers file as the source of truth (YAML).
- Use a template engine that supports both initial generation and updates.
- Model stack choices and optional features in the answer file; gate files and content with conditions.
- Provide presets for common stacks for fast starts.
- Support “pretend/plan” to preview changes and “update/apply” to perform them.
- Keep hooks idempotent; side effects are optional and guarded.

## Personas and Primary Use Cases

- Solo developer with diverse stacks: quickly create projects, apply standards, and evolve them over time.
- Team lead: standardize repository scaffolds across multiple teams, enforce CI/lint/docs conventions.
- Automation: CI jobs can validate or plan updates across many repos.

## UX Principles

- Declarative first, CLI-assisted: edit YAML or use CLI helpers that write YAML.
- Idempotent operations: re-running updates should be safe and predictable.
- Composable features: enable/disable with clear dependencies/conflicts.
- Transparent changes: preview diffs and steps before applying.

## Success Metrics

- Time-to-create: new repo from preset in under 30 seconds.
- Consistency: 90%+ of new repos use the same core features without manual tweaks.
- Upgradability: existing repos can apply updates without churn or data loss.
- Adoption: number of presets/features used across different stacks.

## Risks and Mitigations

- Drift between repo and template: use update flows and optional lock files; prefer generated separate files over shared
  hand-edited monoliths.
- Merge conflicts on update: isolate generated sections, use comment sentinels, and prefer per-feature files.
- Provider flakiness (gh/glab/tea): keep side effects optional and retryable; fail gracefully and explain next steps.

## Roadmap (high level)

1) Declarative core (answers + template + presets + pretend/update).
2) Providers (VCS/CI) with guarded hooks.
3) Upgrades and migrations (versioned features, guidelines for breaking changes).
4) Expanded features and curated presets across stacks.
