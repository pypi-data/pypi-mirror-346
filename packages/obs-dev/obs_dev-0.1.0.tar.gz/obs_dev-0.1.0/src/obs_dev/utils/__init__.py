import secrets
import platform
import os
from time import sleep
import json
import time
import obs_dev.consts as consts
import subprocess
from itertools import chain
import urllib.parse 

def generate_id():
    """Generate a random 16-character hexadecimal ID.
    
    Returns:
        str: A random 16-character hexadecimal string.
    """
    hex_string = secrets.token_hex(8)
    return hex_string

REAL_PATH = None

def get_obsidian_path():
    """Get the path to the Obsidian executable.
    
    This function searches for the Obsidian executable in common installation paths
    and Windows shortcuts. It caches the result for subsequent calls.
    
    Returns:
        str: The absolute path to the Obsidian executable.
        
    Raises:
        NotImplementedError: If the platform is not Windows or macOS.
        FileNotFoundError: If the Obsidian executable cannot be found.
    """
    global REAL_PATH
    if REAL_PATH is not None:
        return REAL_PATH

    # method 1:
    if platform.system() == "Windows":
        # Try to find Obsidian in common installation paths
        possible_paths = [
            os.path.expandvars(r"%LOCALAPPDATA%\obsidian\Obsidian.exe"),
            os.path.expandvars(r"%PROGRAMFILES%\Obsidian\Obsidian.exe"),
            os.path.expandvars(r"%PROGRAMFILES(X86)%\Obsidian\Obsidian.exe")
        ]
        obsidian_path = None
        for path in possible_paths:
            if os.path.exists(path):
                obsidian_path = path
                break
                
    elif platform.system() == "Darwin":
        obsidian_path = "/Applications/Obsidian.app/Contents/MacOS/Obsidian"
    else:
        raise NotImplementedError("Unsupported platform")
    
    # method 2:
    # check via windows shortcuts
    if platform.system() == "Windows":
        shortcut_usr_dir=  r"C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs".format(os.getlogin())
        shortcut_programdata_dir = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
        for root, dirs, files in chain(os.walk(shortcut_usr_dir), os.walk(shortcut_programdata_dir)):
            for file in files:
                if file.lower() == "obsidian.lnk":
                    shortcut_path = os.path.join(root, file)
                    if os.path.exists(shortcut_path):
                        obsidian_path = os.path.realpath(shortcut_path)
                        break   
    
    if not obsidian_path:
        raise FileNotFoundError("Could not find Obsidian executable")
    if not os.path.exists(obsidian_path):
        raise FileNotFoundError("Could not find Obsidian executable")

    REAL_PATH = obsidian_path
    return obsidian_path



def kill_obsidian():
    """Forcefully terminate all running Obsidian processes.
    
    This function uses platform-specific commands to kill Obsidian processes
    and waits for 1 second after execution.
    """
    if platform.system() == "Windows":
        subprocess.run(["taskkill", "/f", "/im", "obsidian.exe"], 
                      stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL,
        )
    else:
        subprocess.run(["killall", "obsidian"],
                      stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL)
    sleep(consts.KILL_HOLD_INTERVAL)

