import asyncio
import asyncpg

from util import async_timed

product_query = \
"""
SELECT
p.product_id,
p.product_name,
p.brand_id,
s.sku_id,
pc.product_color_name,
ps.product_size_name
FROM product as p
JOIN sku as s on s.product_id = p.product_id
JOIN product_color as pc on pc.product_color_id = s.product_color_id
JOIN product_size as ps on ps.product_size_id = s.product_size_id
WHERE p.product_id = 100"""

async def query_product(pool):
    async with pool.acquire() as connection:
        return await connection.fetchrow(product_query)

@async_timed()
async def query_products_synchronously(pool, queries):
    return [await query_product(pool) for _ in range(queries)]
         
@async_timed()
async def query_products_concurrently(pool, queries):
    queries = [query_product(pool) for _ in range(queries)]
    return await asyncio.gather(*queries)

async def main():
    async with asyncpg.create_pool(host="127.0.0.1",
                                    port=5432,
                                    user="postgres",
                                    password="password",
                                    database="products",
                                    min_size=6,
                                    max_size=6) as pool:
        
        # The slight difference in these 2 functions is that one is await-ing each coroutine in the list comp (synchronous) and the other
        #  is calling gather on the list of coroutines (async)

        # The results on this will look something like this:
        # starting <function query_products_synchronously at 0x1099c3b50> with args (<asyncpg.pool.Pool object at 0x1092baa80>, 10000) {}
        # finished <function query_products_synchronously at 0x1099c3b50> in 17.5329 second(s)
        # starting <function query_products_concurrently at 0x1099c3c70> with args (<asyncpg.pool.Pool object at 0x1092baa80>, 10000) {}
        # finished <function query_products_concurrently at 0x1099c3c70> in 5.7965 second(s)        

        await query_products_synchronously(pool, 10000)
        await query_products_concurrently(pool, 10000)

asyncio.run(main())
