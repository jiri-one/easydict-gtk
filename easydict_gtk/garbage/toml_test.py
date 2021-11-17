from pathlib import Path
cwd = Path(__file__).parent
def extract_version_from_toml():
	toml_path = cwd.parent.parent / 'pyproject.toml'
	result = None
	if toml_path.is_file():
		with open(str(toml_path), "r") as f:
			while result == None:
				string=f.readline()
				if 'version = ' in string:
					result = string.split('"')[1]
	return result
	

print(extract_version_from_toml())