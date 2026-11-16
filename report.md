# Final Report: Halloween, Friday the 13th, and Wikipedia Page Views

**Michael Benner**

## Introduction

This project asks which categories of English Wikipedia articles experience the largest increases in readership around Halloween and Friday the 13th, and how the patterns differ between these dates. The analysis uses 12 articles from five topic categories: folklore and superstition, supernatural, horror, true crime, and historical disasters. Daily pageviews from 2016 through 2025 provide a way to compare readership on the event dates with typical readership during the same month.

## Methods

Daily all-access user pageviews were collected from the Wikimedia Pageviews REST API for 12 English Wikipedia articles from January 1, 2016 through December 31, 2025. The collector made 120 article-year requests, used an identifying User-Agent, paused between requests, and retried rate-limited responses. It returned 43,836 records with no failed requests.

The cleaning step converted API timestamps to calendar dates, retained one observation per article per day, and created a tidy dataset with date, year, month, day, article, category, and views. A 50-row sample is committed to the repository; full raw and cleaned data are reproducible and excluded from version control.

For Halloween, each October 31 observation was compared with the same article's mean pageviews on the other days in October of that year. For Friday the 13th, each Friday the 13th was compared with the same article's mean pageviews on the other Fridays in that month and year. Percentage change was calculated as (event-day views minus baseline mean) divided by baseline mean, multiplied by 100. Category results report the mean and median of the article-event percentage changes.

## Findings

Halloween showed a consistent increase across several spooky-content categories. The mean change was +62.6% for supernatural articles and +52.5% for horror articles. Folklore and superstition had a much larger mean increase of +393.2%, although its median was +36.9%. This difference indicates that the mean is strongly influenced by the *Halloween* article itself, which receives a large readership spike on October 31. True crime increased by a more modest mean of +9.9%, while historical-disaster articles were down by an average of 7.9%.

Friday the 13th produced the largest measured increase in folklore and superstition, with a mean of +2,482.2% and a median of +232.7%. This dramatic result is largely driven by the *Friday the 13th* article, whose readership rises sharply on the date named in the article title. The remaining categories showed comparatively modest mean changes: true crime +11.1%, horror +5.0%, historical disasters +2.7%, and supernatural -0.7%.

The comparison suggests that Halloween is associated with a broader increase across horror and supernatural topics, whereas Friday the 13th produces an especially concentrated spike in readership for the directly relevant *Friday the 13th* article. The very large folklore means should not be interpreted as typical increases for every article in that category; the median and article-level results are important context.

## Discussion and Limitations

The results are consistent with the idea that culturally significant dates influence what people read on Wikipedia. Halloween is associated with elevated readership across multiple spooky-topic categories. Friday the 13th is associated with a particularly strong increase for the article specifically about that date.

There are several limitations. First, the project examines a purposive sample of only 12 articles rather than all Wikipedia content. Second, pageviews measure visits to article pages, not searches, beliefs, or general public interest. Third, news events, seasonality, article edits, and other outside factors may affect daily readership. Fourth, percentage changes can become very large when the comparison baseline is small. Finally, this observational comparison cannot establish that the calendar date itself caused the increase.

Overall, the strongest conclusion is that Halloween corresponds to broader readership increases across horror and supernatural articles, while Friday the 13th produces a highly concentrated spike for its namesake article. Future work could expand the article sample, compare additional culturally significant dates, and use a more robust statistical model to account for seasonality and long-term pageview trends.
