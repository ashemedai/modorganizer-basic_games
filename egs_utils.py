# -*- encoding: utf-8 -*-

import json
import winreg
from pathlib import Path
from typing import Dict, List


def find_games() -> Dict[str, Path]:
    """
    Find the list of Epic Games Store games installed.

    Returns:
        A mapping from EGS catalog item IDs to install locations for available
        EGS games.
    """
    games: Dict[str, Path] = {}

    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, r"Software\Wow6432Node\Epic Games\EpicGamesLauncher"
        ) as key:
            egs_app_data_path, _ = winreg.QueryValueEx(key, "AppDataPath")
    except FileNotFoundError:
        return {}

    egs_manifests_dir = Path(egs_app_data_path).joinpath("Manifests")
    if egs_manifests_dir.exists:
        for manifest_file in egs_manifests_dir.glob("*.item"):
            with open(manifest_file, "r") as manifest_fp:
                manifest_file_data = json.load(manifest_fp)
                games[manifest_file_data["CatalogItemId"]] = manifest_file_data["InstallLocation"]

    return games


if __name__ == "__main__":
    games = find_games()
    for k, v in games.items():
        print("Found game with id {} at {}.".format(k, v))
