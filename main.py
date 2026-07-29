import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


async def get_env_id(string_name: str) -> int:
  return int(os.getenv(string_name))


class AkaneBot(commands.Bot):

  def __init__(self):
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    intents.members = True

    super().__init__(command_prefix="!", intents=intents)
    self.dynamic_channels = set()

  async def setup_hook(self):
    for filename in os.listdir("./cogs"):
      if filename.endswith(".py"):
        cog_name = filename[:-3]
        await self.load_extension(f"cogs.{cog_name}")
        print(f"Cog loaded: {cog_name}")

  async def on_ready(self):
    print(f"Logged in as {self.user} (ID: {self.user.id})")

    creator_channel_id = await get_env_id("CREATOR_CHANNEL_ID")
    creator_channel = self.get_channel(creator_channel_id)

    if creator_channel and creator_channel.category:
      for channel in creator_channel.category.voice_channels:
        if channel.id != creator_channel_id and len(channel.members) == 0:
          try:
            await channel.delete()
            print(f"Removed old empty channel: {channel.name}")
          except discord.HTTPException:
            pass


if __name__ == "__main__":
  bot = AkaneBot()
  bot.run(os.getenv("BOT_TOKEN"))