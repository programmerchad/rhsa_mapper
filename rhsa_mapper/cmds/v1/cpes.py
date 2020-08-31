import json
from os import path

import click
from click_option_group import optgroup, AllOptionGroup

from rhsa_mapper.utils import group_by_cpe


@click.group('cpe')
def cpe():
    """Commands to be used with cpes"""
    pass


@cpe.command('list')
@click.option('--display-output/--hide-output', help='Display or hide output', type=bool, default=True)
@optgroup.group('Output configuration',
                help='The output directory and filename configuration', cls=AllOptionGroup)
@optgroup.option('-d', '--out_dir', help='Directory to store output', type=str)
@optgroup.option('-o', '--out_file', help='Filename for output', type=str)
@optgroup.option('--save/--no-save', help='Save output to file in directory', type=bool, default=False)
def cpe_list(display_output, out_dir, out_file, save):
    """Return a list of all available CPEs and the repository for each"""
    click.echo(f'Gathering list of CPEs...')
    cpe_list = group_by_cpe()
    click.echo(f'{len(cpe_list)} CPEs found...')
    if save:
        save_path = path.join(path.expanduser(out_dir), out_file)
        click.echo(f'Saving CPE list to {save_path}')
        with click.open_file(save_path, 'w') as f:
            click.echo(message=json.dumps(cpe_list, indent=4), file=f)
    if display_output:
        for _cpe in cpe_list:
            click.echo(f'  - {_cpe}')


@cpe.command('search')
@click.argument('cpe_list', nargs=-1)
@click.option('--display-output/--hide-output', help='Display or hide output', type=bool, default=True)
@optgroup.group('Output configuration',
                help='The output directory and filename configuration', cls=AllOptionGroup)
@optgroup.option('-d', '--out_dir', help='Directory to store output', type=str)
@optgroup.option('-o', '--out_file', help='Filename for output', type=str)
@optgroup.option('--save/--no-save', help='Save output to file in directory', type=bool, default=False)
def search(cpe_list, out_dir, out_file, save, display_output):
    """Return a list of repositories for a given list of CPEs"""
    # Create unique sorted list of repos
    cpe_list = sorted(set(cpe_list))
    if len(cpe_list) <= 3:
        cpe_list_str = " or ".join(cpe_list)
    else:
        cpe_list_str = ", ".join(cpe_list)
    click.echo(f'Gathering a list of repositories that contain {cpe_list_str}...')
    cpe_mapping = group_by_cpe()
    cpe_dict = {}
    for cpe in cpe_list:
        repo_list = cpe_mapping.get(cpe, [])
        if not repo_list:
            click.echo(f'No repositories found for {cpe}.')
        else:
            cpe_dict[cpe] = {'num_of_repos': len(repo_list), 'repo_list': sorted(repo_list)}
    if display_output:
        for cpe, details in cpe_dict.items():
            repo_count = details.get('num_of_repos') or 0
            msg = "repositories" if repo_count > 1 else "repository"
            click.echo(f'Found {repo_count} {msg} containing {cpe_list_str}...')
            for repo in details.get('repo_list', []):
                click.echo(f'  - {repo}')
    if save:
        save_path = path.join(path.expanduser(out_dir), out_file)
        click.echo(f'Saving CPE list to {save_path}')
        with click.open_file(save_path, 'w') as f:
            click.echo(message=json.dumps(cpe_dict, indent=4), file=f)
