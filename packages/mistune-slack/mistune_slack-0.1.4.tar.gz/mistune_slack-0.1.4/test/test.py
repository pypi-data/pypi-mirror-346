import json
from pathlib import Path

from mistune_slack.util import render_slack_blocks_from_markdown

TEST_DIR = Path(__file__).resolve().parent / "testdata"


def test_kitchen_sink():
    run_file("kitchen_sink")


def test_everything_but_the_kitchen_sink() -> None:
    run_file("backtick_backslash_escape")
    run_file("backtick_backslash_escape_space")
    run_file("backtick_double_code")
    run_file("backtick_escape_hanging")
    run_file("backtick_escape_one")
    run_file("backtick_simple")
    run_file("backtick_sql_escape")
    run_file("backtick_sql_wrong")
    run_file("bullet_margin")
    run_file("headings")


def run_file(prefix: str, *, _save_test_data: bool = False):
    markdown_path_md_txt = TEST_DIR / f"{prefix}.md.txt"
    markdown_path_md = TEST_DIR / f"{prefix}.md"
    if markdown_path_md_txt.exists() and markdown_path_md.exists():
        raise Exception(f"Cannot have both {markdown_path_md_txt} and {markdown_path_md} files")
    markdown_path = markdown_path_md if not markdown_path_md_txt.exists() else markdown_path_md_txt
    json_path = TEST_DIR / f"{prefix}.json"

    actual_blocks = render_slack_blocks_from_markdown(markdown_path.read_text())
    if _save_test_data:
        json_path.write_text(json.dumps(actual_blocks, indent=4))

    expected_blocks = json.loads((TEST_DIR / f"{prefix}.json").read_text())

    assert actual_blocks == expected_blocks
