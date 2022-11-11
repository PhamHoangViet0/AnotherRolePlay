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
    @check.guild.load(checks=[
        check.guild.not_exist,
    ])
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
            respond_msg += f'\nGM role: {gm_role.mention}'
        if player_role_id is not None:
            respond_msg += f'\nPlayer role: {player_role.mention}'
        if bot_role_id is not None:
            respond_msg += f'\nBot role: {bot_role.mention}'
        await ctx.respond(respond_msg)

    @guild_group_admin.command(name='del', description='Delete guild.')
    @check.guild.load(checks=[
        check.guild.exist,
    ])
    async def guild_del(self, ctx: discord.ApplicationContext):
        guild_dc_id = ctx.guild.id
        await m_guild.delete(guild_dc_id)
        respond_msg = 'Guild deleted.'
        await ctx.respond(respond_msg)

    @guild_group_admin.command(name='upd', description='Update roles in guild.')
    @discord.option("gm_role", description='Choose GM role')
    @discord.option("player_role", description='Choose Player role')
    @discord.option("bot_role", description='Choose Bot role')
    @check.guild.load(checks=[
        check.guild.exist,
    ])
    async def guild_upd(self,
                        ctx: discord.ApplicationContext,
                        gm_role: discord.Role,
                        player_role: discord.Role,
                        bot_role: discord.Role):
        guild_dc_id = ctx.guild.id
        gm_role_id = gm_role.id
        bot_role_id = bot_role.id
        player_role_id = player_role.id
        await m_guild.update(guild_dc_id, gm_role_id, player_role_id, bot_role_id)
        respond_msg = f'Guild updated.\n' \
                      f'GM role: {gm_role.mention}\n' \
                      f'Player role: {player_role.mention}\n' \
                      f'Bot role: {bot_role.mention}'
        await ctx.respond(respond_msg)

    @guild_group_admin.command(name='init', description='Initiates categories and channels.')
    @discord.option("arp_main_category", description='Choose AnoterRP category')
    @discord.option("gm_terminal_channel", description='Choose terminal channel')
    @discord.option("arp_terminal_category", description='Choose category for personal terminals')
    @discord.option("arp_talk_category", description='Choose category for personal chats')
    @check.guild.load(checks=[
        check.guild.exist,
        check.guild.have_roles,
    ])
    async def guild_init(self,
                         ctx: discord.ApplicationContext,
                         guild_model: m_guild.Guild,
                         arp_main_category: discord.CategoryChannel = None,
                         gm_terminal_channel: discord.TextChannel = None,
                         arp_terminal_category: discord.CategoryChannel = None,
                         arp_talk_category: discord.CategoryChannel = None, ):
        guild = ctx.guild
        gm_role = discord.utils.get(guild.roles, id=guild_model.gm_role_id)
        player_role = discord.utils.get(guild.roles, id=guild_model.player_role_id)
        bot_role = discord.utils.get(guild.roles, id=guild_model.bot_role_id)

        overwrites_GM_default = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=False,
            ),
            gm_role: discord.PermissionOverwrite(
                view_channel=True,
            ),
            bot_role: discord.PermissionOverwrite(
                view_channel=True,
            ),
        }  # access for GM and BOT
        if arp_main_category is None:
            arp_main_category = await guild.create_category(name='ARP-main',
                                                            overwrites=overwrites_GM_default)
        if gm_terminal_channel is None:
            gm_terminal_channel = await guild.create_text_channel(name='GM-terminal',
                                                                  category=arp_main_category,
                                                                  overwrites=arp_main_category.overwrites)
        if arp_terminal_category is None:
            arp_terminal_category = await guild.create_category(name='ARP-terminal',
                                                                overwrites=overwrites_GM_default)
        if arp_talk_category is None:
            arp_talk_category = await guild.create_category(name='ARP-talk',
                                                            overwrites=overwrites_GM_default)
        await m_guild.initiate(guild_model.guild_id,
                               arp_main_category.id,
                               gm_terminal_channel.id,
                               arp_terminal_category.id,
                               arp_talk_category.id)

        respond_msg = f'Guild initiated.\n' \
                      f'ARP main: {arp_main_category.mention}\n' \
                      f'{gm_terminal_channel.mention}\n' \
                      f'{arp_terminal_category.mention}\n' \
                      f'{arp_talk_category.mention}'
        await ctx.respond(respond_msg)


def setup(bot: commands.Bot):
    bot.add_cog(Guild(bot))
