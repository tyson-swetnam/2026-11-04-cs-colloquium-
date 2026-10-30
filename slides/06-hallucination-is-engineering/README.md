# Slide 06 · Hallucination is an engineering problem

Section: 01 · Fear · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-06)

## What needs checking

- **`c1`** (technical, medium): “It invents citations” → the agent must call a real index
- **`c2`** (technical, medium): “It makes up metadata” → terms must resolve in an ontology
- **`c3`** (technical, medium): “It varies run to run” → a JSON schema, validated in the agent
- **`c4`** (technical, medium): “I cannot audit it” → provenance in DuckLake; replay any run
- **`c5`** (attribution, high): Google DeepMind's GNoME proposed 380,000 crystals; independent labs confirmed under 5%
- **`c6`** (qualitative, low): Every output is a hypothesis until it is checked

Status and the plan for each claim are in [`claims.yaml`](claims.yaml).

## Evidence

_Nothing yet. Code goes in `src/`, data in `data/`, outputs in `figures/`; see the top-level README._
