# filepath: reddit-scraper/reddit_scraper/reddit_scraper.py
import asyncio
import aiohttp
import datetime
import re
import html

DOMAIN = "https://www.reddit.com"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"

class RedditScraper:
    def __init__(self):
        pass

    async def search_reddit_users(self, search_query: str) -> list:
        """Search Reddit site based on a query"""
        url = f"{DOMAIN}/search/.json?q={search_query}&type=user&limit=100"
        async with aiohttp.ClientSession() as session:
            response = await self._get_url(url, session, type="json")
            results = []
            if response:
                for user in response['data']['children']:
                    user_data = user['data']
                    results.append({
                        'username': user_data['name'],
                        'created_at': datetime.datetime.fromtimestamp(user_data['created_utc']).strftime('%Y-%m-%d %H:%M:%S') if 'created_utc' in user_data.keys() else None,
                        'profile_url': f"{DOMAIN}/user/{user_data['name']}",
                        'profile_image_url': user_data['icon_img'] if 'icon_img' in user_data else None,
                    })
                return results
            return []

    async def scrape_user_data(self, username):
        """Scrape user data based on a username"""
        results = []
        after = ''
        async with aiohttp.ClientSession() as session:
            while after is not None:
                url = f"{DOMAIN}/user/{username}/submitted.json?limit=100&after={after}" 
                response = await self._get_url(url, session, type="json")
                if response:
                    for post in response['data']['children']:
                        post_data: dict = post['data']
                        results.append({
                            'title': post_data['title'],
                            'created': datetime.datetime.fromtimestamp(post_data['created']).strftime('%Y-%m-%d %H:%M:%S'),
                            'url': f"{DOMAIN}{post_data['permalink']}" if 'permalink' in post_data else None,
                            'body': post_data['selftext'] if 'selftext' in post_data else None,
                            'upvotes': post_data['ups'] if 'ups' in post_data else 0,
                            'downvotes': post_data['downs'] if 'downs' in post_data else 0,
                            'total_comments': post_data['num_comments'] if 'num_comments' in post_data else 0,
                            'subreddit': post_data['subreddit'] if 'subreddit' in post_data else None, 
                            'thumbnail': post_data['thumbnail'] if post_data['thumbnail'] != 'default'  else None,
                            'gallery_images': post_data['media_metadata'] if 'is_gallery' in post_data.keys() else None,
                            'poll_data': post_data['poll_data'] if 'poll_data' in post_data else None,
                            'media': post_data['media']if 'media' in post_data else None,
                        })
                    after = response['data']['after']
                else:
                    break
        
        tasks = [ self._get_comments(post) for post in results if post['url'] is not None ]
        results = await asyncio.gather(*tasks)
        return results

    async def _get_url(self, url: str, session, type: str = None) -> str | None:
        """Get content from the URL"""
        try:
            headers = {'User-Agent': USER_AGENT}
            if type == "json":
                async with session.get(url, headers=headers) as response:
                    json_response = await response.json()
                    return json_response
            async with session.get(url, headers=headers) as response:
                text_response = await response.text()
                return text_response
        except Exception as e:
            print(f"Error fetching URL {url}: {e}")
            return None
    
    async def _get_comments(self, post: dict) -> dict:
        """Get comments from post data"""
        url = f"{post['url']}.json"
        async with aiohttp.ClientSession() as session:
            response = await self._get_url(url, session, type="json")
            if response:
                comments = self._extract_comments(response[1]['data']['children'])
                post['comments'] = comments
            return post

    def _extract_comments(self, comments):
        extracted_comments = []
        for comment in comments:
            if isinstance(comment, dict) and comment.get("kind") == "t1":
                comment_data = comment.get("data", {})
                extracted_comment = {
                    "author": comment_data.get("author", ""),
                    "body": comment_data.get("body", ""),
                    "score": comment_data.get("score",""),
                    "replies": [],
                }

                replies = comment_data.get("replies", "")
                if isinstance(replies, dict):
                    extracted_comment["replies"] = self._extract_comments(
                        replies.get("data", {}).get("children", [])
                    )
                extracted_comments.append(extracted_comment)
        return extracted_comments
    
    async def _get_gallery_images(self, gallery: dict) -> list:
        """Get gallery images from post data"""
        gallery_items = []
        for item in gallery.items():
            gallery_items.append(item['p'][0]['u'].replace('amp;', ''))
        return gallery_items

    def _extract_iframe_src(self, iframe_content: str) -> str | None:
        """Extract the src link from an iframe tag"""
        try:
            decoded_content = html.unescape(iframe_content)
            match = re.search(r'src="([^"]+)"', decoded_content)
            if match:
                return match.group(1)
            return None
        except Exception as e:
            print(f"Error extracting iframe src: {e}")
            return None