# Example CLI Application using the Click library

## Project Creation:
```bash
touch __init__.py
# Install pipenv if not already installed
#pip3 install --user -U pipenv

# Create virtual env and install click
pipenv --python python3 install click

# Activate virtual env
pipenv shell
```

## Define CLI Function
_cli.py_
```python
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

```

Mark file as executable: `chmod +x cli.py`

Test the above with `./cli.py --help`. You should see some generic help message output

