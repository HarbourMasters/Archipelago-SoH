import asyncio
import os
import json
import sys
from CommonClient import get_base_parser, handle_url_arg
from Utils import open_directory, open_filename
from . import SohWorld

# Stolen from SC2 client
# worlds/sc2/client.py
_has_forced_save = False
def force_settings_save_on_close() -> None:
    """
    Settings has an existing auto-save feature, but it only triggers if a new key was introduced.
    Force it to mark things as changed by introducing a new key and then cleaning up.
    """
    global _has_forced_save
    if _has_forced_save:
        return
    SohWorld.settings.update({'invalid_attribute': True})
    del SohWorld.settings.invalid_attribute
    _has_forced_save = True

def launch(*launch_args: str):
    async def main():
        hostname = None
        username = None
        password = None

        parser = get_base_parser(description="Ship of Harkinian Client")
        parser.add_argument('--name', default=None, help="Slot Name to connect as.")
        args, uri = parser.parse_known_args(launch_args)

        if uri and uri[0].startswith('archipelago://'):
            args.url = uri[0]
            handle_url_arg(args, parser)
            hostname = ':'.join([args.url.hostname, str(args.url.port)])
            username = args.name
            password = "" if args.password == "None" else args.password

        executable_path = SohWorld.settings.executable_path
        settings_folder = SohWorld.settings.soh_settings_folder

        # If there is no path to the Ship install. Prompt once and if they cancel close the client
        if not executable_path or not os.path.exists(executable_path):
            selected = open_filename("Select Ship of Harkinian AP Client", (("Ship of Harkinian AP Client", (".exe", ".appimage", ".elf")), ("Any File", "")), "")
            if not selected:
                return
            executable_path = os.path.abspath(selected)
            SohWorld.settings.executable_path = executable_path
            force_settings_save_on_close()

            # The settings folder is usually next to the executable
            candidate = os.path.dirname(executable_path)
            if os.path.exists(os.path.join(candidate, "shipofharkinian.json")):
                settings_folder = candidate
                SohWorld.settings.soh_settings_folder = settings_folder
                force_settings_save_on_close()

        # Similarly for the folder containing other ship related files, if it wasn't found above
        if not settings_folder or not os.path.exists(settings_folder):
            suggested_path = ""
            if sys.platform == "linux":
                suggested_path = os.path.realpath(os.path.join(os.environ["HOME"], ".local/share"))
            selected = open_directory("Select folder containing Ship of Harkinian settings, mods, etc", suggested_path)
            if not selected or not os.path.exists(os.path.join(selected, "shipofharkinian.json")):
                return
            settings_folder = os.path.realpath(selected)
            SohWorld.settings.soh_settings_folder = settings_folder
            force_settings_save_on_close()

        if executable_path is not None and settings_folder is not None:
            directory = settings_folder

            # Parse JSON to update credentials
            if hostname is not None:
                settings = dict()
                if os.path.isfile(os.path.join(directory, "shipofharkinian.json")):
                    with open(os.path.join(directory, "shipofharkinian.json"), "r", encoding="utf-8") as settings_file:
                        settings = json.load(settings_file)

                if "CVars" not in settings:
                    settings["CVars"] = {}

                if "gRemote" not in settings["CVars"]:
                    settings["CVars"]["gRemote"] = {}

                if "Archipelago" not in settings["CVars"]["gRemote"]:
                    settings["CVars"]["gRemote"]["Archipelago"] = {}

                settings["CVars"]["gRemote"]["Archipelago"]["ServerAddress"] = hostname
                settings["CVars"]["gRemote"]["Archipelago"]["SlotName"] = username
                settings["CVars"]["gRemote"]["Archipelago"]["Password"] = password

                with open(os.path.join(directory, "shipofharkinian.json"), "w", encoding="utf-8") as settings_file:
                    json.dump(settings, settings_file, indent=4)#, sort_keys=True)

            # Open Ship
            proc = await asyncio.create_subprocess_exec(
                executable_path,
                cwd=directory,
                stdout=None,
                stderr=None
            )

            # Wait for the process to finish and get output
            await proc.wait()

    asyncio.run(main())
