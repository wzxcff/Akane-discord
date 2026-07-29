from random import choice
import discord
from discord.ext import commands, tasks

STATUSES = [
    discord.Game(name="League of Legends"),
    discord.Game(name="Genshin Impact"),
    discord.Game(name="World of Warcraft"),
    discord.Game(name="Dota 2"),
    discord.Game(name="Grand Theft Auto VI"),
    discord.Game(name="Half-Life 3"),
    discord.Activity(type=discord.ActivityType.listening, name="YOASOBI — Idol (アイドル)"),
    discord.Activity(type=discord.ActivityType.listening, name="RADWIMPS feat. Toaka — Suzume"),
    discord.Activity(type=discord.ActivityType.listening, name="Lofi Hip Hop Radio 🎧"),
    discord.CustomActivity(name="Делает какао для участников ☕"),
    discord.Activity(type=discord.ActivityType.competing, name="Соревнуюсь по поеданию оперативы на Pi 🥧"),
    discord.CustomActivity(name="Играет с вашими нервами 💅 (в частности разраба)"),
]


class StatusCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.change_status.start()

  def cog_unload(self):
    self.change_status.cancel()

  @tasks.loop(minutes=30)
  async def change_status(self):
    new_status = choice(STATUSES)
    await self.bot.change_presence(activity=new_status)

  @change_status.before_loop
  async def before_status_loop(self):
    await self.bot.wait_until_ready()


async def setup(bot):
  await bot.add_cog(StatusCog(bot))