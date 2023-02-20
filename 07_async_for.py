import asyncio


async def fetch_doc(doc):
    await asyncio.sleep(3)
    return doc


async def get_pages(docs):
    for cur_doc in docs:
        doc = await fetch_doc(cur_doc)
        for page in doc:
            yield page


async def main():
    async for page in get_pages(['doc1', 'doc2']):
        print(f'finally {page}')


if __name__ == '__main__':
    asyncio.run(main())

