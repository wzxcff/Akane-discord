import datetime
import discord
from discord.ext import commands


class AntiSpamCog(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.last_message_time = {}
    self.cooldown_seconds = 1.5

  @commands.Cog.listener()
  async def on_message(self, message: discord.Message):
    if message.author.bot or not message.guild:
      return

    user_id = message.author.id
    now = datetime.datetime.now(datetime.timezone.utc)

    if user_id in self.last_message_time:
      delta = (now - self.last_message_time[user_id]).total_seconds()

      if delta < self.cooldown_seconds:
        try:
          await message.delete()
        except discord.Forbidden:
          pass

        await message.channel.send(
            f"{message.author.mention}, не флуди, пес <3", delete_after=2
        )
        return

    self.last_message_time[user_id] = now


async def setup(bot):
  await bot.add_cog(AntiSpamCog(bot))