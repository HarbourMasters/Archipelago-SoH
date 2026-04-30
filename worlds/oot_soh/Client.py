import asyncio
import os
import json
from CommonClient import get_base_parser, handle_url_arg
from Utils import open_filename
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

        path = SohWorld.settings.soh_install_path

        # If there is no path to the Ship install, prompt them until there is one
        while path is None or path == "" or not os.path.exists(path):
            try:
                tempPath = os.path.realpath(open_filename("Select Ship of Harkinian AP Client", (("Ship of Harkinian AP Client", (".exe", ".appimage")), ('Any File', '')), ""))

                # Check this exists
                if os.path.exists(tempPath):
                    path = tempPath
                    SohWorld.settings.soh_install_path = path
                    force_settings_save_on_close()

            except Exception as e:
                # Log an error? Unlikely to happen unless they close the file dialog
                return

        if path is not None:
            directory, filename = os.path.split(path)

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
                path,
                cwd=directory,
                stdout=None,
                stderr=None
            )

            # Wait for the process to finish and get output
            await proc.wait()

    asyncio.run(main())