def start_obsidian(detach: bool = True):
    """Start Obsidian application.
    
    Args:
        detach (bool, optional): Whether to start Obsidian in a detached process.
            Defaults to True.
    """
    if platform.system() == "Windows":
        if detach:  
            flags = (
                subprocess.DETACHED_PROCESS
                | subprocess.CREATE_NEW_PROCESS_GROUP
                | subprocess.CREATE_BREAKAWAY_FROM_JOB
            )
            obsidian_path = get_obsidian_path()
        else:
            flags = 0
            obsidian_path = "cmd /c start /b obsidian://"
            
        subprocess.Popen(
            obsidian_path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=flags,
            shell=True
        )
    else:
        subprocess.Popen(
            ["open", "obsidian://"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=detach
        )
    sleep(1)

_cached_data = None
_cached_last_modified = None

def get_obsidian_config():
    """Get the Obsidian configuration data from obsidian.json.
    
    This function implements caching to avoid reading the file multiple times
    if it hasn't been modified.
    
    Returns:
        dict: The Obsidian configuration data.
    """
    global _cached_data, _cached_last_modified
    config_path = os.path.join(consts.OBSIDIAN_APPDATA, "obsidian.json")
    
    if _cached_data is not None and _cached_last_modified is not None:
        if os.path.getmtime(config_path) == _cached_last_modified:
            return _cached_data

    with open(config_path, "r") as f:
        data = json.load(f)
        _cached_data = data
        _cached_last_modified = os.path.getmtime(config_path)

    return data

def save_obsidian_config(data):
    """Save the Obsidian configuration data to obsidian.json.
    
    Args:
        data (dict): The configuration data to save.
    """
    global _cached_data, _cached_last_modified
    config_path = os.path.join(consts.OBSIDIAN_APPDATA, "obsidian.json")
    
    with open(config_path, "w") as f:
        json.dump(data, f)
    
    _cached_data = data
    _cached_last_modified = os.path.getmtime(config_path)

def register_vault(vault_path: str, check_path_unique: bool = True, skip_if_exists: bool = False):
    """Register a new vault in Obsidian's configuration.
    
    Args:
        vault_path (str): The absolute path to the vault directory.
        
    Returns:
        str: The generated vault ID.
        
    Raises:
        AssertionError: If the vault path doesn't exist or is not a directory.
    """
    assert os.path.exists(vault_path), f"Vault path {vault_path} does not exist"
    assert os.path.isdir(vault_path), f"Vault path {vault_path} is not a directory"
    vault_path = os.path.abspath(vault_path)

    data = get_obsidian_config()

    if check_path_unique:
        for _, c_vault_data in data["vaults"].items():
            if c_vault_data["path"] == vault_path:
                if skip_if_exists:
                    return
                else:
                    raise ValueError("Vault already registered")

    data["vaults"][(vault_id := generate_id())] = {
        "path": vault_path,
        "ts": int(time.time() * 1000),
        "open": False,
    }
    save_obsidian_config(data)
    return vault_id

def _pre_check_idandpath(vault_id : str = None, vault_path : str = None):
    """Internal function to validate vault ID or path and load Obsidian configuration.
    
    Args:
        vault_id (str, optional): The vault ID to check.
        vault_path (str, optional): The vault path to check.
        
    Returns:
        dict: The Obsidian configuration data.
        
    Raises:
        ValueError: If neither or both vault_id and vault_path are provided.
        AssertionError: If vault_id is not 16 characters or vault_path doesn't exist.
    """
    if vault_id is None and vault_path is None:
        raise ValueError("Either vault_id or vault_path must be provided")

    if vault_id and vault_path:
        raise ValueError("Only one of vault_id or vault_path must be provided")

    if vault_id:
        assert len(vault_id) == 16, "Vault ID must be 16 characters long"

    if vault_path:
        assert os.path.exists(vault_path), f"Vault path {vault_path} does not exist"
        assert os.path.isdir(vault_path), f"Vault path {vault_path} is not a directory"
        vault_path = os.path.abspath(vault_path)

    return get_obsidian_config()

def unregister_vault(
    vault_id: str | None = None, vault_path: str | None = None, raise_error: bool = False
):
    """Remove a vault from Obsidian's configuration.
    
    Args:
        vault_id (str | None, optional): The ID of the vault to unregister.
        vault_path (str | None, optional): The path of the vault to unregister.
        raise_error (bool, optional): Whether to raise an error if vault not found.
            Defaults to False.
            
    Raises:
        ValueError: If vault not found and raise_error is True.
    """
    data = _pre_check_idandpath(vault_id, vault_path)

    done = False
    for c_vault_id, c_vault_data in data["vaults"].items():
        if vault_id and c_vault_id == vault_id:
            data["vaults"].pop(c_vault_id)
            done = True
            break
        if vault_path and c_vault_data["path"] == vault_path:
            data["vaults"].pop(c_vault_id)
            done = True
            break
    if not done:
        if raise_error:
            raise ValueError("Vault not found")
        else:
            return

    save_obsidian_config(data)

def toggle_open(vault_id : str = None, vault_path : str = None, toggle_to : bool = None):
    """Toggle the 'open' state of a vault in Obsidian's configuration.
    
    Args:
        vault_id (str, optional): The ID of the vault to toggle.
        vault_path (str, optional): The path of the vault to toggle.
        toggle_to (bool, optional): The specific state to set. If None, toggles current state.
    """
    data = _pre_check_idandpath(vault_id, vault_path)

    for c_vault_id, c_vault_data in data["vaults"].items():
        if vault_id and c_vault_id == vault_id:
            c_vault_data["open"] = toggle_to if toggle_to is not None else not c_vault_data["open"]
            break

    save_obsidian_config(data)

def toggle_alls(togglemap : dict):
    """Toggle the 'open' state of multiple vaults in Obsidian's configuration.
    
    Args:
        togglemap (dict): A dictionary mapping vault identifiers to their desired open states.
            Keys can be in the following formats:
            - 16-character vault ID (e.g., "1234567890abcdef")
            - Absolute vault path (e.g., "/path/to/vault")
            - Name with prefix (e.g., "name_vaultname")
            Values should be integers (0 for closed, 1 for open)
            
    Examples:
        >>> toggle_alls({
        ...     "1234567890abcdef": 1,  # Open vault by ID
        ...     "/path/to/vault": 0,    # Close vault by path
        ...     "name_myvault": 1       # Open vault by name
        ... })
    """
    data = get_obsidian_config()
    done = []
    for k, v in togglemap.items():
        done_len = len(done)
        ok = k
        if "_" not in k and len(k) == 16:
            ktype = "id"
        elif os.path.exists(k) and os.path.isdir(k):
            ktype = "path"
        else:
            ktype, k = k.split("_", 1)

        if ktype == "id":
            assert len(k) == 16, "Vault ID must be 16 characters long"
        elif ktype == "path":
            assert os.path.exists(k), f"Vault path {k} does not exist"
            assert os.path.isdir(k), f"Vault path {k} is not a directory"
            k = os.path.abspath(k)
        elif ktype == "name":
            for c_vault_id, c_vault_data in data["vaults"].items():
                if os.path.basename(c_vault_data["path"]) == k:
                    k = c_vault_id
                    break

        for c_vault_id, c_vault_data in data["vaults"].items():
            if c_vault_id in done:
                continue
            if c_vault_id == k:
                c_vault_data["open"] = v
                done.append(c_vault_id)
                break
            elif c_vault_data["path"] == k:
                c_vault_data["open"] = v
                done.append(c_vault_id)
                break
        
        if done_len == len(done):
            print(f"Vault {ok} not found")

    save_obsidian_config(data)

def open_vault(vault_id : str = None, vault_path : str = None, vault_name : str = None):
    """Open a vault in Obsidian.
    
    Args:
        vault_id (str, optional): The ID of the vault to open.
        vault_path (str, optional): The path of the vault to open.
        vault_name (str, optional): The name of the vault to open.
    """
    if vault_path:
        # If a path is provided, use the path-based URL format
        abs_path = os.path.abspath(vault_path)
        encoded_path = urllib.parse.quote(abs_path)
        url = f"obsidian://open?path={encoded_path}"
    else:
        # If only vault_id is provided, use the vault-based URL format
        target = vault_id
        encoded_target = urllib.parse.quote(target)
        url = f"obsidian://open?vault={encoded_target}"
    
    if platform.system() == "Windows":
        subprocess.Popen(
            ["cmd", "/c", "start", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL
        )
    else:
        subprocess.Popen(
            ["open", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL
        )

def serialize_name(name : str):
    """Serialize a name to a valid filename.
    
    Args:
        name (str): The name to serialize.
    """
    return name.replace(" ", "-").replace("_", "-").lower()

def query_vault(vault_id: str = None, vault_path: str = None, vault_name: str = None) -> dict:
    """Query vault data from Obsidian's configuration.
    
    Args:
        vault_id (str, optional): The ID of the vault to query.
        vault_path (str, optional): The path of the vault to query.
        vault_name (str, optional): The name of the vault to query.
        
    Returns:
        dict: A dictionary mapping vault IDs to their data. If specific vault is queried,
              returns a single-item dictionary with that vault's data.
              
    Examples:
        >>> query_vault_data()  # Get all vaults
        {'1234567890abcdef': {'path': '/path/to/vault', 'ts': 1234567890, 'open': True}}
        >>> query_vault_data(vault_name='myvault')  # Get specific vault
        {'1234567890abcdef': {'path': '/path/to/vault', 'ts': 1234567890, 'open': True}}
    """
    data = get_obsidian_config()
    vaults = data.get("vaults", {})
    
    if not vault_id and not vault_path and not vault_name:
        return vaults
        
    if vault_name:
        for vid, vdata in vaults.items():
            if os.path.basename(vdata["path"]) == vault_name:
                return {vid: vdata}
        return {}
        
    if vault_id:
        if vault_id in vaults:
            return {vault_id: vaults[vault_id]}
        return {}
        
    if vault_path:
        abs_path = os.path.abspath(vault_path)
        for vid, vdata in vaults.items():
            if vdata["path"] == abs_path:
                return {vid: vdata}
        return {}
        
    return {}

def query_vault_2(query_str: str) -> dict:
    """Query vault data using a flexible string format.
    
    Args:
        query_str (str): Query string can be:
            - 16-character vault ID
            - Existing vault path
            - "id_xxx" - Query by vault ID
            - "path_xxx" - Query by vault path
            - "name_xxx" - Query by vault name
            - "open" - Query all open vaults
            - "closed" - Query all closed vaults
            - "*" - Query all vaults
            
    Returns:
        dict: A dictionary mapping vault IDs to their data.
            Each vault data contains:
            - path: str - The absolute path to the vault
            - ts: int - Timestamp of last modification
            - open: bool (optional) - Whether the vault is open
    """
    data = get_obsidian_config()
    vaults = data.get("vaults", {})
    
    if not query_str or query_str == "*":
        return vaults
        
    if query_str in ["open", "closed"]:
        state = query_str == "open"
        return {vid: vdata for vid, vdata in vaults.items() 
                if vdata.get("open", False) == state}

    # First check if query_str itself is a valid ID or path
    if len(query_str) == 16:
        if query_str in vaults:
            return {query_str: vaults[query_str]}
        return {}
        
    if os.path.exists(query_str) and os.path.isdir(query_str):
        abs_path = os.path.abspath(query_str)
        for vid, vdata in vaults.items():
            if vdata["path"] == abs_path:
                return {vid: vdata}
        return {}
        
    # Check if query_str matches any vault name
    for vid, vdata in vaults.items():
        if os.path.basename(vdata["path"]) == query_str:
            return {vid: vdata}
            
    # If not found, try prefix-based query
    if "_" not in query_str:
        return {}
        
    query_type, query_value = query_str.split("_", 1)
    
    if query_type == "id":
        if len(query_value) != 16:
            return {}
        if query_value in vaults:
            return {query_value: vaults[query_value]}
        return {}
        
    if query_type == "path":
        if not os.path.exists(query_value) or not os.path.isdir(query_value):
            return {}
        abs_path = os.path.abspath(query_value)
        for vid, vdata in vaults.items():
            if vdata["path"] == abs_path:
                return {vid: vdata}
        return {}
        
    if query_type == "name":
        for vid, vdata in vaults.items():
            if os.path.basename(vdata["path"]) == query_value:
                return {vid: vdata}
        return {}
        
    return {}