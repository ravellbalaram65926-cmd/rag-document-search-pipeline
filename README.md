# RAG Document Search Pipeline

## Problem
Let users ask questions over a document collection and retrieve grounded answers with citations.

## Dataset and provenance

`data/raw/docs/` has two short, original demo documents. Add public documents you are permitted to process to this directory; for example, use documents from [arXiv](https://arxiv.org/) and preserve source/license metadata. No third-party corpus or API key is required for the local demo.

### Download the Kaggle arXiv corpus

The optional downloader defaults to `Cornell-University/arxiv`, a very large corpus (over 1.7 million paper records). Check current Kaggle terms, disk space, and license before downloading. Install the Kaggle CLI with `python -m pip install kaggle`, create an API token in Kaggle account settings, and save `kaggle.json` to `%USERPROFILE%\.kaggle\kaggle.json` on Windows or `~/.kaggle/kaggle.json` on macOS/Linux. Run `python scripts/download_kaggle.py`; data goes to ignored `data/external/`. Convert permitted text fields into `.txt` documents under `data/raw/docs/` before running the demo indexer; it does not ingest Kaggle JSON directly. Keep source and license metadata.

## Run the ETL demo

From this directory, run `python src/main.py`. It hashes each text file, skips duplicate content, stores source names and content hashes, and emits overlapping chunks to `data/gold/chunks.jsonl`. Chunk size and overlap are configurable with `--chunk-words` and `--overlap`. This prepares retrieval data only; it does not call an LLM or create embeddings. Re-run safely after adding documents. Run checks with `python -m pytest -q tests`.

## Stack
Python, embeddings, vector store, LLM API, FastAPI

## Architecture
- Bronze / raw ingestion layer
- Silver / cleaned and validated data layer
- Gold / feature or serving layer
- Monitoring / validation and retraining feedback loop

## DE tasks
1. Ingest raw data with versioned file naming and timestamps.
2. Build idempotent and incremental transformations.
3. Add data quality checks and freshness alerts.
4. Create a reproducible run order using a Makefile or run script.
5. Store outputs in a warehouse, lake, or streaming sink with clear contracts.

## DS tasks
1. Run EDA and validate assumptions about seasonality, drift, and user behavior.
2. Benchmark a baseline model before trying a stronger approach.
3. Use proper time-based splits and avoid leakage.
4. Log experiments, tuning choices and key metrics.
5. Report limitations and next steps in a production-focused way.

## Deliverables
- Reproducible pipeline or app
- Tests for transformation and validation logic
- Dashboard, API, or report showing outputs
- Clear business summary with measurable impact

## Recommended repository structure
`	ext
rag-document-search-pipeline/
+-- README.md
+-- requirements.txt
+-- Makefile
+-- .gitignore
+-- src/
+-- tests/
+-- notebooks/
+-- docs/
`

## Resume line
Built a RAG pipeline with incremental ingestion and improved retrieval quality through chunking and re-ranking experiments.

### Kaggle dataset download

Install Kaggle CLI with `python -m pip install kaggle`, create an API token in Kaggle account settings, and save it locally as `%USERPROFILE%\.kaggle\kaggle.json` on Windows or `~/.kaggle/kaggle.json` on macOS/Linux. Never commit or share the token. Run `python scripts/download_kaggle.py`; downloaded files go to Git-ignored `data/external/` and are not published to this repository. Review the dataset license and Kaggle terms before use; large datasets may require adapting the sample input schema.
