from random import choice
import discord
from discord.ext import commands, tasks

STATUSES = [
    discord.Game(name="Minecraft"),
    discord.Game(name="Cyberpunk 2077"),
    discord.Game(name="Stardew Valley"),
    discord.Game(name="Terraria"),
    discord.Game(name="The Sims 4"),
    discord.Game(name="Honkai: Star Rail"),
    discord.Game(name="Zenless Zone Zero"),
    discord.Game(name="Valorant"),
    discord.Game(name="Counter-Strike 2"),
    discord.Game(name="Baldur's Gate 3"),

    discord.Activity(
        type=discord.ActivityType.listening,
        name="Rammstein — Sonne"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Rammstein — Deutschland"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Rammstein — Du Hast"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Rammstein — Radio"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Rammstein — Engel"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Måneskin — THE LONELIEST"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Mitski — My Love Mine All Mine"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="The Weeknd — After Hours"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="YOASOBI — アイドル"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Ado — 唱"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Kenshi Yonezu — KICK BACK"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="RADWIMPS — 前前前世"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Linkin Park — The Emptiness Machine"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Bring Me The Horizon — Can You Feel My Heart"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Deftones — Change (In the House of Flies)"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="System Of A Down — Aerials"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Arctic Monkeys — 505"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Cigarettes After Sex — Apocalypse"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Lana Del Rey — Summertime Sadness"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Lady Gaga — Judas"
    ),
]


class StatusCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.change_status.start()

  def cog_unload(self):
    self.change_status.cancel()

  @tasks.loop(minutes=60)
  async def change_status(self):
    new_status = choice(STATUSES)
    await self.bot.change_presence(activity=new_status)

  @change_status.before_loop
  async def before_status_loop(self):
    await self.bot.wait_until_ready()


async def setup(bot):
  await bot.add_cog(StatusCog(bot))