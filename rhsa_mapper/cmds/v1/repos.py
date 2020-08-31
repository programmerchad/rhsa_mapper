import json
from os import path

import click
from click_option_group import optgroup, AllOptionGroup

from rhsa_mapper.utils import group_by_repository


@click.group('repo')
def repo():
    """Commands to be used with repos"""
    pass


@repo.command('list')
@click.option('--display-output/--hide-output', help='Display or hide output', type=bool, default=True)
@optgroup.group('Output configuration',
                help='The output directory and filename configuration', cls=AllOptionGroup)
@optgroup.option('-d', '--out_dir', help='Directory to store output', type=str)
@optgroup.option('-o', '--out_file', help='Filename for output', type=str)
@optgroup.option('--save/--no-save', help='Save output to file in directory', type=bool, default=False)
def repo_list(display_output, out_dir, out_file, save):
    """Return a list of all available repositories and the CPEs for each"""
    click.echo(f'Gathering list of repositories...')
    repo_list = group_by_repository()
    click.echo(f'{len(repo_list)} repositories found...')
    if save:
        save_path = path.join(path.expanduser(out_dir), out_file)
        click.echo(f'Saving repository list to {save_path}')
        with click.open_file(save_path, 'w') as f:
            click.echo(message=json.dumps(repo_list, indent=4), file=f)
    if display_output:
        for _repo in repo_list:
            click.echo(f'  - {_repo}')


@repo.command('search')
@click.argument('repo_list', nargs=-1)
@click.option('--display-output/--hide-output', help='Display or hide output', type=bool, default=True)
@optgroup.group('Output configuration',
                help='The output directory and filename configuration', cls=AllOptionGroup)
@optgroup.option('-d', '--out_dir', help='Directory to store output', type=str)
@optgroup.option('-o', '--out_file', help='Filename for output', type=str)
@optgroup.option('--save/--no-save', help='Save output to file in directory', type=bool, default=False)
def search(repo_list, out_dir, out_file, save, display_output):
    """Return a list of CPEs for a given list of repositories"""
    # Create unique sorted list of repos
    repo_list = sorted(set(repo_list))
    if len(repo_list) <= 3:
        repository_list_str = " or ".join(repo_list)
    else:
        repository_list_str = ", ".join(repo_list)
    click.echo(f'Gathering a list of CPEs found in {repository_list_str}...')
    repository_mapping = group_by_repository()
    repo_dict = {}
    for repo in repo_list:
        cpe_list = repository_mapping.get(repo, [])
        if not cpe_list:
            click.echo(f'No CPEs found in for {repo}.')
        else:
            repo_dict[repo] = {'num_of_cpes': len(cpe_list), 'cpe_list': sorted(cpe_list)}
    if display_output:
        for repository, details in repo_dict.items():
            cpe_count = details.get('num_of_cpes') or 0
            msg = "CPEs" if cpe_count > 1 else "CPE"
            click.echo(f'Found {cpe_count} {msg} in {repository}...')
            for cpe in details.get('cpe_list', []):
                click.echo(f'  - {cpe}')
    if save:
        save_path = path.join(path.expanduser(out_dir), out_file)
        click.echo(f'Saving repository list to {save_path}')
        with click.open_file(save_path, 'w') as f:
            click.echo(message=json.dumps(repo_dict, indent=4), file=f)
