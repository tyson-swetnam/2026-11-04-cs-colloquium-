# Each slide with an analysis gets a target named slide-NN that runs its src/ scripts in order.
PY ?= uv run python

.PHONY: setup slides claims check test slide-05 slide-06 slide-17 slide-13 slide-14 slide-34

setup:
	uv sync --extra dev

slides:            ## regenerate talk/slides.md after re-exporting the deck
	$(PY) tools/deck.py extract

claims:            ## regenerate CLAIMS.md from slides/*/claims.yaml
	$(PY) tools/claims.py index

check: test        ## what CI runs
	$(PY) tools/claims.py check

test:
	uv run pytest -q

slide-05:
	@for s in slides/05-the-build-out/src/[0-9]*.py; do [ -e "$$s" ] || continue; echo "== $$s"; $(PY) $$s || exit 1; done

slide-06:
	@for s in slides/06-the-concerns/src/[0-9]*.py; do [ -e "$$s" ] || continue; echo "== $$s"; $(PY) $$s || exit 1; done

slide-17:
	@for s in slides/17-hallucination-is-engineering/src/[0-9]*.py; do [ -e "$$s" ] || continue; echo "== $$s"; $(PY) $$s || exit 1; done

slide-13:
	@for s in slides/13-ai-molecular-science/src/[0-9]*.py; do echo "== $$s"; $(PY) $$s || exit 1; done

slide-14:
	@for s in slides/14-agentic-ai/src/[0-9]*.py; do echo "== $$s"; $(PY) $$s || exit 1; done

slide-34:
	@for s in slides/34-vote-for-the-future/src/[0-9]*.py; do echo "== $$s"; $(PY) $$s || exit 1; done
