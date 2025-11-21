import discord
import yt_dlp
from discord.ext import commands

# Variáveis globais deste módulo
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

# Função auxiliar para tocar a próxima música
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

        # ctx.bot é usado aqui pois 'bot' não é global neste arquivo
        ctx.bot.loop.create_task(ctx.send(embed=embed))
    else:
        ctx.bot.loop.create_task(ctx.send("Acabou a fila!"))

class Musica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, query:str):
        if not ctx.author.voice:
            await ctx.send("Entre em um canal de voz.")
            return
        if not ctx.voice_client:
            channel = ctx.author.voice.channel
            await channel.connect()
            embed = discord.Embed(title="Música", description="Conectando!")
            await ctx.send(embed=embed)

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
        
        await ctx.send(f"Procurando: {query}...")

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

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and (ctx.voice_client.is_playing() or ctx.voice_client.is_paused()):
            ctx.voice_client.stop()
            await ctx.send(f"Música pulada")
        else:
            await ctx.send(f"Nenhuma música tocando.")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            if ctx.guild.id in filas:
                filas[ctx.guild.id].clear()
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            await ctx.send("Desconectando!")
        else:
            await ctx.send("Não estou em um canal de voz.")

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            embed = discord.Embed(title="Música", description="Música pausada!")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Música", description="Não tem música para eu pausar :/")
            await ctx.send(embed=embed)

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            embed = discord.Embed(title="Música", description="Continuando!")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Música", description="Não tem música para eu voltar... Tente usar o !play B)")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Musica(bot))