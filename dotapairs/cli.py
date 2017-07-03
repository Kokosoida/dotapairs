import click

from dotapairs.getter import get_and_save_matches, get_max_seq_num


@click.command()
def get_matches():
    while 1:
        get_and_save_matches(get_max_seq_num() + 1)
