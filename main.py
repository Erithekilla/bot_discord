import discord
import os
import json
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
import yt_dlp

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CONFIG_FILE = "config.json"
intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot("!",intents=intents)

filas = {}

def format_duration(seconds):
    if seconds is None:
        return "Desconhecida"
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def load_welcome():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_welcome(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

@bot.event
async def on_ready():

    try:
        synced = await bot.tree.sync()
        print(f"Foram sincronizados {len(synced)} comandos!")
    except Exception as e:
        print(e)

    myActivity = discord.Activity(type=discord.ActivityType.streaming, name="!ajuda")
    await bot.change_presence(status=discord.Status.online, activity=myActivity)
    print(f'Bot iniciado!')

@bot.command()
async def ajuda(ctx:commands.Context):
    embed = discord.Embed(
        title=f"Ajuda!",
        description=f"Krishna tem vários comandos, listamos alguns para você!\n\n1- !server_avatar\n\n2- !avatar\n\n3- !falar \n\n4- !play\n\n5- !pause\n\n6- !resume\n\n7- !skip\n\n8- !clear",
        color=discord.Color.red()
    )
    embed.set_author(name="Krishna")
    img = discord.File("krishna.jpg","krishna.jpg")
    embed.set_thumbnail(url="attachment://krishna.jpg")
    await ctx.send(embed=embed, file=img)

@bot.command()
async def clear(ctx, amount:int):
    try:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"Apagamos {amount} mensagens...", delete_after=5)
    except discord.Forbidden:
        await ctx.send("Não tenho permissão para apagar mensagens nesse chat.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command()
async def gita(ctx:commands.Context):
    await ctx.send(f"""Às vezes você me pergunta
Por que é que eu sou tão calado
Não falo de amor quase nada
Nem fico sorrindo ao teu lado
Você pensa em mim toda hora
Me come, me cospe, me deixa
Talvez você não entenda
Mas hoje eu vou lhe mostrar

Eu sou a luz das estrelas
Eu sou a cor do luar
Eu sou as coisas da vida
Eu sou o medo de amar
Eu sou o medo do fraco
A força da imaginação
O blefe do jogador
Eu sou
Eu fui
Eu vou (Gita, Gita, Gita, Gita, Gita)

Eu sou o seu sacrifício
A placa de contramão
O sangue no olhar do vampiro
E as juras de maldição
Eu sou a vela que acende
Eu sou a luz que se apaga
Eu sou a beira do abismo
Eu sou
O tudo
E o nada

Por quê? Você me pergunta
Perguntas não vão lhe mostrar
Que eu sou feito da terra
Do fogo, da água e do ar

Você me tem todo dia
Mas não sabe se é bom ou ruim
Mas saiba que eu estou em você
Mas você não está em mim

Das telhas, eu sou o telhado
A pesca do pescador
A letra A tem meu nome
Dos sonhos, eu sou o amor

Eu sou a dona de casa
Nos peg-pags do mundo
Eu sou a mão do carrasco
Sou raso
Largo
Profundo (Gita, Gita, Gita, Gita, Gita)

Eu sou a mosca da sopa
E o dente do tubarão
Eu sou os olhos do cego
E a cegueira da visão

É, mas eu sou o amargo da língua
A mãe, o pai e o avô
O filho que ainda não veio
O início
O fim
E o meio

O início
O fim
E o meio
Eu sou o início
O fim e o meio
Eu sou o início
O fim
E o meio""")

@bot.command()
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, canal: discord.TextChannel):
    config = load_welcome()

    server_id = str(ctx.guild.id)

    if server_id not in config:
        config[server_id] = {}
    
    config[server_id]['welcome_channel_id'] = canal.id

    save_welcome(config)

    await ctx.send(f"Canal de boas-vindas agora fica em {canal.mention}!")

@setwelcome.error
async def setwelcome_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Por favor, marque o canal na qual deseja colocar como o canal de bem-vindo.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Você não tem permissão.")

@bot.event
async def on_member_join(member):
    config = load_welcome()
    server_id = str(member.guild.id)

    if server_id in config and 'welcome_channel_id' in config[server_id]:
        channel_id = config[server_id]['welcome_channel_id']
        channel = bot.get_channel(channel_id)

        if channel:
            embed = discord.Embed(
                title=f"Seja bem-vindo(a), {member.name}",
                description=f"Esperamos que você se divirta no {member.guild.name}",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.display_avatar.url)

            await channel.send(embed=embed)
        else:
            print(f"Error: Não foi possível encontrar o canal de boas-vindas: {channel_id} \nno servidor: {member.guild.name}")

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
    await ctx.channel.purge(limit=1)
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

@bot.command()
async def play(ctx, *, query:str):
    if not ctx.author.voice:
        await ctx.send("Entre em um canal de voz.")
        return
    if not ctx.voice_client:
        channel = ctx.author.voice.channel
        await channel.connect()
        embed = discord.Embed(
            title="Música",
            description="Conectando!"
        )

    YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'noplaylist': 'True',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as yld:
            try:
                info = yld.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            except (IndexError, TypeError):
                await ctx.send(f"Não encontrei a música: {query}")
                return

    

    guild_id = ctx.guild.id
    if guild_id not in filas:
        filas[guild_id] = []

    info['requester'] = ctx.author
    filas[guild_id].append(info)

    await ctx.send(f"Adicionado a fila: {info['title']} ")

    if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
        play_next(ctx)

def play_next(ctx):
    guild_id = ctx.guild.id
    if guild_id in filas and filas[guild_id]:
        song_info = filas[guild_id].pop(0)

        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn',
        }

        url = song_info['url']
        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)

        voice_client = ctx.voice_client
        voice_client.play(source, after=lambda e: play_next(ctx))

        embed = discord.Embed(
            title="Tocando agora!",
            description=f"{song_info['title']} {song_info['webpage_url']}"
        )

        embed.add_field(name="Canal", value=song_info['uploader'])
        embed.add_field(name="Duração", value=format_duration(song_info.get('duration')))
        embed.set_thumbnail(url=song_info['thumbnail'])
        embed.set_footer(text=f"pedido por: {song_info['requester'].name}")

        bot.loop.create_task(ctx.send(embed=embed))
    else:
        bot.loop.create_task(ctx.send("Acabou a fila!"))

@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
        ctx.voice_client.stop()
        await ctx.send(f"Música pulada")
    else:
        await ctx.send(f"Nenhuma música tocando.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        if ctx.guild.id in filas:
            filas[ctx.guild.id].clear()

        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send("Desconectando!")
    else:
        await ctx.send("Não estou em um canal de voz.")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        embed = discord.Embed(
            title="Música",
            description="Música pausada!"
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Música",
            description="Não tem música para eu pausar :/"
        )
        await ctx.send(embed=embed)

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        embed = discord.Embed(
            title="Música",
            description="Continuando!"
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Música",
            description="Não tem música para eu voltar... Tente usar o !play B)"
        )
        await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == bot.user.mention:
        await message.channel.send(f"Olá! Meu prefixo é ! , utilize !ajuda para saber mais.")
    
    await bot.process_commands(message)

bot.run(TOKEN)
