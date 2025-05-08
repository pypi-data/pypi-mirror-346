import llm
from click import Group

from .gitbard import gitbard


@llm.hookimpl
def register_commands(cli: Group):
    cli.add_command(gitbard, "gitbard")
