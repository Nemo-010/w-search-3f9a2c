.PHONY: fetch fetch-fresh digest maturity llms facts reports check check-full test all

all: fetch digest maturity llms facts reports test

fetch:
	python3 scripts/fetch.py

fetch-fresh:
	rm -rf data/snapshots
	python3 scripts/fetch.py

digest:
	python3 scripts/digest.py

maturity:
	python3 scripts/maturity.py

llms:
	python3 scripts/llms.py

facts:
	python3 scripts/facts.py

reports: facts
	python3 scripts/build_reports.py

test:
	python3 scripts/test_integrity.py

check:
	python3 scripts/check.py --llms-only

check-full:
	python3 scripts/check.py
