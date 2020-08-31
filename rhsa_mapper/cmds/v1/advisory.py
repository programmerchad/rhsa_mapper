import json
from os import path
from click_option_group import optgroup, AllOptionGroup

import click

from rhsa_mapper.utils import generate_output, parse_xml, generate_advisory_dict


@click.group('advisory')
def advisory():
    """Commands to be used with advisory_search"""
    pass


@advisory.command('search')
@click.argument('advisory_id', type=str)
@click.argument('oval_xml', type=str)
@click.argument('oval_directory', type=str)
@click.option('--display-output/--hide-output', help='Display or hide output', type=bool, default=True)
@optgroup.group('Output configuration',
                help='The output directory and filename configuration', cls=AllOptionGroup)
@optgroup.option('-d', '--out_dir', help='Directory to store output', type=str)
@optgroup.option('-o', '--out_file', help='Filename for output', type=str)
@optgroup.option('--save/--no-save', help='Save output to file in directory', type=bool, default=False)
def search(advisory_id, oval_xml, oval_directory, display_output, out_dir, out_file, save):
    """Search for a specific advisory ID in the OVAL XML"""
    oval_file = path.join(path.expanduser(oval_directory), oval_xml)
    save_path = None
    if not path.isfile(oval_file):
        click.echo(f'No such OVAL File: {oval_file}')
        return
    if save:
        save_path = path.join(path.expanduser(out_dir), out_file)
    click.echo(f'Searching for {advisory_id} in {oval_file}...')
    # noinspection PyTypeChecker
    for output in generate_advisory_dict(parse_xml(oval_file, advisory_id)):
        if advisory_id in output:
            click.echo(f'{advisory_id} found in {oval_file}...')
        else:
            click.echo(f'{advisory_id} not found in {oval_file}...')
        if display_output:
            for advisory_id, details in output.items():
                click.echo(generate_output(advisory_id, details))
        if save:
            with click.open_file(save_path, 'w') as f:
                click.echo(message=json.dumps(output, indent=4), file=f)


@advisory.command('parse')
@click.argument('oval_xml', type=str)
@click.argument('oval_directory', type=str)
@click.option('--display-output/--hide-output', help='Display or hide output', type=bool, default=True)
@optgroup.group('Output configuration',
                help='The output directory and filename configuration', cls=AllOptionGroup)
@optgroup.option('-d', '--out_dir', help='Directory to store output', type=str)
@optgroup.option('-o', '--out_file', help='Filename for output', type=str)
@optgroup.option('--save/--no-save', help='Save output to file in directory', type=bool, default=False)
def parse(oval_xml, oval_directory, display_output, out_file, out_dir, save):
    """Parse entire OVAL XML file for CPEs/repository information"""
    oval_file = path.join(path.expanduser(oval_directory), oval_xml)
    save_path = None
    if not path.isfile(oval_file):
        click.echo(f'No such OVAL File: {oval_file}')
        return
    if save:
        save_path = path.join(path.expanduser(out_dir), out_file)
    output_dict = {}
    # noinspection PyTypeChecker
    with click.progressbar(list(parse_xml(oval_file)), label=f'Processing {oval_file}: ') as bar:
        output_list = []
        for output in generate_advisory_dict(bar):
            if display_output:
                for advisory_id, details in output.items():
                    output_list.append(generate_output(advisory_id, details))
            if save:
                output_dict.update(output)
        if display_output:
            click.echo('\n'.join(output_list))
    if output_dict:
        with click.open_file(save_path, 'w') as f:
            click.echo(message=json.dumps(output_dict, indent=4), file=f)
