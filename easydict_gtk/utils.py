import difflib
import re
from os import environ
from pathlib import Path

# imports from my other files with classes and methods
# from settings import eng_cze, where


def db_search(language, text, fulltext):
    if fulltext == False:
        text = rf"\b{text}\b"
    results = eng_cze.search(where(language).search(text, flags=re.IGNORECASE))
    results_with_matchratio = []
    for result in results:
        ratio = difflib.SequenceMatcher(None, result[language], text).ratio()
        results_with_matchratio.append([result, ratio])
    sorted_results = sorted(results_with_matchratio, key=lambda x: x[1], reverse=True)
    return [r[0] for r in sorted_results]


def get_xdg_config_home() -> Path:
    xdg_config_home_str = environ.get("XDG_CONFIG_HOME")
    if xdg_config_home_str:
        xdg_config_home = Path(xdg_config_home_str)
    else:
        xdg_config_home = Path.home() / ".config"

    easydict_cfg_dir = xdg_config_home / "easydict"
    easydict_cfg_dir.mkdir(exist_ok=True)
    return easydict_cfg_dir
