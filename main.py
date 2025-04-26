import discord
from discord.ext import commands

import os
import random
import math

from dotenv import load_dotenv
from db import create_connection, execute_query, execute_read_query

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DB_NAME = os.getenv("DB_NAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

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


@bot.tree.command(name="yazkenara", description="Atasözü oluştur")
async def yazkenara(interaction: discord.Interaction, mesaj: str):
    if not mesaj:
        interaction.response.send_message("Mesaj boş olamaz!", ephemeral=True)
        return

    query = """
        INSERT INTO messages (guild_id, user_id, username, message, datetime)
        VALUES (%s, %s, %s, %s, %s)
    """

    guild_id = interaction.guild.id
    user_id = interaction.user.id
    username = interaction.user.name
    message = mesaj
    datetime = interaction.created_at
    values = (guild_id, user_id, username, message, datetime)

    connection = create_connection(DB_NAME, USER, PASSWORD, HOST, PORT)
    execute_query(connection, query, values)
    connection.close()

    await interaction.response.send_message(f"<@{user_id}> atasözü ekledi: ***{mesaj}***")
    

@bot.tree.command(name="atasozu", description="Random atasözü")
async def atasozu(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    query = f"SELECT user_id, message FROM messages WHERE guild_id = {guild_id} ORDER BY RANDOM() LIMIT 1"
    
    connection = create_connection(DB_NAME, USER, PASSWORD, HOST, PORT)
    result = execute_read_query(connection, query)
    connection.close()

    if not result:
            await interaction.response.send_message("Henüz kimse bir söz yazmamış 😢")
            return
    
    user_id, message = result[0]
    templates = [
        "Bir zamanlar bilge bir adam olan <@{user_id}> demişti ki: ***{message}***",
        "Ünlü Japon bilim adamı <@{user_id}> bir gün şöyle demişti: ***{message}***",
        "Antik Yunan filozofu <@{user_id}> vaktiyle şöyle buyurmuştu: ***{message}***",
        "<@{user_id}> bir gün dedi ki: ***{message}***",
        "Tarihin tozlu sayfalarından: <@{user_id}> şöyle demiş: ***{message}***"
    ]
    template = random.choice(templates)
    response = template.format(user_id=user_id, message=message)
    await interaction.response.send_message(response)

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("DISCORD_TOKEN not found in environment variables.")

    if not all([DB_NAME, USER, PASSWORD, HOST, PORT]):
        raise ValueError("Database connection details not found in environment variables.")

    connection = create_connection(DB_NAME, USER, PASSWORD, HOST, PORT)

    if connection is None:
        raise ValueError("Database connection failed.")
    
    # Create the messages table if it doesn't exist
    query = """CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    username TEXT NOT NULL,
    message TEXT NOT NULL,
    datetime TIMESTAMP NOT NULL
    );
    """

    execute_query(connection, query)

    connection.close()

    bot.run(TOKEN)