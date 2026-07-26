import discord
from dotenv import load_dotenv
import os


load_dotenv()


async def get_env_id(string_name: str) -> int:
    return int(os.getenv(string_name))


class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith("hello"):
            await message.channel.send(f"Hello! {message.author.mention}")

    async def on_member_join(self, member: discord.Member):
        welcome_channel = self.get_channel(await get_env_id("WELCOME_CHANNEL_ID"))
        if not welcome_channel:
            return

        embed = discord.Embed(
            title="Нью генчик пожаловал",
            description=(
                f"Приветствуем на сервере, {member.mention}!"
            ),
            color=discord.Color.gold(),
        )

        if member.display_avatar:
            embed.set_thumbnail(url=member.display_avatar.url)

        embed.set_image(
            url="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGI1Z3I1eTdnaGxvemlzZWJqYThldnNscTdvMXk2N2czODN1dDhjbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/o1pWpHPHw2JbLDUQLb/giphy.gif"
        )

        guild_icon = member.guild.icon.url if member.guild.icon else None

        embed.set_footer(
            text=f"Ты наш {member.guild.member_count}-й мембер! (уро)",
            icon_url=guild_icon,
        )

        await welcome_channel.send(content=f"Эй! {member.mention}!", embed=embed)




intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

client = Client(intents=intents)
client.run(f"{os.getenv('BOT_TOKEN')}")