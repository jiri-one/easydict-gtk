from pathlib import Path
import configparser

# internal imports
from utils import get_xdg_config_home

DEFAULT_SETTINGS = (
    {  # TODO: for any value we can add validator
        "win_size_remember": {"value": True, "type": bool},
        "win_height": {"value": 1200, "type": int},
        "win_width": {"value": 600, "type": int},
        "clipboard_scan": {"value": True, "type": bool},
        "search_language": {"value": "eng", "type": str},
    }
)

LANGUAGES_DATA = {
    "eng": {
        "id": 0,
        "label": "ENG",
        "name": "English",
        "native_name": "English",
        "flag_file": "flag_eng.svg",
    },
    "cze": {
        "id": 1,
        "label": "CZE",
        "name": "Czech",
        "native_name": "Česky",
        "flag_file": "flag_cze.svg",
    },
}

# set current working directory
cwd = Path(__file__).parent
# dictionary with images
images = dict()
for img_path in (cwd / "images").iterdir():
    images[img_path.name] = str(img_path.resolve())


cfg_dir = get_xdg_config_home()  # set user config directory
ini_file = cfg_dir / "easydict.ini"  # set user config file


class Settings:
    def __init__(self, ini_file: Path):
        config = configparser.ConfigParser()
        # check if ini_file exists and if not, create it
        if not ini_file.exists():
            config["EASYDICT"] = {
                key: value["value"] for key, value in DEFAULT_SETTINGS.items()
            }
            with open(ini_file, "w") as configfile:
                config.write(configfile)
        # read the ini file
        config.read(ini_file)
        try:
            ed_config = config["EASYDICT"]
        except KeyError:
            raise KeyError("""In easydict.ini file has to be ["EASYDICT"] section!""")
        # set all keys and values like this object attributes
        for key, value in ed_config.items():
            try:
                value_type = DEFAULT_SETTINGS[key]["type"]
            except KeyError as e:
                raise KeyError(
                    f"In easydict.ini file in section EASYDICT are allowed only known keys \n\n {e}"
                )
            if value_type == bool:
                # getboolean method is case insensitive and care about more variants
                value = ed_config.getboolean(key)
            elif value_type == int:
                value = int(value)
            setattr(self, key, value)
        # assert that all keys were read from file and are set
        try:
            for key in DEFAULT_SETTINGS:
                assert hasattr(self, key)
        except AssertionError as e:
            raise ValueError(f"Some keys from file were read broken: \n\n {e}")


ed_setup = Settings(ini_file)
