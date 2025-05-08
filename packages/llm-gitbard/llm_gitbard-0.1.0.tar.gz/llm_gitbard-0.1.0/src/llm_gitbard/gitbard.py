import inspect
import re
import sys
from typing import Literal

import llm
import questionary
import rich
import rich_click as click
from click import ParamType
from click.shell_completion import CompletionItem
from pydanclick import from_pydantic
from pydantic import BaseModel, Field
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner

from .configs import CliCommonSettings
from .git import GitRepo
from .prompt import CONVENTIONAL_COMMIT_STYLE, ODOO_COMMIT_STYLE


@click.group()
def gitbard(): ...


class CommitPromptSettings(BaseModel):
    preset: Literal["conventional", "odoo"] = Field(
        default="conventional", description="Commit message style preset"
    )
    prompt: str | None = Field(
        default=None,
        description="Custom prompt to overrides preset style",
    )
    extra_context: str | None = Field(
        default=None, description="Extra context added to the prompt"
    )
    accept: bool = Field(
        default=False,
        description="Accept the generated commit message without modification",
    )


class CommitSettings(CliCommonSettings):
    commit: CommitPromptSettings = CommitPromptSettings()

    def get_commit_style(self):
        if self.commit.prompt:
            return self.commit.prompt

        match self.commit.preset:
            case "conventional":
                return CONVENTIONAL_COMMIT_STYLE
            case "odoo":
                return ODOO_COMMIT_STYLE
            case _:
                return CONVENTIONAL_COMMIT_STYLE

    def build_instrustions(self):
        prompt = self.get_commit_style()
        prompt += "## Output\nOutput the final commit message in a <message> block."
        return prompt

    def get_llm_model(self) -> llm.Model:
        model_obj = llm.get_model(self.model.name)
        if model_obj.needs_key:
            model_obj.key = llm.get_key(
                self.model.api_key, model_obj.needs_key, model_obj.key_env_var
            )
        return model_obj

    def generate_commit_message(self, diff: str):
        model_obj = self.get_llm_model()
        prompt = self.build_instrustions()
        user_prompt = f"""
        ## Git Diff
        {diff}

        ## User Context
        {self.commit.extra_context or "None"}
        """
        with Live(refresh_per_second=10) as live:
            response = model_obj.prompt(
                inspect.cleandoc(user_prompt),
                system=inspect.cleandoc(prompt),
                stream=True,
                **self.model.options,
            )
            live.update(Spinner("dots", text="Generating..."))
            result = ""
            for chunk in response:
                result += chunk
                live.update(
                    Panel(result, title="Generating...", title_align="right", width=80)
                )
            text = re.sub(r"<think>(.+?)</think>", "", response.text())
            match = re.search(r"<message>(.+?)</message>", text, re.DOTALL)
            return match.group(1).strip() if match else ""


class ModelNameType(ParamType):
    name = "model_name"

    def shell_complete(self, ctx, param, incomplete):
        models = llm.get_model_aliases()
        return [
            CompletionItem(name)
            for name in models.keys()
            if name.startswith(incomplete)
        ]


@gitbard.command()
@from_pydantic(
    CommitSettings,
    shorten={
        "model.name": "-m",
        "model.api_key": "-k",
        "model.options": "-o",
        "commit.extra_context": "-X",
        "commit.preset": "-S",
        "commit.prompt": "-P",
        "commit.accept": "-y",
    },
    extra_options={
        "model.name": {
            "type": ModelNameType(),
        }
    },
)
def commit(commit_settings: CommitSettings):
    """
    Generate Commit Message from Staged Diff
    """
    with GitRepo(search_parent_directories=True) as repo:
        diff = repo.get_staged_diff()
        if not diff:
            rich.print("No staged changes found.")
            return

        commit_message = commit_settings.generate_commit_message(diff)
        rich.print(
            Panel(commit_message, title="Commit Message", title_align="right", width=80)
        )

        if commit_settings.commit.accept:
            repo.commit_staged(commit_message, edit=False)
            return

        if not sys.stdin.isatty():
            return

        answer = questionary.select(
            "Action to do",
            choices=[
                questionary.Choice(title="Accept", value="accept", shortcut_key="a"),
                questionary.Choice(title="Edit", value="edit", shortcut_key="e"),
                questionary.Choice(title="Reject", value="reject", shortcut_key="r"),
            ],
            use_arrow_keys=True,
            use_jk_keys=True,
            use_shortcuts=True,
        ).ask()
        match answer:
            case "accept":
                repo.commit_staged(commit_message, edit=False)
            case "edit":
                repo.commit_staged(commit_message, edit=True)
            case _:
                return
