# It's worth noting there is an aiostream library which does much of the streaming functionality we've defined ourselves here: https://aiostream.readthedocs.io/en/stable/

import asyncpg
import asyncio
 
# This keeps track of how many items we've seen so far with item_count. 
async def take(generator, to_take: int):
    item_count = 0
    
    # Enter an "async for" loop and yield each record.
    async for item in generator:
        if item_count > to_take - 1:
            return
        item_count = item_count + 1
        yield item
 
 
async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='products',
                                       password='password')
    async with connection.transaction():
        query = 'SELECT product_id, product_name from product'
        product_generator = connection.cursor(query)
        async for product in take(product_generator, 5):
            print(product)
 
        print('Got the first five products!')
 
    await connection.close()
 
 
asyncio.run(main())
