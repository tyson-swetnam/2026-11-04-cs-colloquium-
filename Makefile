# Each slide with an analysis gets a target named slide-NN that runs its src/ scripts in order.
PY ?= uv run python

.PHONY: setup slides claims check test slide-05 slide-06 slide-16 slide-17 slide-13 slide-14 slide-20 slide-25 slide-30 slide-38 slide-34 slide-35 slide-37

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

slide-37:
	@for s in slides/37-vote-for-the-future/src/[0-9]*.py; do echo "== $$s"; $(PY) $$s || exit 1; done

slide-34:
	@for s in slides/34-carc-docs-for-ai-agents/src/[0-9]*.py; do echo "== $$s"; $(PY) $$s || exit 1; done

slide-35:
	@for s in slides/35-ai-on-the-help-desk/src/[0-9]*.py; do echo "== $$s"; $(PY) $$s || exit 1; done

slide-20:
	@for s in slides/20-nairr/src/03_early_adopter_logos.py slides/20-nairr/src/04_resource_logos.py; do echo "== $$s"; $(PY) $$s || exit 1; done

slide-25:
	@for s in slides/25-demo-1-video/src/02_place_slide.py slides/25-demo-1-video/src/03_check_formation_docs.py; do echo "== $$s"; $(PY) $$s || exit 1; done

slide-30:
	@for s in slides/30-demo-3-question-to-result/src/03_place_video.py; do echo "== $$s"; $(PY) $$s || exit 1; done

slide-38:
	@for s in slides/38-questions/src/04_place_qr.py; do echo "== $$s"; $(PY) $$s || exit 1; done

slide-16:
	@for s in slides/16-system-one-models/src/04_cover_and_columns.py; do echo "== $$s"; $(PY) $$s || exit 1; done
