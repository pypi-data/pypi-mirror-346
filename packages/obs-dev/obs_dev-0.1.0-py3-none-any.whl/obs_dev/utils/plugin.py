import os
import json
import typing

def check_is_plugin(path : str):
    if not os.path.exists(os.path.join(path, "manifest.json")):
        return False
    if not os.path.exists(os.path.join(path, "package.json")):
        return False
    if not os.path.exists(os.path.join(path, "src")):
        return False
    return True


def assert_plugin_meta_ready(path : str):
    assert os.path.exists(os.path.join(path, "manifest.json")), "manifest.json does not exist"
    assert os.path.exists(os.path.join(path, "package.json")), "package.json does not exist"
    assert os.path.exists(os.path.join(path, "src")), "src directory does not exist"
    
    with open(os.path.join(path, "manifest.json"), "r") as f:
        manifest = json.load(f)
        assert manifest["id"] != "{id}", "manifest.json [id] is not set"
        assert manifest["name"] != "{name}", "manifest.json [name] is not set"
        assert manifest["description"] != "{description}", "manifest.json [description] is not set"
        assert manifest["author"] != "{author}", "manifest.json [author] is not set"
        assert manifest["authorUrl"] != "{authorUrl}", "manifest.json [authorUrl] is not set"
        assert manifest["isDesktopOnly"] != "{isDesktopOnly}", "manifest.json [isDesktopOnly] is not set"


    with open(os.path.join(path, "package.json"), "r") as f:
        package = json.load(f)
        assert package["name"] != "{name}", "package.json [name] is not set"
        assert package["description"] != "{description}", "package.json [description] is not set"


def get_plugin_id(path : str):
    with open(os.path.join(path, "manifest.json"), "r") as f:
        manifest = json.load(f)
        return manifest["id"]


def get_plugin_version():
    with open("manifest.json", "r") as f:
        manifest = json.load(f)
        return manifest["version"]
    
def increment_version(increment_type : typing.Literal["major", "minor", "patch"] = "patch"):
    version = get_plugin_version()
    import packaging.version
    version = packaging.version.parse(version)
    major, minor, patch = version.release
    if increment_type == "major":
        version = packaging.version.Version(f"{major + 1}.0.0")
    elif increment_type == "minor":
        version = packaging.version.Version(f"{major}.{minor + 1}.0")
    elif increment_type == "patch":
        version = packaging.version.Version(f"{major}.{minor}.{patch + 1}")
    return str(version)

def update_plugin_version(increment_type : typing.Literal["major", "minor", "patch"] = "patch"):
    version = increment_version(increment_type)
    with open("manifest.json", "r") as f:
        manifest = json.load(f)
        manifest["version"] = version
    with open("package.json", "r") as f:
        package = json.load(f)
        package["version"] = version
    with open("manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)
    with open("package.json", "w") as f:
        json.dump(package, f, indent=4)
