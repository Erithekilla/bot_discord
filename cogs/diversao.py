import discord
import random
from discord.ext import commands
from discord import app_commands

class Diversao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ball8(self, ctx, pergunta:str):
        aleatorio = random.randint(0,5)
        match aleatorio:
            case 1: await ctx.send("Com certeza não.")
            case 2: await ctx.send("Provavelmente não.")
            case 3: await ctx.send("Talvez.")
            case 4: await ctx.send("Provavelmente sim.")
            case 5: await ctx.send("Com certeza sim.")
            case _: await ctx.send("Não sei dizer.")

    @commands.command()
    async def jokenpo(self, ctx, escolha:str):
        escolhaBotInt = random.randint(0,2)
        escolhaPlr = escolha.lower()
        
        if escolhaPlr not in ["pedra", "papel", "tesoura"]:
            await ctx.send("Por favor, digite apenas 'Pedra', 'Papel' ou 'Tesoura'.")
            return

        opcoes = ["pedra", "papel", "tesoura"]
        escolhaBot = opcoes[escolhaBotInt]

        resultado = ""
        if escolhaBot == escolhaPlr:
            resultado = "Empate!"
        elif (escolhaPlr == "pedra" and escolhaBot == "tesoura") or \
             (escolhaPlr == "papel" and escolhaBot == "pedra") or \
             (escolhaPlr == "tesoura" and escolhaBot == "papel"):
            resultado = "Você ganhou!"
        else:
            resultado = "Você perdeu!"

        await ctx.send(f"{resultado}\nMinha escolha: {escolhaBot}\nSua escolha: {escolhaPlr}")

    @commands.command()
    async def kellvys(self, ctx:commands.Context):
        embed = discord.Embed(
            title="Kellvys", description="Eu amo esse mano!", color=discord.Color.red()
        )
        try:
            img = discord.File("kelvo.png","kelvo.png")
            embed.set_image(url="attachment://kelvo.png")
            await ctx.send(embed=embed, file=img)
        except FileNotFoundError:
            await ctx.send("Arquivo de imagem 'kelvo.png' não encontrado.")

    @app_commands.command(name="jokenpo", description="jogue um jokenpo ai.")
    @app_commands.describe(escolha="o que quer jogar? (pedra/papel/tesoura)")
    async def jokenpo2(self, interaction:discord.Interaction, escolha:str):
        escolhaBotInt = random.randint(0,2)
        escolhaPlr = escolha.lower()
        
        if escolhaPlr not in ["pedra", "papel", "tesoura"]:
            await interaction.response.send_message("Por favor, digite apenas 'Pedra', 'Papel' ou 'Tesoura'.", ephemeral=True)
            return

        opcoes = ["pedra", "papel", "tesoura"]
        escolhaBot = opcoes[escolhaBotInt]

        resultado = ""
        if escolhaBot == escolhaPlr:
            resultado = "Empate!"
        elif (escolhaPlr == "pedra" and escolhaBot == "tesoura") or \
             (escolhaPlr == "papel" and escolhaBot == "pedra") or \
             (escolhaPlr == "tesoura" and escolhaBot == "papel"):
            resultado = "Você ganhou!"
        else:
            resultado = "Você perdeu!"

        await interaction.response.send_message(f"{resultado}\nMinha escolha: {escolhaBot}\nSua escolha: {escolhaPlr}", ephemeral=True)

    @commands.command()
    async def gita(self, ctx:commands.Context):
        # (O texto é longo, mantive a estrutura original simplificada aqui para caber, mas é a mesma lógica)
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
    
   

async def setup(bot):
    await bot.add_cog(Diversao(bot))