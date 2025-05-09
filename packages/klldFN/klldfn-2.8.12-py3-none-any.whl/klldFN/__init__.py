"""
Copyright (c) 2024 klld
This code is licensed under the MIT License.
"""
import subprocess
import os
import sys
#sys.path.append(os.path.abspath('./rebootpy'))
sys.path.append(r"./")

import sanic
from sanic import response
from sanic.request import Request
from jinja2 import Template
import aiohttp

import requests
import asyncio
import json

import rebootpy as fortnitepy
#import fortnitepy as fortnitepy
from rebootpy.ext import commands as fcommands
#from fortnitepy.ext import commands as fcommands

from typing import TYPE_CHECKING, Optional, Any, List
# Import Discord functionality from local module
from .discord import discord_bot
from .clients import clients
import FortniteAPIAsync
from functools import partial
import random
import random as py_random
from rich.progress import Progress, TextColumn, BarColumn, SpinnerColumn, TimeElapsedColumn
import arabic_reshaper
from bidi.algorithm import get_display
from random import choice as random_choice

#loop = asyncio.get_event_loop()
# Initialize Sanic with Python 3.10 compatibility
Sanic = sanic.Sanic(__name__, configure_logging=False)
fortnite_api = FortniteAPIAsync.APIClient()
owner = 'e375edab04964813a886ee974b66bd70'
owner_name = 'klld َََََ'

async def get_name(id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://fortnite-api.com/v2/cosmetics/br/search?id={id}&language={get_Language}"
        ) as r:
            response = await r.json()
            if 'data' in response:
                return response['data']['name']
            else:
                return None

class UpdateTranslations:
    async def __call__(self):
        urls = [
            "https://a--s-2342-djias4388--24ohi-udd--aou-hs3-24-flie.pages.dev/translations-system.json",
            "https://a--s-2342-djias4388--24ohi-udd--aou-hs3-24-flie.pages.dev/translations.json"
        ]
        results = []
        for url in urls:
            result = await self.update_translations(url)
            results.append(result)
        return results

    async def update_translations(self, url):
        """
        Update translations file if its content has changed.

        Args:
            url (str): The URL of the translations file.

        Returns:
            str: Message indicating whether the file was updated or not.
        """
        response = requests.get(url)

        if response.status_code == 200:
            new_content = response.content

            file_name = "translations/" + url.split('/')[-1]

            try:
                os.makedirs(os.path.dirname(file_name), exist_ok=True)
              
                with open(file_name, 'rb') as f:
                    existing_content = f.read()

                if new_content != existing_content:
                    with open(file_name, 'wb') as f:
                        f.write(new_content)
                    pass
                else:
                    pass
            except FileNotFoundError:
                with open(file_name, 'wb') as f:
                    f.write(new_content)
                pass
        else:
            return f"Failed to download file from '{url}'. Status code: {response.status_code}"

def load_auths_data(filename):
    with open(filename, 'r') as f:
        auths_data = json.load(f)
    return auths_data



# These functions have been moved to utils.py

progress = None
async def clients_sanic_Run():
    updater = UpdateTranslations()
    
    
    # Read the language from the configuration
    get_Language = configuration.read()["Control"]["Language"]
    
    # Load the configuration for starting the Sanic server
    config = configuration.read()['sanic web']['start']
    if config:
        await sanic_start()

    # Initialize the progress bar
    progress = Progress(
        TextColumn("[bold blue]{task.description}", justify="right"),
        BarColumn(bar_width=None),
        SpinnerColumn(spinner_name="clock", style="bright_yellow", speed=1.0),
        TimeElapsedColumn(),
    )        

    with progress:
        # Read translations based on the configured language
        klldFN_Starting = translations_system.read()["translations"]["klldFN-Starting"][get_Language]
        updating_package = translations_system.read()["translations"]["updating-package"][get_Language]
        updating_translations = translations_system.read()["translations"]["updating-translations"][get_Language]

        # Reshape text if the language is Arabic
        if get_Language == "ar":
            klldFN_Starting = reshape_arabic_text(klldFN_Starting)
            updating_package = reshape_arabic_text(updating_package)
            updating_translations = reshape_arabic_text(updating_translations)

        # Add tasks to the progress bar
        task1 = progress.add_task(f"[bold green]{klldFN_Starting}", total=3)
        await asyncio.sleep(2)
        progress.update(task1, advance=2, description=f"[bold green]{updating_package}")
        
        await check_and_update_package()
        await asyncio.sleep(1)
        progress.update(task1, advance=1, description=f"[bold green]{updating_translations}")
        await updater()
        await asyncio.sleep(1)

    await run_clients()

