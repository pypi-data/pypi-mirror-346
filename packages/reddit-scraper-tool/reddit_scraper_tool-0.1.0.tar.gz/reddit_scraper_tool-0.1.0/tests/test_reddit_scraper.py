import pytest
import asyncio
from reddit_scraper.reddit_scraper import RedditScraper

@pytest.mark.asyncio
async def test_search_reddit_users():
    scraper = RedditScraper()
    results = await scraper.search_reddit_users("OpenAI")
    assert isinstance(results, list)
    assert len(results) > 0
    assert 'username' in results[0]
    assert 'created_at' in results[0]
    assert 'profile_url' in results[0]

@pytest.mark.asyncio
async def test_scrape_user_data():
    scraper = RedditScraper()
    user_data = await scraper.scrape_user_data("pokimane")
    assert isinstance(user_data, list)
    assert len(user_data) > 0
    assert 'title' in user_data[0]
    assert 'created' in user_data[0]
    assert 'url' in user_data[0]

@pytest.mark.asyncio
async def test_get_url_valid():
    scraper = RedditScraper()
    url = "https://www.reddit.com/r/test/.json"
    response = await scraper._get_url(url, None, type="json")
    assert response is not None

@pytest.mark.asyncio
async def test_get_url_invalid():
    scraper = RedditScraper()
    url = "https://www.reddit.com/r/invalid_subreddit/.json"
    response = await scraper._get_url(url, None, type="json")
    assert response is None

def test_extract_comments():
    scraper = RedditScraper()
    comments = [
        {"kind": "t1", "data": {"author": "user1", "body": "Comment 1", "score": 10, "replies": {}}},
        {"kind": "t1", "data": {"author": "user2", "body": "Comment 2", "score": 5, "replies": {"data": {"children": []}}}},
    ]
    extracted = scraper._extract_comments(comments)
    assert len(extracted) == 2
    assert extracted[0]['author'] == "user1"
    assert extracted[1]['author'] == "user2"