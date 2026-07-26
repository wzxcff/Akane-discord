import discord
from dotenv import load_dotenv
import os
from random import choice


load_dotenv()

GIFS = [
    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXNiMm15OW1ic2V2Nms5Z3lyOHVsajJlbmU4aTVqMW1hM3UxeDJtbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/In0Lpu4FVivjISX9HT/giphy.gif",
    "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGI1Z3I1eTdnaGxvemlzZWJqYThldnNscTdvMXk2N2czODN1dDhjbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/o1pWpHPHw2JbLDUQLb/giphy.gif",
    "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExazRiMXRjbjk0MW1tdDR5eGRpOXZjaXQ2ajZteDZtcmlnbW52bmN6eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/y4nk5bgwpWL6T5Ax9y/giphy.gif",
    "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGMxb2Noemw3bXcwZjU2ZGRrZXdkMnA2MjdweWdmdHNvanEyYmwzMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/D7PwMxzlDx9HfOnSP4/giphy.gif"
]


async def get_env_id(string_name: str) -> int:
    return int(os.getenv(string_name))


class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dynamic_channels = set()

    async def on_ready(self):
        print(f"Logged in as {self.user}")

        creator_channel_id = await get_env_id("CREATOR_CHANNEL_ID")
        creator_channel = self.get_channel(creator_channel_id)

        if creator_channel and creator_channel.category:
            for channel in creator_channel.category.voice_channels:
                if channel.id != creator_channel_id and len(channel.members) == 0:
                    try:
                        await channel.delete()
                        print(f"Удален старый пустой канал: {channel.name}")
                    except discord.HTTPException:
                        pass

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

        embed.add_field(
            name="Чек правила, не хотим чтобы ты отлетел(а).",
            value=f"<#{await get_env_id("RULES_CHANNEL_ID")}>",
            inline=False
        )

        if member.display_avatar:
            embed.set_thumbnail(url=member.display_avatar.url)

        embed.set_image(
            url=choice(GIFS)
        )

        guild_icon = member.guild.icon.url if member.guild.icon else None

        embed.set_footer(
            text=f"Ты наш {member.guild.member_count}-й мембер! (уро)",
            icon_url=guild_icon,
        )

        await welcome_channel.send(content=f"Эй! {member.mention}!", embed=embed)

    async def on_voice_state_update(
            self,
            member: discord.Member,
            before: discord.VoiceState,
            after: discord.VoiceState,
    ):
        creator_channel_id = await get_env_id("CREATOR_CHANNEL_ID")

        if after.channel and after.channel.id == creator_channel_id:
            category = after.channel.category

            new_channel = await member.guild.create_voice_channel(
                name=f"🔊 {member.display_name}'s voice channel",
                category=category,
                reason="Динамический голосовой канал",
            )

            self.dynamic_channels.add(new_channel.id)

            await member.move_to(new_channel)

        # -------------------------------------------------------------

        if before.channel and before.channel.id in self.dynamic_channels:
            if len(before.channel.members) == 0:
                self.dynamic_channels.remove(before.channel.id)
                try:
                    await before.channel.delete(
                        reason="Динамический канал опустел и был удален"
                    )
                except discord.NotFound:
                    pass





intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

client = Client(intents=intents)
client.run(f"{os.getenv('BOT_TOKEN')}")