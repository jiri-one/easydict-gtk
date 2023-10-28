from pathlib import Path
from os import environ
import configparser

# internal imports
from utils import get_xdg_config_home

DEFAULT_SETTINGS = {
    "win_size_remember": (True, bool),
    "window_size": ("1200x600", str),
    "clipboard_scan": (True, bool),
    "search_language": ("eng", str),
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
            config["EASYDICT"] = {key: value[0] for key, value in DEFAULT_SETTINGS}
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
                value_type = DEFAULT_SETTINGS[key][1]
            except KeyError as e:
                raise (
                    f"In easydict.ini file in section EASYDICT are allowed only known keys \n\n {e}"
                )
            except IndexError:
                raise f"There is some internal error: \n\n {e}"
            if (
                value_type == bool
            ):  # in the future we can use eval for more types or care them separately (like bool, list, ..) which is safer
                value = ed_config.getboolean(key)
            setattr(self, key, value)
        # assert that all keys were read from file and are set
        try:
            for key in DEFAULT_SETTINGS:
                assert hasattr(self, key)
        except AssertionError as e:
            raise ValueError(f"Some keys from file were read broken: \n\n {e}")

ed_setup = Settings(ini_file)
