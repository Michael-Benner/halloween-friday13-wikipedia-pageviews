import csv, json, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
import os

START_YEAR = 2016
END_YEAR = 2025
PAUSE_SECONDS = 1.2
USER_AGENT = 'HalloweenFriday13WikipediaStudy/1.0 (student research; https://github.com/Michael-Benner)'
ARTICLES = [
    ('Halloween', 'folklore and superstition'),
    ('Friday the 13th', 'folklore and superstition'),
    ('Superstition', 'folklore and superstition'),
    ('Ghost', 'supernatural'),
    ('Vampire', 'supernatural'),
    ('Werewolf', 'supernatural'),
    ('Horror film', 'horror'),
    ('Horror fiction', 'horror'),
    ('Serial killer', 'true crime'),
    ('Jack the Ripper', 'true crime'),
    ('Chernobyl disaster', 'historical disasters'),
    ('Titanic', 'historical disasters'),
]
API = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article'

def fetch_article_year(article, year):
    title = urllib.parse.quote(article.replace(' ', '_'), safe='')
    url = '{}/en.wikipedia.org/all-access/user/{}/daily/{}0101/{}1231'.format(API, title, year, year)
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'application/json'})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.loads(response.read().decode('utf-8')).get('items', [])
        except urllib.error.HTTPError as error:
            if error.code in (429, 503) and attempt < 4:
                try:
                    delay = float(error.headers.get('Retry-After', 2 ** (attempt + 1)))
                except ValueError:
                    delay = 2 ** (attempt + 1)
                time.sleep(min(delay, 120))
            else:
                raise

def main():
    if 'replace-with-your-email' in USER_AGENT:
        print('Reminder: replace the contact placeholder in USER_AGENT before running.')
    os.makedirs('data', exist_ok=True)
    raw = []
    failures = []
    collected_at = datetime.now(timezone.utc).isoformat()
    for article, category in ARTICLES:
        for year in range(START_YEAR, END_YEAR + 1):
            try:
                items = fetch_article_year(article, year)
                for item in items:
                    raw.append({'article': article, 'category': category, 'timestamp': item['timestamp'], 'views': int(item.get('views', 0))})
                print('Collected {} {}'.format(article, year))
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as error:
                failures.append('{} {}: {}'.format(article, year, error))
                print('FAILED {} {}: {}'.format(article, year, error))
            time.sleep(PAUSE_SECONDS)
    raw.sort(key=lambda row: (row['article'], row['timestamp']))
    with open('data/raw_pageviews.csv', 'w', newline='', encoding='utf-8') as output:
        writer = csv.DictWriter(output, fieldnames=['article', 'category', 'timestamp', 'views'])
        writer.writeheader(); writer.writerows(raw)
    cleaned = []; seen = set()
    for row in raw:
        stamp = row['timestamp']
        day = '{}-{}-{}'.format(stamp[:4], stamp[4:6], stamp[6:8])
        key = (row['article'], day)
        if key in seen: continue
        seen.add(key)
        cleaned.append({'date': day, 'year': int(day[:4]), 'month': int(day[5:7]), 'day': int(day[8:10]), 'article': row['article'], 'category': row['category'], 'views': row['views']})
    cleaned.sort(key=lambda row: (row['date'], row['article']))
    fields = ['date', 'year', 'month', 'day', 'article', 'category', 'views']
    for path, subset in [('data/cleaned_pageviews.csv', cleaned), ('data/cleaned_sample.csv', cleaned[:50])]:
        with open(path, 'w', newline='', encoding='utf-8') as output:
            writer = csv.DictWriter(output, fieldnames=fields); writer.writeheader(); writer.writerows(subset)
    with open('data/collection_metadata.txt', 'w', encoding='utf-8') as output:
        output.write('Collection timestamp UTC: {}\n'.format(collected_at))
        output.write('Articles requested: {}\n'.format(len(ARTICLES)))
        output.write('Article-year requests attempted: {}\n'.format(len(ARTICLES) * (END_YEAR - START_YEAR + 1)))
        output.write('Raw records: {}\nClean records: {}\nFailures: {}\n'.format(len(raw), len(cleaned), len(failures)))
        for failure in failures: output.write(failure + '\n')
    print('Complete: {} tidy rows; {} failed requests.'.format(len(cleaned), len(failures)))

if __name__ == '__main__':
    main()