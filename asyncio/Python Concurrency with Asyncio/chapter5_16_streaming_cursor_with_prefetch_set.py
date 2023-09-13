import asyncpg
import asyncio
 
 
async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='products',
                                       password='password')
    async with connection.transaction():
        query = 'SELECT product_id, product_name from product'

        # Create the cursor for the query (we're not using the "async for" pattern here). This is because the cursor in asyncpg is both an async generator and an awaitable.
        cursor = await connection.cursor(query)

        # Move the cursor forward 500 records - this will skip the first 500 records in our query result
        await cursor.forward(500)

        # Get the next 100 records from the current cursor position
        products = await cursor.fetch(100)
        for product in products:
            print(product)
 
    await connection.close()
 
 
asyncio.run(main())
