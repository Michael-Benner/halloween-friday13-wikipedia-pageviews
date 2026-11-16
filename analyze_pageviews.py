import csv, os, statistics
from collections import defaultdict
from datetime import date
import matplotlib.pyplot as plt

os.makedirs('data', exist_ok=True)
os.makedirs('figures', exist_ok=True)

def load_data():
    rows = []
    with open('data/cleaned_pageviews.csv', newline='', encoding='utf-8') as source:
        for row in csv.DictReader(source):
            row['date'] = date.fromisoformat(row['date'])
            row['views'] = int(row['views'])
            rows.append(row)
    return rows

def main():
    rows = load_data()
    by_article = defaultdict(list)
    by_article_date = {}
    for row in rows:
        by_article[row['article']].append(row)
        by_article_date[(row['article'], row['date'])] = row
    comparisons = []
    for article, article_rows in by_article.items():
        for year in range(2016, 2026):
            halloween_day = date(year, 10, 31)
            halloween = by_article_date.get((article, halloween_day))
            october_days = [r['views'] for r in article_rows if r['date'].year == year and r['date'].month == 10 and r['date'].day != 31]
            if halloween and october_days:
                baseline = statistics.mean(october_days)
                if baseline > 0:
                    comparisons.append({'article': article, 'category': halloween['category'], 'event': 'Halloween', 'event_date': halloween_day.isoformat(), 'event_views': halloween['views'], 'baseline_views': baseline, 'change_percent': (halloween['views'] - baseline) / baseline * 100})
            for target in article_rows:
                day = target['date']
                if day.year != year or day.day != 13 or day.weekday() != 4:
                    continue
                fridays = [r['views'] for r in article_rows if r['date'].year == year and r['date'].month == day.month and r['date'].weekday() == 4 and r['date'].day != 13]
                if fridays:
                    baseline = statistics.mean(fridays)
                    if baseline > 0:
                        comparisons.append({'article': article, 'category': target['category'], 'event': 'Friday the 13th', 'event_date': day.isoformat(), 'event_views': target['views'], 'baseline_views': baseline, 'change_percent': (target['views'] - baseline) / baseline * 100})
    detail_fields = ['article', 'category', 'event', 'event_date', 'event_views', 'baseline_views', 'change_percent']
    with open('data/event_comparisons.csv', 'w', newline='', encoding='utf-8') as output:
        writer = csv.DictWriter(output, fieldnames=detail_fields); writer.writeheader(); writer.writerows(comparisons)
    grouped = defaultdict(list)
    for row in comparisons: grouped[(row['event'], row['category'])].append(row['change_percent'])
    summary = []
    for (event, category), values in sorted(grouped.items()):
        summary.append({'event': event, 'category': category, 'n_article_events': len(values), 'mean_change_percent': statistics.mean(values), 'median_change_percent': statistics.median(values)})
    with open('data/category_summary.csv', 'w', newline='', encoding='utf-8') as output:
        fields = ['event', 'category', 'n_article_events', 'mean_change_percent', 'median_change_percent']
        writer = csv.DictWriter(output, fieldnames=fields); writer.writeheader(); writer.writerows(summary)
    if summary:
        labels = ['{}\n{}'.format(r['event'], r['category']) for r in summary]
        values = [r['mean_change_percent'] for r in summary]
        fig, ax = plt.subplots(figsize=(13, 7))
        ax.bar(range(len(values)), values)
        ax.axhline(0, linewidth=1)
        ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, rotation=35, ha='right')
        ax.set_ylabel('Mean change from baseline (%)')
        ax.set_xlabel('Event and article category')
        ax.set_title('Wikipedia readership changes around Halloween and Friday the 13th')
        ax.grid(axis='y', alpha=0.25); fig.tight_layout()
        fig.savefig('figures/event_pageview_changes.png', dpi=200)
        plt.close(fig)
    print('Cleaned article-day records:', len(rows))
    print('Event comparison records:', len(comparisons))
    print('\nEvent | Category | N | Mean change | Median change')
    for row in summary:
        print('{} | {} | {} | {:.1f}% | {:.1f}%'.format(row['event'], row['category'], row['n_article_events'], row['mean_change_percent'], row['median_change_percent']))
    print('\nSaved data/event_comparisons.csv and data/category_summary.csv')
    if summary: print('Saved figures/event_pageview_changes.png')
    else: print('No comparisons found; check collection completeness.')

if __name__ == '__main__':
    main()