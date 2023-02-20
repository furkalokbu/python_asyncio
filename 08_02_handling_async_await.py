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
    async with aiohttp.ClientSession() as session:
        for album in albums:
            try:
                yield await photos_by_album(f't{album}', album, session)
            except Exception as ex:
                print(repr(ex))


async def main():
    async for photos in download_album([1,2,'a',4]):
        print(print_photo_titles(photos))


if __name__== '__main__':
    asyncio.run(main())
    print('eded main')
