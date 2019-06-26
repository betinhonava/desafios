import re
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
import time

REDDIT_OLD_URL = 'https://old.reddit.com/r/'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
NUM_REGEX = re.compile('[^0-9eE.]')


class RedditScrapper:

    def __init__(self, subreddits='', min_votes=5000, num_pages=5):
        self.subreddits = subreddits.split(';')
        self.min_votes = min_votes
        self.num_pages = num_pages

    def run(self):
        df = pd.DataFrame(
            columns=['Pontuação', 'Subreddit', 'Título', 'Comentários',
                     'Link'])
        for subreddit in self.subreddits:
            url = urljoin(REDDIT_OLD_URL, subreddit)
            for i in range(self.num_pages):
                content = requests.get(url, headers=HEADERS).content
                soup = BeautifulSoup(content, features="html.parser")
                for thread in soup.find_all('div', class_='thing'):
                    votes = self._parse_votes(thread)
                    if votes >= self.min_votes:
                        link, title, comments = self._parse_links_and_title(
                            thread)
                        df = df.append(
                            [votes, subreddit, link, title, comments])
                url = soup.find('span', class_='next-button').find('a').attrs[
                    'href']
                time.sleep(2)
        output = StringIO()
        df.to_csv(output, sep='\t', index=False)
        output.seek(0)
        return output.read()

    def _parse_votes(self, thread):
        text = thread.find('div', class_='score unvoted').text
        text = text.replace('•', '0')
        multiplier = {'k': 1e3, 'm': 1e6}
        if text[-1] in multiplier:
            return int(text[:1]) * multiplier[text[-1]]
        return int(text)

    def _parse_links_and_title(self, thread):
        title_link = thread.find('a', class_='title')
        comment_link = thread.find('a', class_='comments')
        return title_link.attrs['href'], title_link.text, comment_link.attrs[
            'href']


if __name__ == '__main__':
    s = RedditScrapper('cats')
    print(s.run())
