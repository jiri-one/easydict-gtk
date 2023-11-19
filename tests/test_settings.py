from pathlib import Path
# internal imports
from easydict_gtk.settings import Settings, DEFAULT_SETTINGS

def test_settings_init_with_non_existent_file(tmp_path):
    ini_file = tmp_path / "easydict.ini"  # set user config file
    settings = Settings(ini_file)
    assert ini_file.exists()

def test_settings_init_with_empty_file(tmp_path):
    ...

def test_settings_init_with_non_empty_text_file():
    ...

def test_setting_with_broken_file():
    ...

def test_settings_with_only_few_config_keys():
    ...

