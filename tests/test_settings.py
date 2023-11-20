from pathlib import Path
import configparser
import re

# test imports
import pytest

# internal imports
from easydict_gtk.settings import Settings, DEFAULT_SETTINGS


@pytest.fixture
def cfg_parser():
    def parser(ini_file: Path):
        config = configparser.ConfigParser()
        config.read(ini_file)
        return config

    return parser


@pytest.fixture
def cfg_checker(cfg_parser):
    """Helper fixture which check ini file with DEFAULT_SETTINGS dict"""

    def check_ini_file(ini_file: Path, settings: Settings):
        cfg = cfg_parser(ini_file)["EASYDICT"]
        for key, value_and_type in DEFAULT_SETTINGS.items():
            type_of_value = value_and_type["type"]
            default_value = value_and_type["value"]
            # get actual value from config file or get default value
            if type_of_value == bool:
                # getboolean method is case insensitive and care about more variants
                value = cfg.getboolean(key)
            elif type_of_value == int:
                value = cfg.getint(key)
            else:  # value is string
                value = cfg.get(key)
            assert getattr(settings, key) == value == default_value

    return check_ini_file


def test_settings_with_non_existent_file(tmp_path, cfg_checker):
    ini_file = tmp_path / "easydict.ini"  # set user config file
    settings = Settings(ini_file)
    assert ini_file.exists()
    cfg_checker(ini_file, settings)


def test_settings_with_empty_file(tmp_path):
    ini_file = tmp_path / "easydict.ini"  # set user config file
    ini_file.touch()
    assert ini_file.exists()
    with pytest.raises(
        KeyError, match=r"In easydict.ini file has to be \[EASYDICT\] section!"
    ):
        settings = Settings(ini_file)


def test_settings_with_empty_easydict_section(tmp_path, cfg_checker):
    ini_file = tmp_path / "easydict.ini"  # set user config file
    ini_file.write_text("[EASYDICT]")
    assert ini_file.exists()
    settings = Settings(ini_file)
    cfg_checker(ini_file, settings)


def test_settings_with_non_empty_text_file(tmp_path):
    ini_file = tmp_path / "easydict.ini"  # set user config file
    ini_file.write_text("[EASYDICT]\nasfasdfasdf")
    assert ini_file.exists()
    with pytest.raises(configparser.ParsingError):
        settings = Settings(ini_file)
    
    ini_file2 = tmp_path / "easydict2.ini"  # set user config file
    ini_file2.write_text("asfasdfasdfasdfasdf\n[EASYDICT]\nasfasdfasdf")
    assert ini_file2.exists()
    with pytest.raises(configparser.ParsingError):
        settings = Settings(ini_file2)
    
    ini_file3 = tmp_path / "easydict3.ini"  # set user config file
    ini_file3.write_text("asfasdfasdfasdfasdfasfasdfasdf")
    assert ini_file3.exists()
    with pytest.raises(configparser.ParsingError):
        settings = Settings(ini_file3)


def test_setting_with_bad_value_type(tmp_path):
    ini_file = tmp_path / "easydict.ini"  # set user config file
    ini_file.write_text("""
[EASYDICT]
win_size_remember = BAD_VALUE_BOOL
""")
    assert ini_file.exists()
    with pytest.raises(ValueError, match="Not a boolean: BAD_VALUE_BOOL"):
        settings = Settings(ini_file)

    ini_file2 = tmp_path / "easydict2.ini"  # set user config file
    ini_file2.write_text("""
[EASYDICT]
win_height = BAD_VALUE_INT
""")
    assert ini_file2.exists()
    with pytest.raises(ValueError, match=re.escape("invalid literal for int() with base 10: 'BAD_VALUE_INT'")):
        settings = Settings(ini_file2)   
    



def test_settings_with_only_few_config_keys():
    ...
