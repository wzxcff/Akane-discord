import discord
from discord.ext import commands
from utils import get_env_id


class VoiceCog(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, message: discord.Message):
    if message.author.bot:
      return

    if message.content.startswith("hello"):
      await message.channel.send(f"Hello! {message.author.mention}")

    if not message.content.startswith("!"):
      return

    args = message.content.split()
    command = args[0].lower()

    try:
        await message.delete()
    except discord.Forbidden:
        pass
    except discord.NotFound:
        pass

    voice_commands = ["!limit", "!lock", "!unlock", "!name"]
    if command in voice_commands:
      author_voice = message.author.voice

      if (
          not author_voice
          or not author_voice.channel
          or author_voice.channel.id not in self.bot.dynamic_channels
      ):
        await message.channel.send(
            f"{message.author.mention}, ты должен находиться в своем"
            " динамическом голосовом канале!",
            delete_after=5,
        )
        return

      voice_channel = author_voice.channel

      # !limit <число>
      if command == "!limit":
        if len(args) < 2 or not args[1].isdigit():
          await message.channel.send(
              "⚠️ Укажи число! Пример: `!limit 3` (или `0` для снятия лимита)",
              delete_after=5,
          )
          return

        limit = int(args[1])
        if 0 <= limit <= 99:
          await voice_channel.edit(user_limit=limit)
          await message.channel.send(
              f"✅ Лимит мест изменен на:"
              f" `{limit if limit > 0 else 'Без лимита'}`",
              delete_after=5,
          )
        else:
          await message.channel.send(
              "⚠️ Лимит должен быть от 0 до 99!", delete_after=5
          )

      # !lock
      elif command == "!lock":
        overwrite = voice_channel.overwrites_for(message.guild.default_role)
        overwrite.connect = False
        await voice_channel.set_permissions(
            message.guild.default_role, overwrite=overwrite
        )
        await message.channel.send(
            f"🔒 Канал **{voice_channel.name}** закрыт для входа!", delete_after=5
        )

      # !unlock
      elif command == "!unlock":
        overwrite = voice_channel.overwrites_for(message.guild.default_role)
        overwrite.connect = None
        await voice_channel.set_permissions(
            message.guild.default_role, overwrite=overwrite
        )
        await message.channel.send(
            f"🔓 Канал **{voice_channel.name}** снова открыт!", delete_after=5
        )

      # !name <новое имя>
      elif command == "!name":
        if len(args) < 2:
          await message.channel.send(
              "⚠️ Укажи новое имя! Пример: `!name Играем в Apex`",
              delete_after=5,
          )
          return

        new_name = " ".join(args[1:])
        await voice_channel.edit(name=f"🔊 {new_name}")
        await message.channel.send(
            f"✏️ Канал переименован в **🔊 {new_name}**", delete_after=5
        )

  @commands.Cog.listener()
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

      self.bot.dynamic_channels.add(new_channel.id)
      await member.move_to(new_channel)

    if before.channel and before.channel.id in self.bot.dynamic_channels:
      if len(before.channel.members) == 0:
        self.bot.dynamic_channels.remove(before.channel.id)
        try:
          await before.channel.delete(reason="Динамический канал опустел и был удален")
        except discord.NotFound:
          pass


async def setup(bot):
  await bot.add_cog(VoiceCog(bot))