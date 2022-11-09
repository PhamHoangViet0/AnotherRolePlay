import logging

# declare logger
logger = logging.getLogger(__name__)

from discord.ext import commands
import discord
from decorator import check
from model import guild as m_guild


class Guild(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    guild_group_admin = discord.SlashCommandGroup(
        name='guild_adm',
        description='Guild admin commands',
        guild_only=True,
        default_member_permissions=discord.Permissions(administrator=True),
        # checks=[
        #     permissions.is_GM().predicate
        # ]
    )

    @guild_group_admin.command(name='reg', description='Register guild.')
    @discord.option("gm_role", description='Choose GM role')
    @discord.option("player_role", description='Choose Player role')
    @discord.option("bot_role", description='Choose Bot role')
    @check.guild.not_exist()
    # @decorator
    async def reg(self,
                  ctx: discord.ApplicationContext,
                  gm_role: discord.Role = None,
                  player_role: discord.Role = None,
                  bot_role: discord.Role = None):
        guild_dc_id = ctx.guild.id
        gm_role_id = gm_role.id if gm_role is not None else None
        player_role_id = player_role.id if player_role is not None else None
        bot_role_id = bot_role.id if bot_role is not None else None
        await m_guild.register(guild_dc_id, gm_role_id, player_role_id, bot_role_id)

        respond_msg = 'Guild registered.'
        if gm_role_id is not None:
            respond_msg += f'\nGM role: <@&{gm_role_id}>'
        if player_role_id is not None:
            respond_msg += f'\nPlayer role: <@&{player_role_id}>'
        if bot_role_id is not None:
            respond_msg += f'\nBot role: <@&{bot_role_id}>'
        await ctx.respond(respond_msg)

    @guild_group_admin.command(name='del', description='Delete guild.')
    @check.guild.exist()
    # @commands.has_permissions(administrator=True)
    # @discord.default_permissions(administrator=True)
    # @commands.guild_only()
    async def guild_del(self, ctx: discord.ApplicationContext):
        guild_dc_id = ctx.guild.id
        await m_guild.delete(guild_dc_id)
        respond_msg = 'Guild deleted.'
        await ctx.respond(respond_msg)


def setup(bot: commands.Bot):
    bot.add_cog(Guild(bot))