# Import configuration classes from config module
from .config import configuration, translations, translations_system, get_Language
from .utils import check_and_update_package, reshape_arabic_text, sanic_start, run_clients, rotate_status



def is_owner():
    async def predicate1(ctx):
        return ctx.author.id in owner
    return fcommands.check(predicate1)



def klldFN_client(device_id, account_id, secret):
    prefix = '!','?','/','',' ','+' 
    client = fcommands.Bot(
        command_prefix=prefix,
        platform=fortnitepy.Platform('MAC'),
        auth=fortnitepy.DeviceAuth(
            account_id=account_id,
            device_id=device_id,
            secret=secret
        ),
        status="🔥 {party_size} / 16 | klldFN.xyz 🔥"
    )

    @client.event  
    async def event_ready() -> None:

        await edit_and_keep_client_member()
        await add_list()
        client_ready = translations.read()["translations"]["Client-ready"][get_Language]
        if get_Language == "ar":
          client_ready = reshape_arabic_text(client_ready)
        print(client_ready.format(client.user.display_name))
      


    async def set_crowns():
        meta = client.party.me.meta
        data = (meta.get_prop('Default:AthenaCosmeticLoadout_j'))['AthenaCosmeticLoadout']
        try:
            data['cosmeticStats'][1]['statValue'] = 1942
        except KeyError:
            data['cosmeticStats'] = [{"statName": "TotalVictoryCrowns", "statValue": 999}, {"statName": "TotalRoyalRoyales", "statValue": 999}, {"statName": "HasCrown", "statValue": 0}]
            final = {'AthenaCosmeticLoadout': data}
            key = 'Default:AthenaCosmeticLoadout_j'
            prop = {key: meta.set_prop(key, final)}
            await client.party.me.patch(updated=prop)

    async def add_list() -> None:
        try:
            if 'e375edab04964813a886ee974b66bd70' in client.friends:
                await asyncio.sleep(0)
            else:
                await client.add_friend('e375edab04964813a886ee974b66bd70')
        except: pass


    async def edit_and_keep_client_member():
        try:
            await client.party.me.edit_and_keep(
                partial(client.party.me.set_outfit, asset=configuration.read()['cosmetics']['outfit']),
                partial(client.party.me.set_banner,
                        icon=configuration.read()['banner']['bannerName'],
                        color=configuration.read()['banner']['bannerColor'],
                        season_level=configuration.read()['banner']['level']),
                partial(client.party.me.set_backpack, asset=configuration.read()['cosmetics']['backpack']),
                partial(client.party.me.set_pickaxe, asset=configuration.read()['cosmetics']['pickaxe']),
            )
        except Exception as e:
            error_klldfn = translations.read()["translations"]["error-klldfn"][get_Language]
            print(error_klldfn, e)


    @client.event
    async def event_party_member_promote(old_leader: fortnitepy.PartyMember, new_leader: fortnitepy.PartyMember):
     if new_leader.id == client.user.id:
        try:
            if old_leader is not None:
                promote_thanks_old = translations.read()["translations"]["promote-thanks_old"][get_Language]
                await client.party.send(promote_thanks_old.format(old_leader.display_name))
            else:
                promote_thanks = translations.read()["translations"]["promote-thanks"][get_Language]
                await client.party.send(promote_thanks)
        finally:
            try:
                await client.party.me.set_emote("EID_TrueLove")
            except:
                pass

    @client.event 
    async def event_party_invite(invite: fortnitepy.ReceivedPartyInvitation) -> None:
        if invite.sender.display_name in configuration.read()['Control']['FullAccess']:
            await invite.accept()
        elif invite.sender.display_name in owner_name:
          try:
            await invite.accept()
          except fortnitepy.HTTPException:
            pass
          except AttributeError:
            pass
          except fortnitepy.PartyError:
            pass
          except fortnitepy.Forbidden:
            pass
          except fortnitepy.PartyIsFull: 
            pass
        else:
          try:
            await invite.decline()
            party_invite = translations.read()["translations"]["party-invite"][get_Language]
            await invite.sender.send(party_invite)
            await invite.sender.invite()
          except fortnitepy.HTTPException:
            pass
          except AttributeError:
            pass
          except fortnitepy.PartyError:
            pass
          except fortnitepy.Forbidden:
            pass
          except fortnitepy.PartyIsFull:
            pass
          except:
            pass

    @client.event 
    async def event_party_message(message: fortnitepy.FriendMessage) -> None:
        if not client.has_friend(message.author.id):
            try:
                await client.add_friend(message.author.id)
            except: pass

    @client.event 
    async def event_friend_add(friend: fortnitepy.Friend) -> None:
        try:
            await asyncio.sleep(0.3)
            friend_add = translations.read()["translations"]["friend-add"][get_Language]
            await friend.send(friend_add.replace(friend.display_name))
            await friend.invite()
        except: pass 

    @client.event 
    async def event_command_error(ctx: fortnitepy.ext.commands.Context, error):
        #if isinstance(error, fcommands.CommandNotFound):
            #notfound = translations.read()["translations"]["command-error-notfound"][get_Language]
            #await ctx.send(notfound)
        if isinstance(error, IndexError):
            pass
        elif isinstance(error, fortnitepy.HTTPException):
            pass
        elif isinstance(error, fcommands.CheckFailure):
            checfFailure = translations.read()["translations"]["command-error-checkfailure"][get_Language]
            await ctx.send(checfFailure)
        elif isinstance(error, TimeoutError):
            timeout = translations.read()["translations"]["command-error-timeouterror"][get_Language]
            await ctx.send(timeout)
        else:
            print(error)



    @client.event
    async def event_party_member_join(member: fortnitepy.PartyMember) -> None:
        if client.party.member_count > 1:
            await set_crowns()
            #await edit_and_keep_client_member()
            member_join = translations.read()["translations"]["member-join"][get_Language]
            await member.party.send(member_join.format(member.display_name))
        else:
            pass


    @client.command(
    name="skin",
    aliases=[
        'outfit',
        'Skin',
        'character'
      ]
    )
    async def skinx(ctx: fortnitepy.ext.commands.Context, *, content = None) -> None:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(language=get_Language,matchMethod="contains",name=content,backendType="AthenaCharacter")

            await client.party.me.set_outfit(asset=cosmetic.id)
            skin_set = translations.read()["translations"]["skin-set"][get_Language]
            await ctx.send(skin_set.format(cosmetic.name))

        except FortniteAPIAsync.exceptions.NotFound:
                pass 


    @client.command(aliases=['crowns','Crowns'])
    async def crown(ctx: fortnitepy.ext.commands.Context, amount: str) -> None:
        meta = client.party.me.meta
        data = (meta.get_prop('Default:AthenaCosmeticLoadout_j'))['AthenaCosmeticLoadout']
        try:
            data['cosmeticStats'][1]['statValue'] = int(amount)
        except KeyError:
          data['cosmeticStats'] = [{"statName": "TotalVictoryCrowns","statValue": int(amount)},{"statName": "TotalRoyalRoyales","statValue": int(amount)},{"statName": "HasCrown","statValue": int(amount)}]

        final = {'AthenaCosmeticLoadout': data}
        key = 'Default:AthenaCosmeticLoadout_j'
        prop = {key: meta.set_prop(key, final)}

        await client.party.me.patch(updated=prop)

        await asyncio.sleep(0.2)
        crown_set = translations.read()["translations"]["crown-set"][get_Language]
        await ctx.send(crown_set.format(int(amount)))
        await client.party.me.clear_emote()
        await client.party.me.set_emote_v2(asset="EID_Coronet")


    @client.command(
        name="emote",
        aliases=[
            'danse',
            'Emote',
            'dance'
        ]
    )
    async def emotex(ctx: fortnitepy.ext.commands.Context, *, content=None) -> None:
        if content is None:
            await ctx.send("Please provide an emote.")
        if content.lower() in ['sce', 'Sce', 'scenario', 'Scenario']:
            await client.party.me.set_emote(asset="EID_KpopDance03")
            emote_set_sce = translations.read()["translations"]["emote-set"][get_Language]
            await ctx.send(f'{emote_set_sce} Scenario.')
        
        elif content.upper().startswith('EID_'):
            await client.party.me.set_emote(asset=content)
            await ctx.send(f'EID Set to {content}')


        else:
            try:
                cosmetic = await fortnite_api.cosmetics.get_cosmetic(language=get_Language,matchMethod="contains",name=content,backendType="AthenaDance")
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset=cosmetic.id)
                emote_set = translations.read()["translations"]["emote-set"][get_Language]
                await ctx.send(emote_set.format(cosmetic.name))
            except FortniteAPIAsync.exceptions.NotFound:
                pass

    @client.command(
      name="backpack",
      aliases=[
        'sac',
        'Backpack' 
      ]
    )
    async def backpackx(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(language=get_Language,matchMethod="contains",name=content,backendType="AthenaBackpack")
            await client.party.me.set_backpack(asset=cosmetic.id)
            backpack_set = translations.read()["translations"]["backpack-set"][get_Language]
            await ctx.send(backpack_set.format(cosmetic.name))

        except FortniteAPIAsync.exceptions.NotFound:
            pass


    @client.command(
      name="tier",
      aliases=[
        'bp',
        'battlepass'
      ]
    )
    async def tierx(ctx: fortnitepy.ext.commands.Context, tier: int) -> None:
        if tier is None:
            await ctx.send('No tier was given. Try: !tier (tier number)') 
        else:
            await client.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier
        )

        await ctx.send(f'Battle Pass tier set to: {tier}')            



    @client.command(
      name="random",
      aliases=[
        'rdm',
        'Rdm',
        'Random'
      ]
    )
    async def randomx(ctx: fortnitepy.ext.commands.Context, cosmetic_type: str = 'skin') -> None:
        if cosmetic_type == 'skin':
            all_outfits = await fortnite_api.cosmetics.get_cosmetics(language=get_Language,backendType="AthenaCharacter")
            random_skin = py_random.choice(all_outfits)
            await client.party.me.set_outfit(asset=random_skin.id,variants=client.party.me.create_variants(profile_banner='ProfileBanner'))
            random_skin_set = translations.read()["translations"]["random-skin-set"][get_Language]
            await ctx.send(random_skin_set.format(random_skin.name)) #random_skin.name
        elif cosmetic_type == 'emote':
            all_emotes = await fortnite_api.cosmetics.get_cosmetics(language=get_Language,backendType="AthenaDance")
            random_emote = py_random.choice(all_emotes)
            await client.party.me.clear_emote()
            await client.party.me.set_emote(asset=random_emote.id)
            await client.party.me.set_emote_v2(asset=random_emote.id)
            random_emote_set = translations.read()["translations"]["random-emote-set"][get_Language]
            await ctx.send(random_emote_set.format(random_emote.name)) 


    @client.command(
      name="pickaxe",
      aliases=[
        'pioche',
        'Pickaxe'
      ]
    )
    async def pickaxex(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(language=get_Language,matchMethod="contains",name=content,backendType="AthenaPickaxe")
            await client.party.me.set_pickaxe(asset=cosmetic.id)
            pickaxe_set = translations.read()["translations"]["pickaxe-set"][get_Language]
            await ctx.send(pickaxe_set.format(cosmetic.name))

        except FortniteAPIAsync.exceptions.NotFound:
            pass    



    @client.command()
    async def purpleskull(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(asset='CID_030_Athena_Commando_M_Halloween',variants=client.party.me.create_variants(clothing_color=1))
        purpleskull = translations.read()["translations"]["purpleskull"][get_Language]
        await ctx.send(purpleskull)

    @client.command()
    async def pinkghoul(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=client.party.me.create_variants(material=3))
        pinkghoul = translations.read()["translations"]["pinkghoul"][get_Language]
        await ctx.send(pinkghoul)

    @client.command()
    async def aerial(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(asset='CID_017_Athena_Commando_M')
        aerial = translations.read()["translations"]["aerial"][get_Language]
        await ctx.send(aerial)

    @client.command()
    async def hologram(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG')
        hologram = translations.read()["translations"]["hologram"][get_Language]
        await ctx.send(hologram)    



    @client.command()
    async def point(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_IceKing')
        point = translations.read()["translations"]["point"][get_Language]
        await ctx.send(point)


    @client.command()
    async def stop(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.clear_emote()
        stop_emote = translations.read()["translations"]["stop-emote"][get_Language]
        await ctx.send(stop_emote)               




    @client.command(aliases=['Ready'])
    async def ready(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_ready(fortnitepy.ReadyState.READY)
        ready = translations.read()["translations"]["ready"][get_Language]
        await ctx.send(ready)

    @client.command(aliases=['sitin'],)
    async def unready(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
        unready = translations.read()["translations"]["unready"][get_Language]
        await ctx.send(unready)

    @client.command(
      name="level",
      aliases=[
        'niveau',
        'Level'
      ]
    )
    async def levelx(ctx: fortnitepy.ext.commands.Context, banner_level: int) -> None:
        await client.party.me.set_banner(season_level=banner_level)
        level = translations.read()["translations"]["level"][get_Language]
        await ctx.send(level.format(banner_level))



    
    @client.command(aliases=['ghost', 'Hide'])
    async def hide(ctx: fortnitepy.ext.commands.Context, *, user=None):
        if client.party.me.leader:
            if user != "all":
                try:
                    if user is None:
                        user = await client.fetch_profile(ctx.message.author.id)
                        member = client.party.get_member(user.id)
                    else:
                        user = await client.fetch_profile(user)
                        member = client.party.get_member(user.id)

                    raw_squad_assignments = client.party.meta.get_prop('Default:RawSquadAssignments_j')["RawSquadAssignments"]

                    for m in raw_squad_assignments:
                        if m['memberId'] == member.id:
                            raw_squad_assignments.remove(m)

                    await set_and_update_party_prop(client, 'Default:RawSquadAssignments_j', {'RawSquadAssignments': raw_squad_assignments})
                    await ctx.send(f"Hid {member.display_name}")
                except AttributeError:
                    await ctx.send("I could not find that user.")
                except fortnitepy.HTTPException:
                    await ctx.send("I am not party leader!")
            else:
                try:
                    raw_squad_assignments = {
                        'RawSquadAssignments': [
                            {
                                'memberId': client.user.id,
                                'absoluteMemberIdx': 1
                            }
                        ]
                    }
    
                    await set_and_update_party_prop(client, 'Default:RawSquadAssignments_j', raw_squad_assignments)
                    await ctx.send("Hid everyone in the party")
                except Exception as e:
                    await ctx.send(f"An error occurred: {e}")
        else:
            await ctx.send("I am not party leader!")









    @client.command()
    async def say(ctx: fortnitepy.ext.commands.Context, *, message = None):
        if message is not None:
            await client.party.send(message)
            say = translations.read()["translations"]["say"][get_Language]
            await ctx.send(say.format(message))  #message
        else:
            say_no = translations.read()["translations"]["say-no"][get_Language]
            await ctx.send(say_no)


    return client

async def set_and_update_party_prop(client, schema_key: str, new_value: str):
    try:
        prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}
        await client.party.patch(updated=prop)
    except Exception as e:
        raise RuntimeError(f"Error setting party property: {e}")

class EpicUser:
    def __init__(self, data: dict = {}):
        self.raw = data

        self.access_token = data.get("access_token", "")
        self.expires_in = data.get("expires_in", 0)
        self.expires_at = data.get("expires_at", "")
        self.token_type = data.get("token_type", "")
        self.refresh_token = data.get("refresh_token", "")
        self.refresh_expires = data.get("refresh_expires", "")
        self.refresh_expires_at = data.get("refresh_expires_at", "")
        self.account_id = data.get("account_id", "")
        self.client_id = data.get("client_id", "")
        self.internal_client = data.get("internal_client", False)
        self.client_service = data.get("client_service", "")
        self.display_name = data.get("displayName", "")
        self.app = data.get("app", "")
        self.in_app_id = data.get("in_app_id", "")

    async def get_displayName(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method="GET",
                url="https://account-public-service-prod03.ol.epicgames.com/"
                f"account/api/public/account/displayName/{self.display_name}",
                headers={"Authorization": f"bearer {self.access_token}"},
            ) as request:
                data = await request.json()

        return data["displayName"]
SWITCH_TOKEN = "OThmN2U0MmMyZTNhNGY4NmE3NGViNDNmYmI0MWVkMzk6MGEyNDQ5YTItMDAxYS00NTFlLWFmZWMtM2U4MTI5MDFjNGQ3"
IOS_TOKEN = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
class epicgames:
    """To Interact with Epicgames API's For User Info!"""

    async def get_access_token() -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url="https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {SWITCH_TOKEN}",
                },
                data={
                    "grant_type": "client_credentials",
                },
            ) as response:
                data = await response.json()
        return data["access_token"]

    async def create_device_code() -> tuple:
        access_token = await epicgames.get_access_token()
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/deviceAuthorization",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            ) as response:
                data = await response.json()

        return data["verification_uri_complete"], data["device_code"]

    async def wait_for_device_code_completion(code: str, timeout: int = 90) -> EpicUser:
        #os.system('cls' if sys.platform.startswith('win') else 'clear')
        
        async def fetch_token():
            while True:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
                        headers={
                        "Authorization": f"basic {SWITCH_TOKEN}",
                        "Content-Type": "application/x-www-form-urlencoded",
                        },
                        data={"grant_type": "device_code", "device_code": code},
                    ) as request:
                        token = await request.json()

                    if request.status == 200:
                        return token
                    else:
                        if (
                            token["errorCode"]
                            == "errors.com.epicgames.account.oauth.authorization_pending"
                        ):
                            pass
                        elif token["errorCode"] == "errors.com.epicgames.not_found":
                            pass
                        elif token["errorCode"] == "errors.com.epicgames.common.slow_down":
                            # Handle the rate limit error silently
                            pass
                        else:
                            print(json.dumps(token, sort_keys=False, indent=4))

                    await asyncio.sleep(5)
        

        try:
            token = await asyncio.wait_for(fetch_token(), timeout=timeout)
        except asyncio.TimeoutError:
            raise asyncio.TimeoutError("Canceled Login")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/exchange",
                headers={"Authorization": f"bearer {token['access_token']}"},
            ) as request:
                exchange = await request.json()

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
                headers={
                    "Authorization": f"basic {IOS_TOKEN}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={"grant_type": "exchange_code", "exchange_code": exchange["code"]},
            ) as request:
                auth_information = await request.json()

                return EpicUser(data=auth_information)

@Sanic.route('/api/start_device_auth', methods=['POST'])
async def start_device_auth(request):
    try:
        device_code = await epicgames.create_device_code()

        return sanic.response.json({"device_code": device_code[0], "user_code": device_code[1]})
    except Exception as e:
        return sanic.response.json({"error": "Device authentication failed"}, status=500)

def read_auths():
    with open('auths.json', 'r') as file:
        return json.load(file)

def write_auths(data):
    with open('auths.json', 'w') as file:
        json.dump(data, file, indent=4)

async def run_createbot(new_auth_entry):
    
    if isinstance(new_auth_entry, dict):
        new_auth_entry = [new_auth_entry]

    for auth in new_auth_entry:
        client = klldFN_client(auth['deviceId'], auth['accountId'], auth['secret'])
        if client:
            clients.append(client)    

    try:
        await asyncio.gather(
            *[client.start() for client in clients],
            *[client.wait_until_ready() for client in clients]
        )

    except Exception as e:
        print(e)
        pass

    finally:
        for client in clients:
            await client.close()

@Sanic.route('/api/device_auth/check')
async def check_device_auth(request):
    user_code = request.args.get('code')
    try:
        user1 = await epicgames.wait_for_device_code_completion(user_code)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{user1.account_id}/deviceAuth",
                headers={
                    "Authorization": f"bearer {user1.access_token}",
                    "Content-Type": "application/json",
                },
            ) as response:
                data = await response.json()
        
        # Read the existing auths from the JSON file
        auth_data = read_auths()

        # Create a new auth entry
        new_auth_entry = {
            "deviceId": data['deviceId'],
            "accountId": data['accountId'],
            "secret": data['secret']
        }
        auth_data['auths'].append(new_auth_entry)

        # Write the updated auths back to the JSON file
        write_auths(auth_data)


        asyncio.create_task(run_createbot(new_auth_entry))
           
        response_obj = sanic.response.json({"authenticated": True})
        return response_obj
        #return sanic.response.json({"authenticated": True, "uuid": sessionid})
    except asyncio.TimeoutError:
        return sanic.response.json({"authenticated": False, "error": "Timeout"})
    except Exception as e:
        return sanic.response.json({"authenticated": False, "error": str(e)})


@Sanic.route('/createbot', methods=['GET'])
async def createbot_route(request):
    template_content = await template_web("https://klldfn-dashboard-v2-v3-beta.pages.dev/create-bot.html")
        
    template = Template(template_content)
    rendered_template = template.render()

    return response.html(rendered_template)

async def template_web(URL):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            return await response.text()

@Sanic.route('/<bot>/dashboard', methods=['GET'])
async def root(request, bot: str):
    try:
        client = next(c for c in clients if c.user.display_name == bot)
    except StopIteration:
        return sanic.response.html("Client not found")

    outfit_name = await get_name(client.party.me.outfit)
    backpack_name = await get_name(client.party.me.backpack)
    pickaxe_name = await get_name(client.party.me.pickaxe)
    display_name = client.user.display_name
    total_friends = len(client.friends)
    platform = str(client.platform)[9:].lower().capitalize()
    party_size = client.party.member_count


    template = Template(await template_web("https://klldfn-dashboard-v2-v3-beta.pages.dev/dashboard.html"))
    html_content = template.render(
        client=client,
        display_name=display_name,
        total_friends=total_friends,
        platform=platform,
        party_size=party_size,
        outfit_name=outfit_name,
        backpack_name=backpack_name,
        pickaxe_name=pickaxe_name
    )

    return sanic.response.html(html_content)


@Sanic.route('/', methods=['GET', 'POST'])
async def client_info(request):
    template = Template(await template_web("https://klldfn-dashboard-v2-v3-beta.pages.dev/dashboard-clients.html"))
    if request.method == 'GET':
        client_info = []

        for client in clients:
            display_name = "Unknown"
            outfit = "Unknown"
            friends_count = "Unknown"

            try:
                if hasattr(client, 'user') and client.user is not None:
                    display_name = client.user.display_name or "Unknown"
                elif hasattr(client, 'display_name'):
                    display_name = client.display_name or "Unknown"
            except Exception as e:
                print(f"Error retrieving display_name: {e}")
            try:
                if hasattr(client, 'party') and client.party is not None and hasattr(client.party, 'me'):
                    outfit = client.party.me.outfit or "Unknown"
            except Exception as e:
                print(f"Error retrieving outfit: {e}")

            try:
                if hasattr(client, 'friends') and client.friends is not None:
                    friends_count = len(client.friends)
            except Exception as e:
                print(f"Error retrieving friends count: {e}")

            client_info.append({
                'display_name': display_name,
                'outfit': outfit,
                'friends_count': friends_count,
            })

        return sanic.response.html(template.render(clients=client_info))


@Sanic.route('/<bot>/cosmetics', methods=['GET'])
async def cosmetics_route(request: Request, bot: str):
    try:
        client = [c for c in clients if c.user.display_name == bot][0]
    except IndexError:
        return response.html("Client not found")

    if client:
        if request.method == 'GET':
            template_content = await template_web("https://klldfn-dashboard-v2-v3-beta.pages.dev/cosmetics.html")
            template = Template(template_content)
            rendered_template = template.render()  # Render the template as a string
            return response.html(rendered_template)  # Return the rendered HTML as the response


@Sanic.route('/<bot>/cosmetics/skin', methods=['GET', 'POST'])
async def skin_route(request, bot: str):
        template = Template(await template_web("https://klldfn-dashboard-v2-v3-beta.pages.dev/cosmetics-skin.html"))
        try:
          client = [c for c in clients if c.user.display_name == bot][0]
        except IndexError:
          return sanic.response.html("Client not found")
        if client:
          if request.method == 'GET':
            display_name_get = client.user.display_name
            return sanic.response.html(template.render(client_name=bot, message=None, error=None, icon_url=None, display_name=display_name_get))
          elif request.method == 'POST':
            content = request.form.get('content')
            try:
                display_name_post = client.user.display_name
                cosmetic = await fortnite_api.cosmetics.get_cosmetic(language=get_Language, matchMethod="contains", name=content, backendType="AthenaCharacter")
                await client.party.me.set_outfit(asset=cosmetic.id)
                skin_set = translations.read()["translations"]["skin-set"][get_Language]
                return sanic.response.html(template.render(client_name=bot, message=skin_set.format(cosmetic.name), error=None, icon_url=f"https://fortnite-api.com/images/cosmetics/br/{cosmetic.id}/icon.png", display_name=display_name_post))      
            except FortniteAPIAsync.exceptions.NotFound:
                return sanic.response.html(template.render(client_name=bot, message=None, error="Cosmetic not found", icon_url=None, display_name=display_name_post))
        else: 
          return sanic.response.html("Client not found")


@Sanic.route('/<bot>/cosmetics/emote', methods=['GET', 'POST'])
async def emote_route(request, bot: str):
        template_emote = Template(await template_web("https://klldfn-dashboard-v2-v3-beta.pages.dev/cosmetics-emote.html"))
        client_name = request.args.get('name')
        try:
            client = [c for c in clients if c.user.display_name == bot][0]
        except IndexError:
            return sanic.response.html("Client not found")
        if client:
          if request.method == 'GET':
            display_name_get = client.user.display_name
            return sanic.response.html(template_emote.render(client_name=bot, message=None, error=None, icon_url=None, display_name=display_name_get))
          elif request.method == 'POST':
            content = request.form.get('content')
            try:
                cosmetic = await fortnite_api.cosmetics.get_cosmetic(language=get_Language, matchMethod="contains", name=content, backendType="AthenaDance")
                await client.party.me.set_emote(asset=cosmetic.id)
                emote_set = translations.read()["translations"]["emote-set"][get_Language]
                display_name_post = client.user.display_name
                return sanic.response.html(template_emote.render(client_name=bot, message=emote_set.format(cosmetic.name), error=None, icon_url=f"https://fortnite-api.com/images/cosmetics/br/{cosmetic.id}/icon.png", display_name=display_name_post))      
            except FortniteAPIAsync.exceptions.NotFound:
                return sanic.response.html(template_emote.render(client_name=bot, message=None, error="Cosmetic not found", icon_url=None))
        else:
          return sanic.response.html("Client not found")


# This function has been moved to utils.py

# Discord bot functionality is now imported from discord.py





# Run the clients
if configuration.read()["discord"]["start"]:
    discord_bot.run(configuration.read()["discord"]["token"])
else:
    try:
        asyncio.run(clients_sanic_Run())
    except KeyboardInterrupt:
        #print("\nKeyboard interrupt detected. Shutting down...")
        pass
        # The shutdown_all_clients will be called in the run_clients function
    except Exception as e:
        print(f"\nError in main loop: {e}")
        # Ensure we exit with a non-zero code on error
        sys.exit(1)