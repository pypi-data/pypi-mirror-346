import click
import requests 
import json
from my_cli_project import utils
from my_cli_project.utils import reverse_string

@click.group()
def cli():
    """My CLI tool"""
    pass

def process_text_(text: str) -> str:
    """A custom function that processes input text by converting it to uppercase."""
    return text.upper()

def greet_(name):
    """Greet the user"""
    greeting = f"Hello, {name}!"
    return greeting

def return_pokemon_(pokemon):
    r = requests.get('https://pokeapi.co/api/v2/pokemon/{pokemon}'.format(pokemon=pokemon))
    parsed = json.loads(r.text)
    retjson = json.dumps(parsed, indent=4)
    return retjson

#Command: `mycli cap abc`
@cli.command(name='cap')
@click.argument('text')
def cap(text):
    """CLI command to process text using the process_text function."""
    result = process_text_(text)
    click.echo(f"Processed text: {result}")

#Command: `mycli reverse abc`
@cli.command(name='reverse')
@click.argument('text')
def reverse(text):
    """CLI command that processes text using the imported utils.reverse_string function"""
    result = reverse_string(text)
    click.echo(f"Processed text: {result}")

#Command: `mycli greet --name ian`
@cli.command(name='greet')
@click.option('--name', default='World', help='Name to greet')
def greet(name):
    """A CLI command that greets the user provided with the --name flag."""
    result = greet_(name)
    click.echo(f"{result}")
    return result

#Command: `mycli return_pokemon --pokemon charizard`
@cli.command(name='return_pokemon')
@click.option('--pokemon', default='Charizard', help='Name of pokemon')
def return_pokemon(pokemon):
    """A CLI command that returns the pokemon provided with the --pokemon flag."""
    result = return_pokemon_(pokemon)
    click.echo(f"{result}")
    return result