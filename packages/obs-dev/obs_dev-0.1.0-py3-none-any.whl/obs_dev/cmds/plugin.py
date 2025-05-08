import os
import shutil
import click
import zipfile
from obs_dev.consts import DATA_DIR
import obs_dev.utils as utils
import json
import obs_dev.utils.plugin as utils_plugin
import threading
import time

@click.group(name="plugin", help="Manage Obsidian plugins")
def plugin():
    """Manage Obsidian plugins"""
    pass

@plugin.command()
@click.option("--path", help="The path to the plugin")
@click.option("--name", help="The name of the plugin")
@click.option("--description", help="The description of the plugin")
@click.option("--author", help="The author of the plugin")
@click.option("--authorurl", help="The author url of the plugin")
@click.option("--isdesktoponly", help="The isDesktopOnly of the plugin", is_flag=True, default=False)
@click.option("-ns", "--no-sample-code", help="Do not create a sample code", is_flag=True, default=False)
def create(path, name, description, author, authorurl, isdesktoponly, no_sample_code):
    """Create a new plugin"""
    if os.path.exists(os.path.join(path, "manifest.json")) and os.path.exists(os.path.join(path, "package.json")):
        click.echo("Plugin already exists")
        return

    if not path:
        # Check for executables, .venv or .git
        has_executables = any(os.access(os.path.join(path, f), os.X_OK) for f in os.listdir(path))
        has_venv = os.path.exists(os.path.join(path, '.venv'))
        has_git = os.path.exists(os.path.join(path, '.git'))
        if has_executables or has_venv or has_git:
            click.echo("Warning: Path contains executables, .venv or .git directory")
            return

        path = os.getcwd()

    # unzip plugin-template.zip
    with zipfile.ZipFile(os.path.join(DATA_DIR, "plugin-template.zip"), "r") as zip_ref:
        zip_ref.extractall(path)

    from ..data.manifest_json import MANIFEST
    from ..data.package_json import PACKAGE_JSON

    manifest = MANIFEST.copy()
    package = PACKAGE_JSON.copy()
    if name:
        manifest["id"] = utils.serialize_name(name)
        package["name"] = name
        manifest["name"] = name
    if description:
        manifest["description"] = description
        package["description"] = description
    if author:
        manifest["author"] = author
    if authorurl:
        manifest["authorUrl"] = authorurl
    manifest["isDesktopOnly"] = bool(isdesktoponly)
    with open(os.path.join(path, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=4)

    with open(os.path.join(path, "package.json"), "w") as f:
        json.dump(package, f, indent=4)

    os.makedirs(os.path.join(path, "src"), exist_ok=True)

    if not no_sample_code:
        shutil.copy(os.path.join(DATA_DIR, "sample_code.ts"), os.path.join(path, "src", "main.ts"))

@plugin.command()
@click.option("--path", help="The path to the plugin")
def repair(path):
    """Repair the plugin configs by restoring missing files from the template"""

    if not path:
        path = os.getcwd()


    if not os.path.exists(os.path.join(path, "manifest.json")) or not os.path.exists(os.path.join(path, "package.json")):
        click.echo("Path folder lacks the basic structure of a plugin, aborting")
        return

    
    try:
        # Get the list of files in the template zip
        template_zip = os.path.join(DATA_DIR, "plugin-template.zip")
        if not os.path.exists(template_zip):
            click.echo("Template zip file not found")
            return

        with zipfile.ZipFile(template_zip, "r") as zip_ref:
            template_files = zip_ref.namelist()
            
            # Check each file in the template
            for file_path in template_files:
                target_path = os.path.join(DATA_DIR, file_path)
                
                # If file is missing or empty, restore it from template
                if not os.path.exists(target_path) or os.path.getsize(target_path) == 0:
                    click.echo(f"Restoring missing file: {file_path}")
                    # Create parent directories if they don't exist
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    # Extract the file
                    zip_ref.extract(file_path, path)
                    click.echo(f"Restored: {file_path}")

        click.echo("Plugin config repair completed")
    except Exception as e:
        click.echo(f"Error during repair: {e}")
        return

@plugin.command()
@click.option("--path", help="The path to the plugin")
@click.option("--no-ver-increment", help="Do not increment the version", is_flag=True, default=False)
@click.option("--ver-increment", help="The version increment", type=click.Choice(["major", "minor", "patch"]), default="patch")
def build(path, no_ver_increment, ver_increment):
    """Build the plugin"""

    if not path:
        path = os.getcwd()

    if not utils_plugin.check_is_plugin(path):
        click.echo("Not a valid plugin")
        return

    try:
        utils_plugin.assert_plugin_meta_ready(path)
    except Exception as e:
        click.echo(e)
        return

    curr_cwd = os.getcwd()
    os.chdir(path)

    os.system("npm install")

    if not no_ver_increment:
        utils_plugin.update_plugin_version(ver_increment)

    os.system("npm run build")

    os.chdir(curr_cwd)

@plugin.command()
@click.option("-p","--path", help="The path to the plugin")
@click.option("-v","--vault", help="The vault query string")
@click.option("--open", help="Open the vault after installation", is_flag=True, default=False)
def install(path, vault, open):
    """Install the plugin to the vault"""

    if not path:
        path = os.getcwd()

    if not os.path.exists(os.path.join(path, "main.js")):
        click.echo("Plugin lacks the main.js file, aborting")
        return

    if not vault:
        click.echo("Vault is required")

    try:
        query = utils.query_vault_2(vault)
        if not query:
            click.echo("Vault not found, you may need to register it first")
            return
        query = query.popitem()
        vault_id = query[0]
        vault_path = query[1]["path"]
        
    except Exception as e:
        click.echo(e)
        return

    if not vault_id:
        click.echo("Vault not found")
        return

    # copy the plugin
    # get plugin id
    plugin_id = utils_plugin.get_plugin_id(path)
    # delete the dest folder
    utils.kill_obsidian()
    dest_path = os.path.join(vault_path, ".obsidian", "plugins", plugin_id)
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.makedirs(os.path.join(vault_path, ".obsidian", "plugins", plugin_id), exist_ok=True)
    shutil.copy(os.path.join(path, "main.js"), os.path.join(vault_path, ".obsidian", "plugins", plugin_id, "main.js"))
    shutil.copy(os.path.join(path, "manifest.json"), os.path.join(vault_path, ".obsidian", "plugins", plugin_id, "manifest.json"))
    if os.path.exists(os.path.join(path, "styles.css")):
        shutil.copy(os.path.join(path, "styles.css"), os.path.join(vault_path, ".obsidian", "plugins", plugin_id, "styles.css"))

    if open:
        utils.open_vault(vault_id)

@plugin.command()
@click.option("--path", help="The path to the plugin")
@click.option("--no-build", help="Do not build the plugin", is_flag=True, default=False)
@click.option("--target", help="The target vault to test the plugin")
@click.pass_context
def test(ctx, path, no_build, target):
    """Test the plugin"""

    if not path:
        path = os.getcwd()

    if not os.path.exists(os.path.join(path, "manifest.json")) or not os.path.exists(os.path.join(path, "package.json")):
        click.echo("Path folder lacks the basic structure of a plugin, aborting")
        return

    if not no_build:
        ctx.invoke(build, path=path)

    ctx.invoke(install, path=path, vault=target, open=True)
    
@plugin.command()
@click.option("--path", help="The path to the plugin")
@click.option("--target", help="The target vault to test the plugin")
@click.option("--src-only", help="Only watch the src folder", is_flag=True, default=False)
@click.pass_context
def watch(ctx, path, target, src_only):
    """Watch the plugin for changes and automatically rebuild and test"""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        click.echo("watchdog is not installed, please install it with 'pip install watchdog'")
        return

    if not path:
        path = os.getcwd()

    if not os.path.exists(os.path.join(path, "manifest.json")) or not os.path.exists(os.path.join(path, "package.json")):
        click.echo("Path folder lacks the basic structure of a plugin, aborting")
        return

    ctx.invoke(test, path=path, target=target)

    class PluginHandler(FileSystemEventHandler):
        def __init__(self, ctx, path, target):
            self.ctx = ctx
            self.path = path
            self.target = target
            self.rebuild_immune_until = 0
            self.earliest_rebuild_time = 0
            self.change_detected = False
            self.last_file_changed = None

        def on_modified(self, event):
            if event.is_directory:
                return
            
            if any(x in event.src_path for x in ["node_modules", ".git", ".obsidian"]):
                return

            if src_only and not event.src_path.startswith(os.path.join(self.path, "src")):
                return
                
            current_time = time.time()
            
            # If we're in the immune period
            if current_time < self.rebuild_immune_until:
                return
            
            # Mark that a change was detected and extend the rebuild time
            self.change_detected = True
            self.last_file_changed = event.src_path
            # Set the earliest rebuild time to be the current time + debounce period
            debounce_seconds = 5
            self.earliest_rebuild_time = current_time + debounce_seconds
            click.echo(f"Change detected in {event.src_path}, rebuild scheduled in {debounce_seconds} seconds")

    event_handler = PluginHandler(ctx, path, target)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    click.echo(f"Watching {path} for changes...")
    try:
        while True:
            time.sleep(0.5)  # Check every half second
            current_time = time.time()
            
            # If a change was detected and we've reached or passed the earliest rebuild time
            if event_handler.change_detected and current_time >= event_handler.earliest_rebuild_time:
                event_handler.change_detected = False
                if event_handler.last_file_changed:
                    click.echo(f"Rebuilding after changes to {event_handler.last_file_changed}")
                    event_handler.last_file_changed = None
                
                # Rebuild the plugin
                click.echo("Rebuilding and testing plugin...")
                ctx.invoke(test, path=path, target=target)
                
                # Set immunity period
                event_handler.rebuild_immune_until = time.time() + 30  # 30 seconds immunity
    except KeyboardInterrupt:
        observer.stop()
        click.echo("\nStopped watching for changes")
    observer.join()
