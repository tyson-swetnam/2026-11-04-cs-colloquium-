# Each slide with an analysis gets a target named slide-NN that runs its src/ scripts in order.
PY ?= uv run python

.PHONY: setup slides claims check test slide-04 slide-05

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

slide-04:
	@for s in slides/04-the-build-out/src/[0-9]*.py; do [ -e "$$s" ] || continue; echo "== $$s"; $(PY) $$s || exit 1; done

slide-05:
	@for s in slides/05-the-concerns/src/[0-9]*.py; do [ -e "$$s" ] || continue; echo "== $$s"; $(PY) $$s || exit 1; done
