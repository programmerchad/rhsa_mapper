import click

from rhsa_mapper.cmds import v1


@click.group()
def rhsam():
    """Red Hat Mapper - Several useful utilities for retrieving CPE/Repository mappings for Red Hat."""
    pass


for sub_cmd in v1.all_cmds:
    rhsam.add_command(sub_cmd)
