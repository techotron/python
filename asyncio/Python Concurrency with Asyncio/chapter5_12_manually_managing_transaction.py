# Using a context manager for transactions is usually the best approach. This will demonstrate how and why you might want to manually manage the transaction (eg custom code to handle the rollback).

import asyncio
import asyncpg
from asyncpg.transaction import Transaction
 
 
async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='products',
                                       password='password')
    transaction: Transaction = connection.transaction()
    await transaction.start()
    try:
        await connection.execute("INSERT INTO brand "
                                 "VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand "
                                 "VALUES(DEFAULT, 'brand_2')")
    except asyncpg.PostgresError:
        # Custom code can go here. The transaction doesn't have to be rolled back for example. Other statements could be placed here.
        print('Errors, rolling back transaction!')
        await transaction.rollback()
    else:
        print('No errors, committing transaction!')
        await transaction.commit()
 
    query = """SELECT brand_name FROM brand
                WHERE brand_name LIKE 'brand%'"""
    brands = await connection.fetch(query)
    print(brands)
 
    await connection.close()
 
asyncio.run(main())
