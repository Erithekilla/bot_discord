import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot("!",intents=intents)

@bot.event
async def on_ready():

    try:
        synced = await bot.tree.sync()
        print(f"Foram sincronizados {len(synced)} comandos!")
    except Exception as e:
        print(e)

    myActivity = discord.Activity(type=discord.ActivityType.streaming, name="!ajuda")
    await bot.change_presence(status=discord.Status.idle, activity=myActivity)
    print(f'Bot iniciado!')

@bot.command()
async def ajuda(ctx:commands.Context):
    embed = discord.Embed(
        title=f"Ajuda!",
        description=f"Krishna tem vários comandos, listamos alguns para você!\n\n1- !server_avatar\n\n2- !avatar\n\n3- !falar",
        color=discord.Color.red()
    )
    embed.set_author(name="Krishna")
    img = discord.File("krishna.jpg","krishna.jpg")
    embed.set_thumbnail(url="attachment://krishna.jpg")
    await ctx.send(embed=embed, file=img)
    


@bot.command()
async def server_avatar(ctx:commands.Context):
    avatar = ctx.guild.icon
    await ctx.send(avatar)

@bot.command()
async def avatar(ctx:commands.Context, mention: discord.Member=None):
    if mention is None:
        mention = ctx.author

    avatar = mention.display_avatar.url
    embed = discord.Embed(
        title=f'Avatar do {mention.name}',
        color=discord.Color.red()
    )

    embed.set_image(url=avatar)
    await ctx.send(embed=embed)

@bot.command()
async def falar(ctx:commands.Context, *, texto):
    await ctx.send(texto)

@bot.tree.command(name="ola", description="Um olá para você!")
async def ola(interaction: discord.Interaction):
    mention = interaction.user.mention
    await interaction.response.send_message(f"Olá viado de bosta! {mention}", ephemeral=True)

@bot.tree.command(name="soma", description="Faça a soma de dois valores.")
@app_commands.describe(
    numero1="Primeiro número da soma",
    numero2="Segundo número da soma"
)
async def somar(interaction:discord.Interaction, numero1:int,numero2:int):
    soma = numero1 + numero2
    await interaction.response.send_message(f"A soma é {soma}", ephemeral=True)

@bot.tree.command(name="calculo", description="Calcule dois valores!")
@app_commands.describe(
    numero1="Digite o primeiro valor",
    numero2="Digite o segundo valor",
    sinal="Que tipo de calculo deseja fazer? (+ , - , * , /)"
)
async def calculo(interaction:discord.Interaction, numero1:int,numero2:int,sinal:str):
    if sinal == "+":
        soma = numero1 + numero2
        await interaction.response.send_message(soma, ephemeral=True)
    elif sinal == "-":
        soma = numero1 - numero2
        await interaction.response.send_message(soma, ephemeral=True)
    elif sinal == "*":
        soma = numero1 * numero2
        await interaction.response.send_message(soma, ephemeral=True)
    elif sinal == "/":
        soma = numero1 / numero2
        await interaction.response.send_message(soma, ephemeral=True)
    else:
        await interaction.response.send_message("Error.", ephemeral=True)
    
@bot.tree.command(name="avatar", description="Pegue o avatar de alguma pessoa!")
@app_commands.describe(
    membro="Digite o nome do membro!"
)
async def avatar(interaction:discord.Interaction, membro:discord.Member):
    apelido = membro.display_name

    embed = discord.Embed(
        title=f"Nome do membro: {apelido}",
        color=membro.color
    )

    embed.set_image(url=membro.display_avatar)

    await interaction.response.send_message(embed=embed, ephemeral=True)
    


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == bot.user.mention:
        await message.channel.send(f"Olá! Meu prefixo é ! , utilize !ajuda para saber mais.")
    
    await bot.process_commands(message)


bot.run(TOKEN)
