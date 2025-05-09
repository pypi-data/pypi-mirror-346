"""Utility functions for klldFN"""
import asyncio
import subprocess
import sys
import os
import requests
import json
import signal
from typing import List, Optional

# Import from local modules
from .config import configuration, translations_system, get_Language
from .arprint import arprint

async def check_and_update_package():
    try:
        installed_version = subprocess.check_output([sys.executable, '-m', 'pip', 'show', 'klldFN']).decode('utf-8')
        installed_version = next(line for line in installed_version.split('\n') if line.startswith('Version:')).split(': ')[1].strip()
        latest_version = get_latest_version()

        # Only update if the installed version is lower than the latest version
        from packaging import version
        if version.parse(installed_version) < version.parse(latest_version):
            Updating_klldFN = translations_system.read()["translations"]["Updating-klldFN"][get_Language]
            print(Updating_klldFN.format(installed_version, latest_version))
            await update_package()
            print("Update successful! Restarting script...")
            await restart_script()
        else:
            pass
    except subprocess.CalledProcessError as e:
        print("Error occurred while checking package:", e)

def get_latest_version():
    url = "https://pypi.org/pypi/klldFN/json"
    response = requests.get(url)
    data = response.json()
    latest_version = data["info"]["version"]
    return latest_version

async def update_package():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'klldFN'])

async def restart_script():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def reshape_arabic_text(text):
    """Reshape Arabic text for proper display."""
    return arprint(text)

async def sanic_start():
    from . import Sanic
    port = configuration.read()['sanic web']['port']
    if "-p" in sys.argv:
        port_index = sys.argv.index("-p") + 1
        if port_index < len(sys.argv):
            port = int(sys.argv[port_index])
    
    # For Python 3.10 compatibility, we need to use a different approach
    # Create and await the server to avoid the coroutine warning
    server = await Sanic.create_server(
        host=configuration.read()['sanic web']['host'],
        port=port,
        return_asyncio_server=True,
        access_log=False,
        debug=False
    )
    
    return server

async def run_clients():
    from . import clients, klldFN_client
    from .client import shutdown_client
    
    with open('auths.json') as f:
        auths_data = json.load(f)

    for auth in auths_data['auths']:
        client = klldFN_client(auth['deviceId'], auth['accountId'], auth['secret'])
        if client:
            clients.append(client)    

    if not clients:
        config = configuration.read()
        
        # Show appropriate message based on which services are enabled
        if config['sanic web']['start']:
            host = config['sanic web']['host']
            port = config['sanic web']['port']
            print(f"Please create a bot through the site: http://{host}:{port}/createbot")
        elif config['discord']['start']:
            print("Please create a bot through the discord bot using the /createbot command")
        else:
            print("Please create a bot to continue")
        return

    try:
        # Register a cleanup handler for unexpected termination
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(
                    shutdown_all_clients("Signal received: {}".format(s.name))))
            except NotImplementedError:
                # Windows doesn't support add_signal_handler
                # We'll handle KeyboardInterrupt in the outer try/except instead
                pass

        # Start all clients
        await asyncio.gather(
            *[client.start() for client in clients],
            *[client.wait_until_ready() for client in clients]
        )

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Shutting down gracefully...")
        await shutdown_all_clients("Keyboard interrupt")
    except Exception as e:
        print(f"Error starting clients: {e}")
        pass

    finally:
        await shutdown_all_clients("Application closing")

async def shutdown_all_clients(reason="Unknown"):
    """Safely shutdown all Fortnite clients.
    
    Args:
        reason: The reason for shutting down
    """
    from . import clients
    from .client import shutdown_client
    
    #print(f"\nShutting down all clients. Reason: {reason}")
    
    if clients:
        shutdown_tasks = [shutdown_client(client) for client in clients]
        try:
            # Use wait_for to add a timeout
            await asyncio.wait_for(asyncio.gather(*shutdown_tasks), timeout=10)
        except asyncio.TimeoutError:
            #print("Shutdown timed out, some clients may not have closed properly.")
            # Fallback: directly call close() on each client
            for client in clients:
                try:
                    await client.close()
                except Exception as e:
                    print(f"Error closing client {client.user.display_name if hasattr(client, 'user') and client.user else 'Unknown'}: {e}")
        except KeyboardInterrupt:
            #print("Keyboard interrupt received during shutdown. Forcing immediate close.")
            # Force immediate close on keyboard interrupt during shutdown
            for client in clients:
                try:
                    await client.close()
                except Exception as e:
                    pass  # Suppress errors during forced shutdown
        except Exception as e:
            print(f"Error during shutdown: {e}")
            # Fallback: directly call close() on each client
            for client in clients:
                try:
                    await client.close()
                except Exception as e:
                    print(f"Error closing client {client.user.display_name if hasattr(client, 'user') and client.user else 'Unknown'}: {e}")
        finally:
            # Clear the clients list
            clients.clear()
            #print("All clients have been shut down.")
            
    # If this was triggered by a KeyboardInterrupt, we want to ensure the program exits cleanly
    if reason == "Keyboard interrupt":
        #print("Shutdown complete. Exiting...")
        pass
        # We don't call sys.exit() here as it would raise SystemExit and potentially disrupt the cleanup process

async def rotate_status():
    from . import clients
    import discord
    from .discord import discord_bot
    import random
    
    while True:
        try:
            statuses = [f"{len(clients)} bots Online!", f"klldFN Bot | {len(clients)} bots"]
            random_status = random.choice(statuses)
            game = discord.Activity(type=discord.ActivityType.playing, name=random_status)
            await discord_bot.change_presence(
                status=discord.Status.dnd, 
                activity=game
            )
        except Exception as e:
            # Silently handle any errors during status update
            pass
        await asyncio.sleep(30)


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