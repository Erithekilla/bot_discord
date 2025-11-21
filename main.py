import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot("k!", intents=intents)

@bot.event
async def on_ready():
    print(f'Conectado como {bot.user}!')
    
    # Carrega os arquivos da pasta 'cogs'
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Cog {filename} carregada.')
            except Exception as e:
                print(f'Erro ao carregar {filename}: {e}')

    try:
        synced = await bot.tree.sync()
        print(f"Foram sincronizados {len(synced)} comandos slash!")
    except Exception as e:
        print(e)

    myActivity = discord.Activity(type=discord.ActivityType.custom, name="test", state="Digite: k!ajuda")
    await bot.change_presence(status=discord.Status.online, activity=myActivity)
    print(f'Bot iniciado e pronto!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == bot.user.mention:
        await message.channel.send(f"Olá! Meu prefixo é k! , utilize k!ajuda para saber mais.")
    
    await bot.process_commands(message)

if __name__ == '__main__':
    bot.run(TOKEN)