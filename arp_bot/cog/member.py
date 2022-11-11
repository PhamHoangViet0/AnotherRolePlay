import logging
# declare logger
logger = logging.getLogger(__name__)

from discord.ext import commands
import discord
from decorator import check
from model import guild as m_guild, member as m_member


class Member(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name='reg', description='Register member.')
    @check.guild.load(checks=[
        check.guild.exist,
    ])
    @check.check_model(checks=[
        check.guild.have_all,
        check.member.is_player,
    ])
    @check.member.load(checks=[
        check.member.not_exist,
    ])
    async def reg(self, ctx: discord.ApplicationContext, guild_model: m_guild.Guild, **kwargs):
        author = ctx.author
        await m_member.register(guild_model.guild_id, author.id)
        respond_msg = 'New member registered.'
        await ctx.respond(respond_msg)

    @commands.slash_command(name='unreg', description='Unregister member.')
    @check.guild.load(checks=[
        check.guild.exist,
        check.guild.have_all,
        check.member.is_player,
    ])
    @check.member.load(checks=[
        check.member.exist,
    ])
    async def unreg(self, ctx: discord.ApplicationContext, member_model: m_member.Member, **kwargs):
        await m_member.unregister(member_model.member_id)
        respond_msg = 'Member deleted.'
        await ctx.respond(respond_msg)


def setup(bot: commands.Bot):
    bot.add_cog(Member(bot))
