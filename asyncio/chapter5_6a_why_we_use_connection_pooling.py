# This example demonstrates why we should use connection pooling. Running this will result in an error:
# > asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress
#
# This is because with SQL, one connection is one socket connection to the database and here, we're trying to 
# read the results of multiple queries conncurrently. The solution to this is to create multiple connections
# to the database. Since creating connections to the DB is resource intensive, we'll cache them so they can be
# accessed when needed. This is known as connection pooling.


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

async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='products',
                                       password='password')
    print('Creating the product database...')
    queries = [connection.execute(product_query),
               connection.execute(product_query)]
    results = await asyncio.gather(*queries) 

asyncio.run(main())
