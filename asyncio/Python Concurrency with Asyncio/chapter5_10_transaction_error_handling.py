import asyncio
import asyncpg
import logging

async def main():
    connection = await asyncpg.connect(host="127.0.0.1",
                                        port=5432,
                                        user="postgres",
                                        database="products",
                                        password="password")
    
    try:
        async with connection.transaction():

            # The first execution should succeed but the second will will fail as it's trying to insert the same primary key as the first.
            insert_brand = "INSERT INTO brand VALUES(9999, 'big_brand')"
            await connection.execute(insert_brand)
            await connection.execute(insert_brand)
    except:
        logging.exception("Error while running transaction")
    finally:
        query = """SELECT brand_name FROM brand WHERE brand_name LIKE 'big%'"""

        brands = await connection.fetch(query)
        print(brands)

        await connection.close()

asyncio.run(main())

# We get the following error. Notice that the print(brands) statement returns an empty array. Even though one of the inserts above worked, the entire transaction was rolled back due to the failure from the second insert statement
#
# ERROR:root:Error while running transaction
# Traceback (most recent call last):
#   File "/Users/edwardsnow/git/github.com/techotron/python/asyncio/chapter5_10_transaction_error_handling.py", line 18, in main
#     await connection.execute(insert_brand)
#   File "/Users/edwardsnow/.local/share/virtualenvs/asyncio-Usc9Kh22/lib/python3.10/site-packages/asyncpg/connection.py", line 317, in execute
#     return await self._protocol.query(query, timeout)
#   File "asyncpg/protocol/protocol.pyx", line 338, in query
# asyncpg.exceptions.UniqueViolationError: duplicate key value violates unique constraint "brand_pkey"
# DETAIL:  Key (brand_id)=(9999) already exists.
# []
