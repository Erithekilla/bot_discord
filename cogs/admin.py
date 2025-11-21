import discord
import json
from discord.ext import commands

CONFIG_FILE = "config.json"
ROLE_CONFIG = "role.json"

def load_welcome():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_welcome(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def load_role():
    try:
        with open(ROLE_CONFIG, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_role(config):
    with open(ROLE_CONFIG, 'w') as f:
        json.dump(config, f, indent=4)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, amount:int):
        if amount <= 100:
            try:
                await ctx.channel.purge(limit=amount+1)
                await ctx.send(f"Apagando {amount} mensagens...", delete_after=5)
            except discord.Forbidden:
                await ctx.send("Não tenho permissão para apagar mensagens nesse chat.")
            except Exception as e:
                await ctx.send(f"Error: {e}")
        else:
            await ctx.send("Limite de mensagens que posso apagar é de 100.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setrole(self, ctx, cargo: discord.Role):
        config = load_role()
        server_id = str(ctx.guild.id)

        if server_id not in config:
            config[server_id] = {}

        config[server_id]['cargo_id'] = cargo.id

        save_role(config)
        await ctx.send(f"Cargo automático é {cargo.mention}")

    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setwelcome(self, ctx, canal: discord.TextChannel):
        config = load_welcome()
        server_id = str(ctx.guild.id)

        if server_id not in config:
            config[server_id] = {}
        
        config[server_id]['welcome_channel_id'] = canal.id
        save_welcome(config)
        await ctx.send(f"Canal de boas-vindas agora fica em {canal.mention}!")

    @setwelcome.error
    async def setwelcome_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Por favor, marque o canal na qual deseja colocar como o canal de bem-vindo.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Você não tem permissão.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        config = load_welcome()
        server_id = str(member.guild.id)

        if server_id in config and 'welcome_channel_id' in config[server_id]:
            channel_id = config[server_id]['welcome_channel_id']
            channel = self.bot.get_channel(channel_id)

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
        
        configR = load_role()

        if server_id in configR and 'cargo_id' in configR[server_id]:
            role_id = configR[server_id]['cargo_id']
            role = member.guild.get_role(role_id)

            if role:
                try:
                    await member.add_roles(role)
                    print(f"Dei o cargo {role} para {member.name}")
                except discord.Forbidden:
                    print("Não tenho permissão")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print(f"O cargo não existe no servidor.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, mention: discord.Member, *, motivo=None):
        if mention == ctx.author:
            await ctx.send("Você não pode se expulsar...")
        elif mention == self.bot.user:
            await ctx.send("Ha ha, engraçadão você.")
        else:
            try:
                await mention.kick(reason=motivo)
                motivo = f"{motivo}" if motivo else "(Sem motivo escrito)"
                await ctx.send(f"O User: {mention.name} foi expulso por {motivo}")
            except discord.Forbidden:
                await ctx.send("Você não tem permissão bot.")
            except Exception as e:
                await ctx.send(f"Ocorreu um error: {e}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, mention: discord.Member, *, motivo=None, delete_messages_days=0):
        if mention == ctx.author:
            await ctx.send("Você não pode se banir...")
        elif mention == self.bot.user:
            await ctx.send("Ha ha, engraçadão você. (Versão Ban)")
        else:
            try:
                await mention.ban(reason=motivo, delete_message_days=delete_messages_days)
                motivo = f"{motivo}" if motivo else "(Sem motivo escrito)"
                await ctx.send(f"O User: {mention.name} \nFoi banido por {motivo}\nMensagem apagadas em dias {delete_messages_days}")
            except discord.Forbidden:
                await ctx.send("Você não tem permissão bot.")
            except Exception as e:
                await ctx.send(f"Ocorreu um error: {e}")
        

async def setup(bot):
    await bot.add_cog(Admin(bot))