# Slide 23 · AI sandboxes and secure enclaves

> **Revised deck.** The revised deck (2026-10-31) removes CAISP from the slide, but the speaker note still mentions it, and adds CARC-hosted models and co-scientists.

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-23)

## What needs checking

- **`c1`** (technical, medium): Petabytes of iRODS collections on CyVerse; public collections read anonymously, with no credentials
- **`c2`** (technical, medium): Kubernetes AI sandboxes: agents get only allowed tools; egress through a proxy, every call recorded
- **`c3`** (factual, low): Private inference: ACCESS-CI allocations, CPU and GPU VMs from IaC templates
- **`c4`** (placeholder, low): CAISP (coming soon): a blind-validation competition

Status and the plan for each claim are in [`claims.yaml`](claims.yaml).

## Evidence

_Nothing yet. Code goes in `src/`, data in `data/`, outputs in `figures/`; see the top-level README._
