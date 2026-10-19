.PHONY: fetch fetch-fresh digest maturity reports check check-full all

all: fetch digest maturity facts reports

fetch:
	python3 scripts/fetch.py

fetch-fresh:
	rm -rf data/snapshots
	python3 scripts/fetch.py

digest:
	python3 scripts/digest.py

maturity:
	python3 scripts/maturity.py

facts:
	python3 scripts/facts.py

reports: facts
	python3 scripts/build_reports.py

check:
	python3 scripts/check.py --llms-only

check-full:
	python3 scripts/check.py
