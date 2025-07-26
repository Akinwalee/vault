import click
from cli.command_router import route_command

@click.group()
def cli():
    """
    CLI application for various commands.
    Use 'cli --help' to see available commands.
    """
    pass

@cli.command(name='vault')
@click.argument('command_name')
@click.argument('args', nargs=-1)
def execute_command(command_name, args):
    """
    Execute a command by its name.
    
    :param command_name: The name of the command to execute.
    :param args: Additional arguments for the command.
    """
    try:
        result = route_command(command_name, *args)
        click.echo(f"Command '{command_name}' executed successfully: \n{result}")
    except ValueError as e:
        click.echo(f"Error: {e}")