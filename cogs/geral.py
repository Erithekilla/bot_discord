import discord
from discord import app_commands
from discord.ext import commands

class View(discord.ui.View):
        def __init__(self, embeds):
            super().__init__(timeout=60)
            self.embeds = embeds
            self.index = 0
            self.updateButtons()

        
        def updateButtons(self):
            total = len(self.embeds)
            current_embed = self.embeds[self.index]
            if not current_embed.footer.text:
                current_embed.set_footer(text=f"Página atual: {self.index + 1} de {total}")

        @discord.ui.button(label="Volte", style=discord.ButtonStyle.red)
        async def previousButton(self, interaction: discord.Interaction, button:discord.ui.Button):
            if self.index > 0:
                self.index -= 1

            self.updateButtons()
            await interaction.response.edit_message(embed=self.embeds[self.index], view=self)
        
        @discord.ui.button(label="Passe", style=discord.ButtonStyle.green)
        async def nextButton(self, interaction: discord.Interaction, button:discord.ui.Button):
            if self.index < len(self.embeds) - 1:
                self.index += 1

            self.updateButtons()
            await interaction.response.edit_message(embed=self.embeds[self.index], view=self)
        
        #@discord.ui.button(label="Fechar", style=discord.ButtonStyle.gray)
        #async def previousButton(self, interaction: discord.Interaction, button:discord.ui.Button):
            #await interaction.message.delete() 



class Geral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ajuda(self, ctx:commands.Context):
        embed = discord.Embed(
            title=f"Ajuda!",
            description=f"Krishna tem vários comandos, listamos alguns para você!\n\n1- k!server_avatar\n\n2- k!avatar\n\n3- k!falar \n\n4- k!play\n\n5- k!pause\n\n6- k!resume\n\n7- k!skip\n\n8- k!clear",
            color=discord.Color.red()
        )
        embed.set_author(name="Krishna")
        try:
            img = discord.File("krishna.jpg","krishna.jpg")
            embed.set_thumbnail(url="attachment://krishna.jpg")
            await ctx.send(embed=embed, file=img)
        except FileNotFoundError:
            await ctx.send(embed=embed)

    @commands.command()
    async def server_avatar(self, ctx:commands.Context):
        avatar = ctx.guild.icon
        if avatar:
            await ctx.send(avatar)
        else:
            await ctx.send("Este servidor não tem ícone.")

    # Comando de Prefixo
    @commands.command()
    async def avatar(self, ctx:commands.Context, mention: discord.Member=None):
        if mention is None:
            mention = ctx.author
        avatar = mention.display_avatar.url
        embed = discord.Embed(title=f'Avatar do {mention.name}', color=discord.Color.red())
        embed.set_image(url=avatar)
        await ctx.send(embed=embed)

    @commands.command()
    async def falar(self, ctx:commands.Context, *, texto):
        await ctx.channel.purge(limit=1)
        await ctx.send(texto)

    

    @commands.command()
    async def botao(self, ctx):
        embed1 = discord.Embed(
            title="Oi",
            description="Nao"
        )
        embed2 = discord.Embed(
            title="Oi2",
            description="Nao"
        )
        embed3 = discord.Embed(
            title="Oi3",
            description="Nao"
        )
        embed4 = discord.Embed(
            title="Oi4",
            description="Nao"
        )

        lista_embeds = [embed1, embed2, embed3, embed4]
        view = View(lista_embeds)

        await ctx.send(embed=lista_embeds[0], view=view)


    # --- Slash Commands ---
    
    @app_commands.command(name="ola", description="Um olá para você!")
    async def ola(self, interaction: discord.Interaction):
        mention = interaction.user.mention
        await interaction.response.send_message(f"Olá viado de bosta! {mention}", ephemeral=True)

    @app_commands.command(name="soma", description="Faça a soma de dois valores.")
    @app_commands.describe(numero1="Primeiro número da soma", numero2="Segundo número da soma")
    async def somar(self, interaction:discord.Interaction, numero1:int, numero2:int):
        soma = numero1 + numero2
        await interaction.response.send_message(f"A soma é {soma}", ephemeral=True)

    @app_commands.command(name="calculo", description="Calcule dois valores!")
    @app_commands.describe(numero1="Digite o primeiro valor", numero2="Digite o segundo valor", sinal="Que tipo de calculo deseja fazer? (+ , - , * , /)")
    async def calculo(self, interaction:discord.Interaction, numero1:int, numero2:int, sinal:str):
        if sinal == "+":
            res = numero1 + numero2
        elif sinal == "-":
            res = numero1 - numero2
        elif sinal == "*":
            res = numero1 * numero2
        elif sinal == "/":
            res = numero1 / numero2
        else:
            await interaction.response.send_message("Error.", ephemeral=True)
            return
        await interaction.response.send_message(res, ephemeral=True)

    @app_commands.command(name="avatar", description="Pegue o avatar de alguma pessoa!")
    @app_commands.describe(membro="Digite o nome do membro!")
    async def avatar_slash(self, interaction:discord.Interaction, membro:discord.Member):
        apelido = membro.display_name
        embed = discord.Embed(title=f"Nome do membro: {apelido}", color=membro.color)
        embed.set_image(url=membro.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Geral(bot))