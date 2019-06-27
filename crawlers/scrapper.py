import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

REDDIT_OLD_URL = 'https://old.reddit.com/r/'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
NUM_REGEX = re.compile('[^0-9eE.]')

FIELDS = ['Pontuação', 'Subreddit', 'Título', 'Comentários', 'Link']


class RedditScrapper:

    def __init__(self, subreddits='', min_votes=5000, num_pages=5):
        self.subreddits = subreddits.split(';')
        self.min_votes = min_votes
        self.num_pages = num_pages

    def run(self, format='string'):
        result = []
        for subreddit in self.subreddits:
            # initial url for subreddit
            url = urljoin(REDDIT_OLD_URL, subreddit)
            for i in range(self.num_pages):
                content = requests.get(url, headers=HEADERS).content
                soup = BeautifulSoup(content, features="html.parser")
                for thread in soup.find_all('div', class_='thing'):
                    votes = self._parse_votes(thread)
                    if votes >= self.min_votes:
                        link, title, comments = self._parse_links_and_title(
                            thread, url)
                        result.append(
                            {
                                key: value for key, value in
                                zip(FIELDS,
                                    (votes, subreddit, title, comments, link))
                            }
                        )
                # find next page link and update url for next iteration
                url = soup.find('span', class_='next-button').find('a').attrs[
                    'href']
                # slowing dow the scrapper
                time.sleep(2)

        return self._format_result(result, format)

    def _parse_votes(self, thread):
        text = thread.find('div', class_='score unvoted').text
        # deal with new threads w/out votes
        text = text.replace('•', '0')
        # deal with thousand multipliers (is million necessary?)
        multiplier = {'k': 1e3, 'm': 1e6}
        if text[-1] in multiplier:
            return int(text[:1]) * multiplier[text[-1]]
        return int(text)

    def _parse_links_and_title(self, thread, url):
        title_link = thread.find('a', class_='title')
        # outbound links are absoltute but inbound links are relative
        if 'outbound' in title_link.attrs['class']:
            title_href = title_link.attrs['href']
        else:
            title_href = urljoin(url, title_link.attrs['href'])
        comment_link = thread.find('a', class_='comments')
        return title_href, title_link.text, comment_link.attrs[
            'href']

    def _format_result(self, result, format):
        if not result:
            return "Nenhuma thread bombamdo no momento :("
        str_list = []
        for thread in result:
            str_list.append(
                '\n'.join(
                    [f'{key} = {value}' for key, value in thread.items()]))
        if format == 'list':
            return str_list
        return '\n\n'.join(str_list)


if __name__ == '__main__':
    s = RedditScrapper('cats;programming;brazil', 1000)
    print(s.run())
