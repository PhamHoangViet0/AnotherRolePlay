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


async def register(guild_dc_id,
                   gm_role_id,
                   player_role_id,
                   bot_role_id):
    conn: aiomysql.Connection
    async with mysql_conn.pool.acquire() as conn:
        cur: aiomysql.Cursor
        async with conn.cursor(aiomysql.DictCursor) as cur:
            query_reg = f'''
INSERT INTO guilds
            (guild_dc_id,
             gm_role_id,
             player_role_id,
             bot_role_id)
VALUES      (%s,
             %s,
             %s,
             %s); '''
            await cur.execute(query_reg, (guild_dc_id,
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


async def update(guild_dc_id,
                 gm_role_id,
                 player_role_id,
                 bot_role_id):
    conn: aiomysql.Connection
    async with mysql_conn.pool.acquire() as conn:
        cur: aiomysql.Cursor
        async with conn.cursor(aiomysql.DictCursor) as cur:
            query_upd = '''
UPDATE guilds
SET    gm_role_id = %s,
       player_role_id = %s,
       bot_role_id = %s
WHERE  guild_dc_id = %s; '''
            await cur.execute(query_upd, (gm_role_id, player_role_id, bot_role_id, guild_dc_id))
        await conn.commit()


async def initiate(guild_id,
                   arp_main_category_id,
                   gm_terminal_channel_id,
                   arp_terminal_category_id,
                   arp_talk_category_id):
    conn: aiomysql.Connection
    async with mysql_conn.pool.acquire() as conn:
        cur: aiomysql.Cursor
        async with conn.cursor(aiomysql.DictCursor) as cur:
            query_init = '''
UPDATE guilds
SET    arp_main_category_id = %s,
       gm_terminal_channel_id = %s,
       arp_terminal_category_id = %s,
       arp_talk_category_id = %s
WHERE  guild_id = %s; '''
            await cur.execute(query_init, (arp_main_category_id,
                                           gm_terminal_channel_id,
                                           arp_terminal_category_id,
                                           arp_talk_category_id,
                                           guild_id))
        await conn.commit()


async def get_roles(guild_dc_id):
    conn: aiomysql.Connection
    async with mysql_conn.pool.acquire() as conn:
        cur: aiomysql.Cursor
        async with conn.cursor(aiomysql.DictCursor) as cur:
            query_get_roles = '''
SELECT gm_role_id,
       player_role_id,
       bot_role_id
FROM   guilds
WHERE  guild_dc_id = %s; '''
            await cur.execute(query_get_roles, guild_dc_id)
            res = await cur.fetchone()
    return res


async def get(guild_dc_id):
    conn: aiomysql.Connection
    async with mysql_conn.pool.acquire() as conn:
        cur: aiomysql.Cursor
        async with conn.cursor(aiomysql.DictCursor) as cur:
            query_get = '''
SELECT *
FROM   guilds
WHERE  guild_dc_id = %s; '''
            await cur.execute(query_get, guild_dc_id)
            res = await cur.fetchone()
    return res


class Guild:
    def __init__(self, guild_data):
        self.guild_id = guild_data.get('guild_id')
        self.guild_dc_id = guild_data.get('guild_dc_id')
        self.gm_role_id = guild_data.get('gm_role_id')
        self.player_role_id = guild_data.get('player_role_id')
        self.bot_role_id = guild_data.get('bot_role_id')
        self.arp_main_category_id = guild_data.get('arp_main_category_id')
        self.gm_terminal_channel_id = guild_data.get('gm_terminal_channel_id')
        self.arp_terminal_category_id = guild_data.get('arp_terminal_category_id')
        self.arp_talk_category_id = guild_data.get('arp_talk_category_id')

