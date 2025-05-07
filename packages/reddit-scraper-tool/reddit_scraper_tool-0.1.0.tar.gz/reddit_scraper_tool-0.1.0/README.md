# Reddit Scraper

A Python package for scraping user data from Reddit. This package provides functionality to search for Reddit users and scrape their submitted posts, comments, and other relevant data.

## Features

- Search for Reddit users based on a query.
- Scrape user data including submitted posts, comments, and media.
- Asynchronous implementation for efficient data fetching.

## Installation

You can install the package using pip:

```
pip install reddit-scraper
```

## Usage

Here is a simple example of how to use the `RedditScraper` class:

```python
from reddit_scraper.reddit_scraper import RedditScraper
import asyncio

async def main():
    scraper = RedditScraper()
    users = await scraper.search_reddit_users("OpenAI")
    print(users)

    user_data = await scraper.scrape_user_data("pokimane")
    print(user_data)

asyncio.run(main())
```

## Running Tests

To run the tests for this package, navigate to the project directory and run:

```
pytest
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.