import aiohttp, asyncio

class Photo:
    def __init__(self, album_id, photo_id, title, url, thumbnail_url):
        self.thumbnail_url = thumbnail_url
        self.url = url
        self.title = title
        self.photo_id = photo_id
        self.album_id = album_id

    @classmethod
    def from_json(cls, obj):
        return Photo(obj['albumId'], obj['id'], obj['title'], obj['url'], obj['thumbnailUrl'])


def print_photo_titles(photos):
    for photo in photos:
        print(f'{photo.title}', end='\n')


async def photos_by_album(task_name, album, session):

    if not isinstance(album, int):
        raise RuntimeError('Invalid album number')

    print(f'{task_name=}')
    url = f'https://jsonplaceholder.typicode.com/albums/{album}/photos'

    response = await session.get(url)
    photos_json = await response.json()

    return [Photo.from_json(photo) for photo in photos_json]


async def download_album(albums):
    photos = []
    async with aiohttp.ClientSession() as session:
        for album in albums:
            photos.extend(await photos_by_album(f't{album}', album, session))


async def main1():
    task1 = asyncio.create_task(download_album([1,2,'a',4]))
    try:
        result = await task1
    except Exception as ex:
        print(repr(ex))

    print('sleeping in main')
    await asyncio.sleep(5)
    print('after sleeping')


def handle_result(future):
    print(future.result())


async def main2():
    task1 = asyncio.create_task(download_album([1,2,'a',4]))
    task1.add_done_callback(handle_result)

    print('sleeping in main')
    await asyncio.sleep(5)
    print('after sleeping')


async def main_gather():
    async with aiohttp.ClientSession() as session:    
        tasks = [
            photos_by_album('task1', 1, session),
            photos_by_album('task2', 2, session),
            photos_by_album('task3', 'a', session),
            photos_by_album('task4', 4, session),
        ]
    
        results = await asyncio.gather(*tasks, return_exceptions=True)
        photos = []

        for result in results:
            if isinstance(result, Exception):
                print(repr(result))
            else:
                photos.extend(result)

        print_photo_titles(photos)


if __name__== '__main__':
    asyncio.run(main_gather())
    print('main ended')
