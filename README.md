# rqa-report-worker

Builds the weekly usage report and uploads it.

The worker fetches a JSON list of events, counts them per day and uploads the result.

## Configuration

Copy `.env.template` to `.env` and set:

- `REPORT_SOURCE_URL`: where to read the events
- `REPORT_SINK_URL`: where to upload the report

## Run

    pip install -r requirements.txt
    python -m worker.report

## Test

    python -m unittest discover -s tests

## Docker

    docker build -t rqa-report-worker .
    docker run --rm --env-file .env rqa-report-worker
