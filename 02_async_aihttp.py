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
    print(f'{task_name=}')
    url = f'https://jsonplaceholder.typicode.com/albums/{album}/photos'

    response = await session.get(url)
    photos_json = await response.json()

    return [Photo.from_json(photo) for photo in photos_json]


async def main():
    async with aiohttp.ClientSession() as session:
        photos_in_album = await asyncio.gather(*(photos_by_album(f'Task {i + 1}', album, session) 
                                                for i, album in enumerate(range(2, 30))))
        
        photos_count = sum([len(cur) for cur in photos_in_album])
        print(photos_count)
        # print_photo_titles(photos)


if __name__ == '__main__':
    asyncio.run(main())