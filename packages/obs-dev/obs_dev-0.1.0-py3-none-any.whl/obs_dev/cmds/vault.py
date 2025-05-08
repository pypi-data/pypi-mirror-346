import os
import click
import obs_dev.utils as utils
import obs_dev.consts as consts

@click.group(name="vault", help="Manage Obsidian vaults")
def vault():
    """Manage Obsidian vaults"""
    pass


@vault.command()
@click.argument("path", type=click.Path(dir_okay=True, file_okay=False))
@click.option("-o", "--open", is_flag=True, help="Open the vault after creation")
def create(path, open):
    if not os.path.exists(os.path.join(path, ".obsidian")):
        click.echo("Creating vault...")
        os.makedirs(os.path.join(path, ".obsidian"), exist_ok=True)
        import zipfile
        with zipfile.ZipFile(os.path.join(consts.DATA_DIR, "vault.zip"), "r") as zip_ref:
            zip_ref.extractall(os.path.join(path, ".obsidian"))
    else:
        click.echo("Vault already exists")

    if open:
        utils.kill_obsidian()
        utils.register_vault(path, skip_if_exists=True)
        utils.open_vault(vault_path=path)

@vault.command()
@click.option("--id", help="The ID of the vault to open")
@click.option("--path", help="The path of the vault to open")
@click.option("--name", help="The name of the vault to open")
def open(id, path, name):
    try:
        if not id and not path and not name:
            utils.start_obsidian()
            return

        if name:
            data = utils.get_obsidian_config()
            for vault_id, vault_data in data["vaults"].items():
                if os.path.basename(vault_data["path"]) == name:
                    id = vault_id
                    break
            
        utils.open_vault(id, path)
    except Exception as e:
        click.echo(e)
        return
    

@vault.command()
@click.option("--id", help="The ID of the vault to toggle")
@click.option("--path", help="The path of the vault to toggle")
@click.option("--name", help="The name of the vault to toggle")
@click.option("--state", type=click.Choice(["open", "closed"]), help="Force a specific state")
def toggle(id, path, name, state):
    """Toggle the open state of a vault"""
    try:
        if not id and not path and not name:
            click.echo("Please provide either --id, --path, or --name")
            return

        if name:
            data = utils.get_obsidian_config()
            for vault_id, vault_data in data["vaults"].items():
                if os.path.basename(vault_data["path"]) == name:
                    id = vault_id
                    break
            if not id:
                click.echo(f"No vault found with name: {name}")
                return

        toggle_to = None
        if state == "open":
            toggle_to = True
        elif state == "closed":
            toggle_to = False

        utils.toggle_open(id, path, toggle_to)
        click.echo("Vault state toggled successfully")
    except Exception as e:
        click.echo(f"Error: {e}")
        return


@vault.command()
@click.option("--off-all", is_flag=True, help="do not open any vaults")
@click.option("-t", "--toggle", help="Use id(xxx)=1, name(xxx)=0 or path(xxx)=0 to toggle the state of the vaults", multiple=True)
def btoggle(toggle, off_all):
    """Batch toggle the open state of multiple vaults"""
    try:
        # Parse the toggle options
        toggle_map = {}
        if off_all:
            assert not toggle, "Cannot provide both --off-all and --toggle"
            toggle_map = {k:0 for k in utils.get_obsidian_config().get("vaults").keys()}
        for item in toggle:
            key, value = item.split("=")
            toggle_map[key] = int(value)
        utils.toggle_alls(toggle_map)
        click.echo("Vault states toggled successfully")
    except Exception as e:
        click.echo(f"Error: {e}")
        return


@vault.command()
@click.option("--id", help="The ID of the vault to unregister")
@click.option("--path", help="The path of the vault to unregister")
@click.option("--name", help="The name of the vault to unregister")
def unregister(id, path, name):
    """Unregister a vault"""
    utils.unregister_vault(id, path, name)


@vault.command()
def list():
    for vault_id, vault_data in utils.get_obsidian_config().get("vaults").items():
        print(f"{vault_id} : {os.path.basename(vault_data.get('path'))}")


