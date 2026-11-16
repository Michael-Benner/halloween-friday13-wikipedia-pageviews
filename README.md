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

## Findings

The completed collection returned **43,836 daily records** for all 12 articles across 2016–2025, with **zero failed article-year requests**. The analysis found that Halloween had the clearest broad seasonal pattern: mean pageviews were above the October baseline in horror (+52.5%), supernatural (+62.6%), and folklore/superstition (+393.2%). The folklore mean is heavily influenced by the *Halloween* article itself, whose pageviews rise sharply on October 31; its category median was +36.9%. True-crime articles showed a smaller mean increase (+9.9%), while historical-disaster articles were below baseline on average (-7.9%).

For Friday the 13th, the folklore/superstition category had a very large mean increase (+2,482.2%), but this is strongly skewed by the *Friday the 13th* article itself, which experiences exceptional readership on those dates. Its category median increase was +232.7%. Other categories had much smaller average changes: true crime +11.1%, horror +5.0%, historical disasters +2.7%, and supernatural -0.7%. These category means should therefore be interpreted alongside medians and individual article results, not as uniform effects across all articles.

The analysis is descriptive. It cannot establish that the dates cause readership changes, and the purposive 12-article sample is not representative of all Wikipedia content. See `data/category_summary.csv` and `data/event_comparisons.csv` for the complete results.

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
