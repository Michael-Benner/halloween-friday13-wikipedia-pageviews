# Halloween, Friday the 13th, and Wikipedia Page Views

**Michael Benner**

## Research question

Which categories of English Wikipedia articles experience the largest increases in readership around Halloween and Friday the 13th, and how do the patterns differ between these dates?

The project examines 12 articles across folklore and superstition, supernatural topics, horror, true crime, and historical disasters.

## Data

Daily English Wikipedia pageviews are collected from the [Wikimedia Pageviews REST API](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/page-views.html) for January 1, 2016 through December 31, 2025. Article titles and categories are listed in `collect_and_clean.py`. The collector writes the actual collection timestamp, record counts, and request failures to `data/collection_metadata.txt`.

The tidy dataset has one row per article-day: date, year, month, day, article, category, and views. Full raw and cleaned data files are generated locally and excluded from Git because they are reproducible and larger than the small portfolio sample. The first 50 cleaned rows are saved as `data/cleaned_sample.csv` after collection. No personal information is collected.

## Methods

The collector sends sequential requests with an identifying User-Agent, pauses between requests, and retries rate-limited responses using Retry-After when available. It saves raw API records, converts timestamps to ISO dates, removes duplicate article-day observations, and produces a tidy CSV plus a 50-row sample.

Halloween (October 31) is compared with the other dates in October of the same year for the same article. Each Friday the 13th is compared with other Fridays in that month and year. Percentage change is `(event-day views - baseline mean) / baseline mean * 100`. Results are summarized by event and category using mean and median percentage change. This is descriptive, not causal; missing observations are not treated as zero.

## Preliminary findings

Numerical findings are generated from live API responses by `analyze_pageviews.py`; they are not filled with invented values. Run the analysis to print category summaries, create `data/event_comparisons.csv` and `data/category_summary.csv`, and save `figures/event_pageview_changes.png`.

**Figure caption:** Mean percentage change in event-day pageviews relative to within-month comparison days, summarized by event and article category. Positive values indicate higher event-day readership than the baseline.

## Data dictionary

See [data/data_dictionary.md](data/data_dictionary.md).

## Reproduce

Requires Python 3.9+.

```bash
python -m pip install -r requirements.txt
python collect_and_clean.py
python analyze_pageviews.py
```

Run `wikipedia_pageviews.ipynb` from top to bottom for the same workflow.

## Limitations

Pageviews measure visits to selected article pages, not all public interest or search activity. The 12 articles are a purposive sample. News cycles, seasonality, long-term trends, and article changes may affect readership. Percentage changes can be sensitive to low baselines. The analysis does not establish that calendar dates cause changes.
