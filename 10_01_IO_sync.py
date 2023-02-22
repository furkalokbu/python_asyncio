import requests
from measure_time import measure_time


def download_site(url, session):
    with session.get(url) as response:
        print(f'Read {len(response.content)} from {url}')


@measure_time
def download_all_site(sites):
    with requests.Session() as session:
        for site in sites:
            download_site(site, session)


if __name__ == '__main__':
    sites = [
        'https://www.maestrochecks.com/',
        'https://www.checksify.com/',
    ]*10

    download_all_site(sites)
