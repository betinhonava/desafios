import argparse

from scrapper import RedditScrapper

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Scrapper para reddit. Procura e retorna as threads mais '
                    'votadas.'
    )
    parser.add_argument('subreddits',
                        help='Lista de subreddits para a busca, separados '
                             'por ponto-e-vírgula ";".')
    parser.add_argument('-v', '--min_votes', type=int, default=5000,
                        help='Número mínimo de votos das threads procuradas.'
                             ' (default=5000).')
    parser.add_argument('-p', '--num_pages', type=int, default=5,
                        help='Número de páginas a serem raspadas em cada'
                             ' subreddit.')

    args = parser.parse_args()

    scrapper = RedditScrapper(args.subreddits, args.min_votes, args.num_pages)
    output = scrapper.run()
    print(output)
