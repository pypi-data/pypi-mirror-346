# PyLatestTrends

PyLatestTrends is a Python library that allows you to fetch and analyze trending topics from Google Trends. Whether you're building a data analytics dashboard, content pipeline, or market intelligence tool, this package provides a simple interface to extract trending keywords by country, category, time period, and relevance.

## 🚀 Features

- 📈 Scrape trends going on in countries from Google Trends in real time.
- 🌍 Filter by country (using ISO codes) for localized trends.
- 🕒 Customize time ranges like last 4 hours, 24 hours, or 7 days.
- 🗂 Sort by volume, recency, or relevance.
- 🧠 Filter by specific categories (e.g., Technology, Business, Health).
- 🐍 Built for data science — returns results in a Pandas DataFrame.
- 🔍 Optional logging for debugging or verbose insights.

## 📦 Installation

```bash
pip install pylatesttrends
```

## 🧑‍💻 Quick Start

You can start by plucking in only this code and you will be able to get the trends.

```python
from pylatesttrends import generate_payload, get_trends

# Create payload for the US
payload = generate_payload("US")

# Fetch trending data
result = get_trends(payload)

# View DataFrame
print(result.head())
```

## ⚙️ Parameters & Customization

You can customize the `generate_payload()` function with the following options:

### `geo` (Required)

The ISO 3166-1 alpha-2 country code to fetch trends from.

```python
payload = generate_payload("US")
```

Full list of supported ISO codes (e.g., US, IN, GB, DE, JP) is provided below.

### `start_trending`

Filter trends based on time when they started trending.

```python
payload = generate_payload("US", start_trending="48h")
```

Valid time options:

```plaintext
4h, 24h, 48h, 7d
```

### `category`

Choose a trend category to narrow the results.

```python
payload = generate_payload("US", category="Technology")
```

Available categories:

```plaintext
Autos and Vehicles, Beauty and Fashion, Business and Finance, Climate, Entertainment, Food and Drink,
Games, Health, Hobbies and Leisure, Jobs and Education, Law and Government, Other, Pets and Animals,
Politics, Science, Shopping, Sports, Technology, Travel and Transportation
```

### `trend_status_active_trends`

Include or exclude active trending status.

```python
payload = generate_payload("US", trend_status_active_trends=True)
```

- `True`: show only currently active trends
- `False`: include historical or past-trending keywords

### `sort_by`

Sort the results using various attributes:

```python
payload = generate_payload("US", sort_by="recency")
```

Valid values:

```plaintext
title, search-volume, recency, relevance
```

### `base_url` (Advanced)

Set a custom base URL for data scraping (for proxies or mirrors).

```python
Set a custom base URL for data scraping (for proxies or mirrors).
```

## Logging Option

Enable logging for insight into data retrieval:

```python
result = get_trends(payload, "print")  # or use "logging"
```

## Output Format

The result returned from `get_trends()` is a pandas DataFrame containing:

- Trends: trend name
- Search volume: volume of the search
- Started: trend start time
- Ended: trend end time
- Trend breakdown: searches
- Explore link: trend explore link

## Use Cases

**Content Strategy:** Discover trending topics in your region for blogs, YouTube, or news content.
**Market Research:** Analyze shifts in consumer interest over time.
**Social Media:** Track viral search terms to time your posts effectively.
**SEO Planning:** Create keyword-rich content based on real-time demand.

## Requirements

- Python 3.9+
- Selenium
- Pandas

(Dependencies are installed automatically with pip.)

## Example: Get Trending Tech Topics in United States Over Last 24 Hours

```python
payload = generate_payload("US", category="Technology", start_trending="24h")
df = get_trends(payload, "logging")
print(df[['title', 'traffic', 'article_url']])
```

### Links

- [📦 PyPI Package](https://pypi.org/project/pylatesttrends/)
- [🧑‍💻 GitHub Repository](https://github.com/faraasat/pylatesttrends)
- [📚 Documentation](https://github.com/faraasat/pylatesttrends/blob/main/README.md)

## Contributing

Contributions are welcome! Open issues, fork the repo, and submit pull requests.

## License

This project is licensed under the GNU General Public License v3 (GPLv3) License.
