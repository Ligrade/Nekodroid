import discord
from discord.ext import commands

redcross = '<:white_cross_mark:612474623333761031>'


class Moderator(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        try:
            if not reason:
                await member.ban()
                await ctx.send('✅ | Member' + member + 'was successfully banned ! Good bye !')
            else:
                await member.ban(reason=reason)
                await ctx.send(
                    f'✅ | Member {member} was successfully banned for the following reason : {reason} ! Good bye !')
        except discord.HTTPException:
            await ctx.send(f'{redcross} | Couldn\'t ban {member}.')

    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, *, member: discord.Member):
        try:
            await member.kick()
            await ctx.send('Member', member, 'was successfully kicked ! Babaï !')
        except discord.HTTPException:
            await ctx.send(f'{redcross} | Couldn\'t kick {member}.')

    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def clear(self, ctx, amount: int):
        await ctx.message.delete()
        try:
            deleted = await ctx.channel.purge(limit=amount)
            await ctx.send(f"✅ | `{len(deleted)}` messages successfully deleted !", delete_after=5)
        except discord.HTTPException:
            await ctx.send(f"{redcross} | I'm sorry, but I can't delete messages older than two weeks. Nya !")

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def setmute(self, ctx):
        muted = discord.utils.get(ctx.guild.roles, name='Muted')
        if muted is not None:
            await ctx.send(f'{redcross} | The `Muted` role was created already, nya.')
        else:
            guild = ctx.guild
            await guild.create_role(name="Muted", send_messages=False, add_reactions=False, speak=False,
                                    colour=0x36393E)
            await ctx.send('✅ | The `Muted` role was succesfully created !')

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def mute(self, ctx, usr: discord.Member, reason=None):
        muted = discord.utils.get(ctx.guild.roles, name='Muted')
        if muted is not None:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            await usr.add_roles(role)
            if not reason:
                await ctx.send(f'✅ | Member `{usr}` was successfully muted, nya !')
            else:
                await ctx.send(
                    f'✅ | Member `{usr}` was successfully muted for the following reason :```{reason}``` Nya !')
            try:
                await usr.send(
                    f'Hi, {usr}. You were muted on **{ctx.guild.name}** by {ctx.author.name} for the following reason :```{reason}```')
            except discord.Forbidden:
                return
        else:
            await ctx.send(
                f'{redcross} | The `Muted` role doesn\'t exist. Please create it first, or let me do that for you by typing `nya!setmute`.')

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def unmute(self, ctx, usr: discord.Member):
        mrole = discord.utils.get(ctx.guild.roles, name="Muted")
        await usr.remove_roles(mrole)
        await ctx.send(f'✅ | Member `{usr}` was successfully unmuted, nya.')
        try:
            await usr.send(f'Hi, {usr}. You were unmuted by {ctx.author.name} on **{ctx.guild.name}**, nya !')
        except discord.Forbidden:
            return

    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def warn(self, ctx, usr: discord.Member, reason):
        await ctx.send(f'✅ | Member `{usr}` has been warned, nya. Reason : ```{reason}```')
        try:
            await usr.send(
                f'Hi, {usr}. You were warned on guild **{ctx.guild.name}** for the following : ```{reason}```')
        except discord.Forbidden:
            return


def setup(bot):
    bot.add_cog(Moderator(bot))
