import app_exception as exc
import aiomysql
import mysql_conn


async def isExist(guild_dc_id):
    conn: aiomysql.Connection
    async with mysql_conn.pool.acquire() as conn:
        cur: aiomysql.Cursor
        async with conn.cursor(aiomysql.DictCursor) as cur:
            query_check = f'''
SELECT COUNT(1)
FROM   guilds
WHERE  guild_dc_id = %s; '''
            await cur.execute(query_check, (guild_dc_id))
            res = await cur.fetchone()
            return res['COUNT(1)'] == 1


async def register(guild_dc_id, gm_role_id, player_role_id, bot_role_id):
    conn: aiomysql.Connection
    async with mysql_conn.pool.acquire() as conn:
        cur: aiomysql.Cursor
        async with conn.cursor(aiomysql.DictCursor) as cur:
            query_add = f'''
INSERT INTO guilds
            (guild_dc_id,
             gm_role_id,
             player_role_id,
             bot_role_id)
VALUES      (%s,
             %s,
             %s,
             %s); '''
            await cur.execute(query_add, (guild_dc_id,
                                          gm_role_id,
                                          player_role_id,
                                          bot_role_id))
        await conn.commit()


async def delete(guild_dc_id):
    conn: aiomysql.Connection
    async with mysql_conn.pool.acquire() as conn:
        cur: aiomysql.Cursor
        async with conn.cursor(aiomysql.DictCursor) as cur:
            query_delete = '''
DELETE FROM guilds
WHERE  guild_dc_id = %s; '''
            await cur.execute(query_delete, guild_dc_id)
        await conn.commit()
