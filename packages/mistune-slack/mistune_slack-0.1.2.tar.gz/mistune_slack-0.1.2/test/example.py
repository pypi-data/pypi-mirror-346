import json
import urllib.parse
import webbrowser
from pathlib import Path

from rich.pretty import pprint

from mistune_slack.util import render_slack_blocks_from_markdown

TESTDATA_DIR = Path(__file__).resolve().parent / "testdata"
EXAMPLE_PATH = TESTDATA_DIR / "kitchen_sink.md"


def example(*, open_browser: bool = True):
    markdown = EXAMPLE_PATH.read_text()
    blocks = render_slack_blocks_from_markdown(markdown)

    pprint(blocks)
    blocks_json = json.dumps({"blocks": blocks}, separators=(",", ":"))

    if open_browser:
        url = "https://app.slack.com/block-kit-builder/#" + urllib.parse.quote(blocks_json)
        webbrowser.open(url, autoraise=False)


if __name__ == "__main__":
    example()
