import discord
from discord.ext import commands
from utils import get_env_id
import datetime


class ModerationLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_log(self, guild: discord.Guild, embed: discord.Embed):
        log_channel_id = get_env_id("MODS_LOG_CHANNEL")
        channel = guild.get_channel(log_channel_id)
        if channel:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        embed = discord.Embed(
            description=f"{member.mention} **{member.name}**",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow(),
        )
        embed.set_author(
            name="Member Joined", icon_url=member.display_avatar.url
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        created_at = discord.utils.format_dt(member.created_at, style="R")
        embed.add_field(name="Account Created", value=created_at, inline=False)

        embed.set_footer(text=f"ID: {member.id}")

        await self.send_log(member.guild, embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        embed = discord.Embed(
            description=f"{member.mention} **{member.name}**",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow(),
        )
        embed.set_author(name="Member Left", icon_url=member.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"ID: {member.id}")

        await self.send_log(member.guild, embed)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.roles == after.roles:
            return

        added_roles = [r for r in after.roles if r not in before.roles]
        removed_roles = [r for r in before.roles if r not in after.roles]

        moderator = None
        try:
            async for entry in after.guild.audit_logs(
                    limit=1, action=discord.AuditLogAction.member_role_update
            ):
                if entry.target.id == after.id:
                    moderator = entry.user
                    break
        except discord.Forbidden:
            pass

        author_name = moderator.name if moderator else after.name
        author_icon = (
            moderator.display_avatar.url
            if moderator
            else after.display_avatar.url
        )

        for role in added_roles:
            embed = discord.Embed(
                description=f"{after.mention} **was given the** `{role.name}` **role**",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow(),
            )
            embed.set_author(name=author_name, icon_url=author_icon)
            embed.set_footer(text=f"ID: {after.id}")
            await self.send_log(after.guild, embed)

        for role in removed_roles:
            embed = discord.Embed(
                description=f"{after.mention} **was removed from the** `{role.name}` **role**",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow(),
            )
            embed.set_author(name=author_name, icon_url=author_icon)
            embed.set_footer(text=f"ID: {after.id}")
            await self.send_log(after.guild, embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite):
        guild = invite.guild
        inviter = invite.inviter

        embed = discord.Embed(
            title="Invite Created",
            description=(
                f"**Creator:** {inviter.mention if inviter else 'Unknown'} (`{inviter.id if inviter else 'N/A'}`)\n"
                f"**Channel:** {invite.channel.mention}\n"
                f"**Link:** discord.gg/{invite.code}"
            ),
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow(),
        )

        if inviter:
            embed.set_author(
                name=f"{inviter.name} ({inviter.id})",
                icon_url=inviter.display_avatar.url,
            )
            embed.set_thumbnail(url=inviter.display_avatar.url)

        max_uses = "Unlimited" if invite.max_uses == 0 else f"{invite.max_uses}"
        expires = (
            "Unlimited"
            if invite.max_age == 0
            else discord.utils.format_dt(
                discord.utils.utcnow()
                + datetime.timedelta(seconds=invite.max_age),
                style="R",
            )
        )

        embed.add_field(name="Usage limit", value=max_uses, inline=True)
        embed.add_field(name="Expires", value=expires, inline=True)
        embed.add_field(
            name="Temporary access",
            value="Yes" if invite.temporary else "No",
            inline=True,
        )

        embed.set_footer(text=f"Code: {invite.code}")

        await self.send_log(guild, embed)

    # TODO: Extend when admin commands added


async def setup(bot):
    await bot.add_cog(ModerationLogs(bot))