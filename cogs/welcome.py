import os
from random import choice
import discord
from discord.ext import commands
from utils import get_env_id

GIFS = [
    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXNiMm15OW1ic2V2Nms5Z3lyOHVsajJlbmU4aTVqMW1hM3UxeDJtbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/In0Lpu4FVivjISX9HT/giphy.gif",
    "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGI1Z3I1eTdnaGxvemlzZWJqYThldnNscTdvMXk2N2czODN1dDhjbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/o1pWpHPHw2JbLDUQLb/giphy.gif",
    "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExazRiMXRjbjk0MW1tdDR5eGRpOXZjaXQ2ajZteDZtcmlnbW52bmN6eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/y4nk5bgwpWL6T5Ax9y/giphy.gif",
    "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGMxb2Noemw3bXcwZjU2ZGRrZXdkMnA2MjdweWdmdHNvanEyYmwzMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/D7PwMxzlDx9HfOnSP4/giphy.gif",
]


class WelcomeCog(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_member_join(self, member: discord.Member):
    welcome_channel = self.bot.get_channel(
        await get_env_id("WELCOME_CHANNEL_ID")
    )
    rules_channel_id = await get_env_id("RULES_CHANNEL_ID")

    try:
      auto_role_id = await get_env_id("AUTO_ROLE_ID")
      role = member.guild.get_role(auto_role_id)
      if role:
        await member.add_roles(role)
    except Exception as e:
      print(f"Не удалось выдать роль: {e}")

    if not welcome_channel:
      return

    embed = discord.Embed(
        title="Нью генчик пожаловал",
        description=f"Приветствуем на сервере, {member.mention}!",
        color=discord.Color.gold(),
    )

    embed.add_field(
        name="Чек правила, не хотим чтобы ты отлетел(а).",
        value=f"<#{rules_channel_id}>",
        inline=False,
    )

    if member.display_avatar:
      embed.set_thumbnail(url=member.display_avatar.url)

    embed.set_image(url=choice(GIFS))

    guild_icon = member.guild.icon.url if member.guild.icon else None

    embed.set_footer(
        text=f"Ты наш {member.guild.member_count}-й мембер! (уро)",
        icon_url=guild_icon,
    )

    await welcome_channel.send(content=f"Эй! {member.mention}!", embed=embed)


async def setup(bot):
  await bot.add_cog(WelcomeCog(bot))