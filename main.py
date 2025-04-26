import discord
from discord.ext import commands

import os
import random
import math

from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix=commands.when_mentioned_or('/'), intents=discord.Intents.all())


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} olarak giriş yaptım!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"{message.author} ({message.author.id}): {message.content}")
    
    if message.content.lower() == "sa":
        await message.channel.send("as")

    await bot.process_commands(message)


@bot.tree.command(name="zenci", description="Random zenci foto")
async def zenci(interaction: discord.Interaction):
    images = os.listdir("./files/zenciler")    
    random_image = os.path.join("./files/zenciler", random.choice(images))

    await interaction.response.send_message(file=discord.File(random_image))


@bot.tree.command(name="pipikontrol", description="Pipi kontrolünü sağlar.")
async def pipikontrol(interaction: discord.Interaction):
    text = "❗🚨  PİPİ KONTROL  🚨❗\n\n👇  İnik\n\n👆  Kalkık\n"
    message = await interaction.channel.send(text)
    await message.add_reaction("👇")
    await message.add_reaction("👆")

    await interaction.response.send_message("Pipi kontrol başarılı.", ephemeral=True)

active_polls = {}

@bot.tree.command(name="anket", description="Anket oluştur")
async def anket(interaction: discord.Interaction, question: str, option1: str, option2: str, option3: str = None, option4: str = None, option5: str = None,
                option6: str = None, option7: str = None, option8: str = None, option9: str = None, option10: str = None):
    options = [option for option in [option1, option2, option3, option4, option5, option6, option7, option8, option9, option10] if option]

    if len(options) < 2:
        await interaction.response.send_message("En az 2 tane secenek eklemelisin!", ephemeral=True)
        return

    guild = interaction.guild
    USER_COUNT = sum(1 for member in guild.members if not member.bot)

    emoji_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    
    options_zip = zip(emoji_list, options)
    options = []
    for emoji, option in options_zip:
        options.append((emoji, option, 0))
    
    print(options)

    poll_message = f'📊 **{question}**\n\n'
    for i, option in enumerate(options):
        poll_message += f'{emoji_list[i]} {option[1]}\n'
    
    message = await interaction.channel.send(poll_message)
    
    for i in range(len(options)):
        await message.add_reaction(emoji_list[i])

    active_polls[message.id] = {
        "question": question,
        "options": options,
        "min_votes": math.ceil(USER_COUNT * 0.3),
        "voters": set()
    }

    await interaction.response.send_message("Poll created!", ephemeral=True)


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return 

    if reaction.message.id in active_polls:
        poll = active_polls[reaction.message.id]
        
        poll['voters'].add(user.id)

        if len(poll['voters']) >= poll['min_votes']:
            await announce_results(reaction.message, poll)


async def announce_results(poll_message, poll):
    reactions = poll_message.reactions

    result_message = f"**📊 Anket Sonuçları:**\n\n**Soru: {poll['question']}**\n\n"

    for emoji, option in poll['options']:
        if emoji in [reaction.emoji for reaction in reactions]:
            result_message += f"{emoji} {option} :  oy\n" 

    await poll_message.channel.send(result_message)

    del active_polls[poll_message.id]


if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        raise ValueError("DISCORD_TOKEN not found in environment variables.")
    
    bot.run(TOKEN)