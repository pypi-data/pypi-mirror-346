import click

from obs_dev.cmds.vault import vault
from obs_dev.cmds.plugin import plugin
@click.group()
def obs_dev():
    pass

obs_dev.add_command(vault)  
obs_dev.add_command(plugin)
if __name__ == "__main__":
    obs_dev()
