def readme_simple_usage():
    from mistune_slack import render_slack_blocks_from_markdown

    markdown = "# Hello, *world*!"
    blocks = render_slack_blocks_from_markdown(markdown)
    print(blocks)


def readme_advanced_usage():
    import mistune
    from mistune.plugins.formatting import strikethrough
    from mistune.plugins.task_lists import task_lists
    from mistune.plugins.url import url

    from mistune_slack import SlackRenderer, slack_plugin

    markdown = "# Hello, *world*!"
    renderer = mistune.create_markdown(renderer=SlackRenderer(), plugins=[slack_plugin, strikethrough, url, task_lists])
    blocks: list[dict] = renderer(markdown)  # type: ignore
    print(blocks)
