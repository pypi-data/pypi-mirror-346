import mistune
from mistune.plugins.formatting import strikethrough
from mistune.plugins.task_lists import task_lists
from mistune.plugins.url import url

from mistune_slack.plugin import slack_plugin
from mistune_slack.renderer import SlackRenderer


def slack_markdown_renderer():
    return mistune.create_markdown(renderer=SlackRenderer(), plugins=[slack_plugin, strikethrough, url, task_lists])


def render_slack_blocks_from_markdown(markdown: str) -> list[dict]:
    renderer = slack_markdown_renderer()
    return renderer(markdown)  # type: ignore
