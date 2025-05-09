"""Module for Fortnite client functionality."""
import rebootpy as fortnitepy
from rebootpy.ext import commands as fcommands
import asyncio
import json
from functools import partial

# Import from local modules
from .config import configuration, translations, translations_system, get_Language
from .utils import reshape_arabic_text

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
        owner_name = 'klld َََََ'
        if invite.sender.display_name in configuration.read()['Control']['FullAccess']:
            try:
                await invite.accept()
            except Exception as e:
                print(f"Error accepting invite from FullAccess user: {e}")
        elif invite.sender.display_name in owner_name:
          try:
            await invite.accept()
          except asyncio.TimeoutError:
            timeout_error = translations.read()["translations"]["command-error-timeouterror"][get_Language]
            await invite.sender.send(timeout_error)
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
          except Exception as e:
            print(f"Error handling party invite: {e}")
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
            member_join = translations.read()["translations"]["member-join"][get_Language]
            await member.party.send(member_join.format(member.display_name))
        else:
            pass

    # Add all the client commands here
    # This is just a stub - the actual commands would need to be added
    # based on what's in __init__.py

    return client

async def set_and_update_party_prop(client, schema_key: str, new_value: str):
    try:
        prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}
        await client.party.patch(updated=prop)
    except Exception as e:
        raise RuntimeError(f"Error setting party property: {e}")

async def shutdown_client(client):
    """Safely shutdown a Fortnite client.
    
    Args:
        client: The Fortnite client to shutdown
    """
    try:    
            # Close the client connection
            await client.close()
            #print(f"Client {client.user.display_name if client.user else 'Unknown'} has been safely shutdown.")
    except Exception as e:
        print(f"Error during client shutdown: {e}")
        # Try to force close if normal shutdown fails
        try:
            await client.close()
        except:
            pass