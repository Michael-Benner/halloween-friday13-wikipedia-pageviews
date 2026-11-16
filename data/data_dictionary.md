# Data Dictionary

The cleaned dataset contains one row per Wikipedia article per calendar day.

| Field | Meaning |
|---|---|
| `date` | Calendar date in YYYY-MM-DD format. |
| `year` | Four-digit year. |
| `month` | Month number (1–12). |
| `day` | Day of the month. |
| `article` | English Wikipedia article title. |
| `category` | Topic category assigned in the collection script. |
| `views` | Daily all-access user pageviews returned by Wikimedia. |

## Derived files

`event_comparisons.csv` contains article, category, event, event date, event-day views, baseline mean, and percentage change.

`category_summary.csv` contains the number of article-event observations and mean/median percentage change for each event/category combination.
