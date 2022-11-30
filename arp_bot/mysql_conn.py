import logging
# declare logger
logger = logging.getLogger(__name__)

import asyncio
import aiomysql
import discord
import json

import os

# loop = asyncio.get_event_loop()


def get_pool(loop: asyncio.AbstractEventLoop) -> aiomysql.Pool:
    config_path = os.path.join('..', 'config')
    with open(os.path.join(config_path, 'mysql_conn_config.json'), 'r') as mysql_config:
        settings = json.load(mysql_config)
    pool = loop.run_until_complete(aiomysql.create_pool(
        host=settings['host'],
        user=settings['user'],
        password=settings['password'],
        db=settings['db'],
        charset=settings['charset'],
        port=settings['port'],
        cursorclass=aiomysql.cursors.DictCursor,
        loop=loop
    ))
    logger.info('Pool created')
    return pool


async def close_pool(pool: aiomysql.Pool):
    pool.close()
    await pool.wait_closed()
    logger.info('Pool closed')


# def close_pool(pool: aiomysql.Pool):
#     pool.close()
#     logger.info('Pool closed')


pool = None