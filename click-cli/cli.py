#!/usr/bin/env python 

import click

@click.command()
@click.option("--filename", "-f", default=None)
@click.option("--region", "-r", default=["us-east-1"], multiple=True)
def cli(filename, region):
    if not filename:
        raise click.UsageError("must provide a filename")


if __name__ == "__main__":
    cli()
