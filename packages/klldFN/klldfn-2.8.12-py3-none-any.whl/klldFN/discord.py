"""Discord bot integration for klldFN"""
import discord
from discord.ext import commands
from discord import Option, AutocompleteContext
import asyncio
import aiohttp
import json
import FortniteAPIAsync
from typing import TYPE_CHECKING, Optional, Any, List
from rich.progress import Progress, TextColumn, BarColumn, SpinnerColumn, TimeElapsedColumn
import arabic_reshaper
from bidi.algorithm import get_display

# Import from local modules
from .config import configuration, translations, translations_system, get_Language
from .utils import check_and_update_package, reshape_arabic_text, sanic_start, run_clients, rotate_status
from . import epicgames
from .clients import clients
from .client import klldFN_client
from .utils import UpdateTranslations

# Global variables
fortnite_api = FortniteAPIAsync.APIClient()

class DiscordBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def on_ready(self):
        updater = UpdateTranslations()
        await updater()
        get_Language = configuration.read()["Control"]["Language"]

        config = configuration.read()['sanic web']['start']
        if config:
            await sanic_start()

        progress = Progress(
            TextColumn("[bold blue]{task.description}", justify="right"),
            BarColumn(bar_width=None),
            SpinnerColumn(spinner_name="clock", style="bright_yellow", speed=1.0),
            TimeElapsedColumn(),
        )        

        with progress:
            klldFN_Starting = translations_system.read()["translations"]["klldFN-Starting"][get_Language]
            updating_package = translations_system.read()["translations"]["updating-package"][get_Language]
            updating_translations = translations_system.read()["translations"]["updating-translations"][get_Language]
            starting_discord = translations_system.read()["translations"]["starting-discord"][get_Language]
            discord_bot_start = translations_system.read()["translations"]["discord-bot-start"][get_Language]

            if get_Language == "ar":
                klldFN_Starting = reshape_arabic_text(klldFN_Starting)
                updating_package = reshape_arabic_text(updating_package)
                updating_translations = reshape_arabic_text(updating_translations)
                starting_discord = reshape_arabic_text(starting_discord)
                discord_bot_start = reshape_arabic_text(discord_bot_start)

            task1 = progress.add_task(f"[bold green]Starting {klldFN_Starting}", total=4)
            await asyncio.sleep(2)  
            progress.update(task1, advance=3, description=f"[bold green]{updating_package}")
            await check_and_update_package()
            await asyncio.sleep(1)  
            progress.update(task1, advance=4, description=f"[bold green]{updating_translations}")
            await asyncio.sleep(1)  
            progress.update(task1, advance=5, description=f"[blue]{starting_discord}")
            await asyncio.sleep(2) 

        print(f'{discord_bot_start} {self.user}')

        await asyncio.gather(
            run_clients(),
            rotate_status() 
        )

# Initialize Discord bot
discord_bot = DiscordBot(command_prefix="!", intents=discord.Intents.default())


@discord_bot.slash_command(name="ping", description="Check the bot's latency")
async def ping(ctx):
    latency = round(discord_bot.latency * 1000)
    embed = discord.Embed(
        title="Pong!",
        description=f"Latency: {latency}ms",
        color=discord.Color.blue()
    )
    await ctx.respond(embed=embed)

# Get owner IDs from configuration
def get_owner_ids():
    return [int(owner_id) for owner_id in configuration.read()["discord"]["ownerId"]]

async def client_name_autocomplete(ctx: AutocompleteContext):
    client_names = [client.user.display_name for client in clients]
    return [name for name in client_names if name.lower().startswith(ctx.value.lower())]

async def get_skins_autocomplete(ctx: AutocompleteContext):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://fortnite-api.com/v2/cosmetics/br/search/All?matchMethod=contains&backendType=AthenaCharacter') as resp:
            if resp.status == 200:
                data = await resp.json()
                skin_names = [item['name'] for item in data['data']]
                return [name for name in skin_names if name.lower().startswith(ctx.value.lower())]
            return []
        
async def get_emotes_autocomplete(ctx: AutocompleteContext):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://fortnite-api.com/v2/cosmetics/br/search/All?matchMethod=contains&backendType=AthenaDance') as resp:
            if resp.status == 200:
                data = await resp.json()
                skin_names = [item['name'] for item in data['data']]
                return [name for name in skin_names if name.lower().startswith(ctx.value.lower())]
            return []

