import asyncio
import asyncpg

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
    # acquire() will use up one of the available connections in the pool. If none are available, it'll suspend execution until one becomes available.
    # When the code leaves the context manager, the connection is returned to the pool.
    async with pool.acquire() as connection:
        # fetchrow() will return a single row (the first one returned from the database), using the connection acquired from the pool
        return await connection.fetchrow(product_query)

async def main():
    # This will create a connection pool which establishes the min_size value fo connections to the database. 
    async with asyncpg.create_pool(host="127.0.0.1",
                                    port=5432,
                                    user="postgres",
                                    password="password",
                                    database="products",
                                    min_size=6,
                                    max_size=6) as pool:
        # Reminder: asnycio.gather() will gather all coroutines, waits on the Futures and returns their results in order. Here, we're running the same coroutine (the one returned by query_product()) twice
        #  and feeding in the same connection pool within the context.
        await asyncio.gather(query_product(pool), query_product(pool))

asyncio.run(main())
