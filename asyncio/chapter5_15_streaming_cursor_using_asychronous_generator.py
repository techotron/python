# Building on the previous example, we can use the async generator to fetch one row at a time with a for loop-like syntax.
# Postgres requires us to use a transaction in order to use streaming features so we'll need to put this inside a transaction context. 
# When inside the transaction context, we call the cursor method on the Connection class. 
import asyncpg
import asyncio
 
 
async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='products',
                                       password='password')
 
# This only pulls a few rows (defaults to prefetching 50 rows) into memory at a time to iterate over. The benefit being if we had a table with loads of rows, we're not pulling them all into memory before processing them in the loop.
    query = 'SELECT product_id, product_name FROM product'
    async with connection.transaction():
        async for product in connection.cursor(query):
            print(product)
 
    await connection.close()
 
 
asyncio.run(main())