@discord_bot.slash_command(name="onlinebots")
async def onlinebots(ctx):
    clients_info = []
    
    for client in clients:
        clients_info.append({
            'display_name': client.user.display_name,
            'friends': len(client.friends)
        })
    
    embed = discord.Embed(title=f"{len(clients)} **bots Online!**", color=discord.Color.blue())
    
    for info in clients_info:
        embed.add_field(name="Display Name", value=info['display_name'], inline=True)
        embed.add_field(name="Friends", value=info['friends'], inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
    
    await ctx.respond(embed=embed)

@discord_bot.slash_command(name="skin", description="Set skin")
async def skin(
    ctx, 
    client: Option(str, "The display name of the client", autocomplete=client_name_autocomplete, required=True), 
    skin: Option(str, "The name of the skin to set", autocomplete=get_skins_autocomplete, required=True)
):
    try:
        client = next(c for c in clients if c.user.display_name == client)
    except StopIteration:
        embed = discord.Embed(
            title="Error",
            description="Client not found",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
        return
    
    if client:
        try:
            display_name_post = client.user.display_name
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(
                language=get_Language, 
                matchMethod="contains", 
                name=skin, 
                backendType="AthenaCharacter"
            )
            await client.party.me.set_outfit(asset=cosmetic.id)
            skin_set_message = f"Skin set to {cosmetic.name}!"
            icon_url = f"https://fortnite-api.com/images/cosmetics/br/{cosmetic.id}/icon.png"
            
            # Create embed for POST request response
            embed = discord.Embed(
                title=skin_set_message,
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=icon_url)
            embed.set_author(name=f"{client.user.display_name}")
            
            await ctx.respond(embed=embed)
        except fortnite_api.exceptions.NotFound:
            embed = discord.Embed(
                title="Error",
                description="Cosmetic not found",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(
            title="Error",
            description="Client not found",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)

@discord_bot.slash_command(name="emote", description="Set emote")
async def emote(
    ctx, 
    client: Option(str, "The display name of the client", autocomplete=client_name_autocomplete, required=True), 
    emote: Option(str, "The name of the emote to set", autocomplete=get_emotes_autocomplete, required=True)
):
    try:
        client = next(c for c in clients if c.user.display_name == client)
    except StopIteration:
        embed = discord.Embed(
            title="Error",
            description="Client not found",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
        return
    
    if client:
        try:
            display_name_post = client.user.display_name
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(
                language=get_Language, 
                matchMethod="contains", 
                name=emote, 
                backendType="AthenaDance"
            )
            await client.party.me.set_emote(asset=cosmetic.id)
            emote_set_message = f"Emote set to {cosmetic.name}!"
            icon_url = f"https://fortnite-api.com/images/cosmetics/br/{cosmetic.id}/icon.png"
            
            # Create embed for POST request response
            embed = discord.Embed(
                title=emote_set_message,
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=icon_url)
            embed.set_author(name=f"{client.user.display_name}")
            
            await ctx.respond(embed=embed)
        except fortnite_api.exceptions.NotFound:
            embed = discord.Embed(
                title="Error",
                description="Cosmetic not found",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(
            title="Error",
            description="Client not found",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)

@discord_bot.slash_command(name="createbot", description="Create a new bot")
async def createbot(ctx):
    # Check if the user is the owner
    owner_ids = get_owner_ids()
    if ctx.author.id not in owner_ids:
        await ctx.respond("You are not authorized to use this command.", ephemeral=True)
        return

    # Create a new bot
    device_code = await epicgames.create_device_code()

    button = discord.ui.Button(label="Login To Your Epic Games Account", url=device_code[0])
    view = discord.ui.View()
    view.add_item(button)

    embed = discord.Embed(
        title="Device Authentication",
        description="Click Login To Your Epic Games Account"
    )
    embed.set_image(url="https://media.discordapp.net/attachments/1191706931593756712/1249318367207231529/image.png?ex=6666dde5&is=66658c65&hm=df5c35cde2fe24bd1495262513b0e4a9be663f6d43be20fbf6497f28f93885c1&=&format=webp")

    await ctx.respond(embed=embed, view=view, ephemeral=True)

    try:
        user1 = await epicgames.wait_for_device_code_completion(code=device_code[1])
    except asyncio.TimeoutError:
        cancel_embed = discord.Embed(
            title="Canceled Login",
            description="The login process took too long and was canceled.",
            color=discord.Color.red()
        )
        await ctx.respond(embed=cancel_embed, ephemeral=True)
        return

    await ctx.respond('Authentication details saved', ephemeral=True)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{user1.account_id}/deviceAuth",
                headers={
                    "Authorization": f"bearer {user1.access_token}",
                    "Content-Type": "application/json",
                },
            ) as response:
                auths = await response.json()
            DEVICE_ID = auths['deviceId']
            ACCOUNT_ID = auths['accountId']
            SECRET = auths['secret']

            # Save authentication details to auths.json
            try:
                with open('auths.json', 'r+') as file:
                    data = json.load(file)
                    data['auths'].append({
                        'deviceId': DEVICE_ID,
                        'accountId': ACCOUNT_ID,
                        'secret': SECRET
                    })
                    file.seek(0)
                    json.dump(data, file, indent=4)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                await ctx.respond(f"Failed to save authentication details: {str(e)}", ephemeral=True)
                return

            # Create a new bot
            client = klldFN_client(auths['deviceId'], auths['accountId'], auths['secret'])
            if client:
                clients.append(client)

            try:
                await asyncio.gather(client.start())
            except Exception as e:
                await ctx.respond(f"Failed to start client: {str(e)}", ephemeral=True)
                return

            # Inform that the client is starting
            embed_regular = discord.Embed(title=f"Starting client: {user1.display_name}")
            await ctx.user.send(embed=embed_regular)
            await asyncio.sleep(1)

    except KeyError as e:
        embed = discord.Embed(
            title="Bot Creation Failed",
            description=f"Failed to create bot: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)
    except Exception as e:
        embed = discord.Embed(
            title="Bot Creation Failed",
            description=f"An error occurred: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)

@discord_bot.slash_command(name="restartbots", description="Restart all bots")
async def restartbots(ctx):
    owner_ids = get_owner_ids()
    if ctx.author.id not in owner_ids:
        await ctx.respond("You are not authorized to use this command.", ephemeral=True)
        return
    try:
        if not clients:
            embed = discord.Embed(
                title="No Bots",
                description="There are no bots to restart.",
                color=discord.Color.orange()
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return
        
        embed = discord.Embed(
            title="Bots Restarted",
            description="All bots have been successfully restarted.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed, ephemeral=True)
        for client in clients:
            await client.restart()

    except Exception as e:
        embed = discord.Embed(
            title="Restart Failed",
            description=f"An error occurred while restarting clients: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)

async def user_name_autocomplete(ctx: discord.AutocompleteContext):
    client_name = ctx.options.get('client')
    users = set()
    
    if client_name == 'all':
        for client_instance in clients:
            users.update([member.display_name for member in client_instance.party.members])
    else:
        for client_instance in clients:
            if client_instance.user.display_name == client_name:
                users.update([member.display_name for member in client_instance.party.members])
                break
    
    return list(users)

@discord_bot.slash_command(name="hide", description="Hide a user in the party")
async def hide(
    ctx: discord.ApplicationContext,
    client: Option(str, "The display name of the client", autocomplete=client_name_autocomplete, required=True),
    user: Option(str, "The user to hide", autocomplete=user_name_autocomplete, required=True)
):
    await hide_single_client(ctx, client, user)

async def hide_single_client(ctx: discord.ApplicationContext, client_name: str, user: str):
    try:
        client_instance = next(c for c in clients if c.user.display_name == client_name)
    except StopIteration:
        embed = discord.Embed(
            title="Error",
            description="Client not found",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
        return
    
    try:
        party_member = next(member for member in client_instance.party.members if member.display_name.lower() == user.lower())
        await party_member.hide()
        
        embed = discord.Embed(
            title="User Hidden",
            description=f"Successfully hid {party_member.display_name} in {client_instance.user.display_name}'s party.",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)
    except StopIteration:
        embed = discord.Embed(
            title="Error",
            description=f"Could not find user {user} in {client_instance.user.display_name}'s party.",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="Error",
            description=f"An error occurred: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)