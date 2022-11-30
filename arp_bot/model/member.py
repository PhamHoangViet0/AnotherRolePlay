import app_exception as exc
import aiomysql
import mysql_conn


async def register(guild_id, member_dc_id):
    conn: aiomysql.Connection
    async with mysql_conn.pool.acquire() as conn:
        cur: aiomysql.Cursor
        async with conn.cursor(aiomysql.DictCursor) as cur:
            query_add = f'''
INSERT INTO members
            (guild_id,
             member_dc_id)
VALUES      (%s,
             %s); '''
            await cur.execute(query_add, (guild_id, member_dc_id))
        await conn.commit()


async def unregister(member_id):
    conn: aiomysql.Connection
    async with mysql_conn.pool.acquire() as conn:
        cur: aiomysql.Cursor
        async with conn.cursor(aiomysql.DictCursor) as cur:
            query_del = f'''
DELETE FROM members
WHERE  member_id = %s; '''
            await cur.execute(query_del, member_id)
        await conn.commit()


async def get(guild_id, member_dc_id):
    conn: aiomysql.Connection
    async with mysql_conn.pool.acquire() as conn:
        cur: aiomysql.Cursor
        async with conn.cursor(aiomysql.DictCursor) as cur:
            query_get = '''
SELECT *
FROM   members
WHERE  guild_id = %s
   AND member_dc_id = %s; '''
            await cur.execute(query_get, (guild_id, member_dc_id))
            res = await cur.fetchone()
    return res


class Member:
    def __init__(self, member_data):
        self.member_id = member_data.get('member_id')
        self.member_dc_id = member_data.get('member_dc_id')
        self.guild_id = member_data.get('guild_id')
