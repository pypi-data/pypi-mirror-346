import re
from typing import Any, ClassVar, Dict, Iterable, Literal, TypedDict

import mistune
from mistune.core import BlockState
from typing_extensions import NotRequired


class SlackBlockStateEnv(TypedDict):
    # This isn't used, just a helpful reference
    border: NotRequired[int]
    bold: NotRequired[bool]
    italic: NotRequired[bool]
    strike: NotRequired[bool]
    code: NotRequired[bool]
    list_indent: NotRequired[int]
    list_style: NotRequired[Literal["bullet", "ordered"]]


class SlackRenderer(mistune.BaseRenderer):
    NAME: ClassVar[Literal["slack"]] = "slack"  # type: ignore

    RICH_TYPE = {"rich_text_section", "rich_text_list", "rich_text_preformatted", "rich_text_quote"}

    HEADING_MAX_LENGTH = 150
    HEADING_OVERFLOW_MESSAGE = " (OVERFLOW)"
    HEADING_USE_HEADER_LTE = 3
    HEADING_ADD_DIVIDER_LTE = 2

    BLOCK_CODE_SPILL_LANG_REGEXP = re.compile(
        r"""^\n*(?P<lang>
        bash|bigquery|c|c++|cpp|cs|csharp|css|csv|docker|dockerfile|go|golang|html|java|javascript|js|json
        |jsonc|jsonl|kotlin|less|lua|makefile|markdown|md|objc|objectivec|perl|php|pl|postcss|powershell|ps
        |ps1|py|python|r|rb|ruby|rust|sass|scala|scss|sh|shell|sql|stylus|swift|ts|typescript|xml|yaml|yml
        )\n""",
        flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
    )

    LIST_MAX_INDENT = 6  # TODO double check this, doc says max 8, but block kit builder only shows 6

    DIVIDER_BLOCK = {"type": "divider"}

    BLANK_LINE_PLACEHOLDER = {"type": "BLANK_LINE_PLACEHOLDER"}

    MAX_NUMBER_OF_BLOCKS: int = 50  # TODO use this in some way

    def __call__(self, tokens: Iterable[Dict[str, Any]], state: BlockState) -> list[dict]:  # type: ignore
        blocks = []
        is_first = True
        last_section = None
        last_rich_type = None
        add_blank_line = False
        sections = list(self.render_tokens(tokens, state))
        for section in sections:
            is_last_block_divider = blocks and blocks[-1]["type"] == "divider"
            is_last_block_header = blocks and blocks[-1]["type"] == "header"
            is_2nd_last_block_header = blocks and len(blocks) > 1 and blocks[-2]["type"] == "header"
            is_different_section_type = last_section and last_section["type"] != section["type"]
            if section == self.BLANK_LINE_PLACEHOLDER:
                add_blank_line = True
            elif section["type"] in self.RICH_TYPE:
                if last_rich_type is None:
                    last_rich_type = {"type": "rich_text", "elements": []}
                    blocks.append(last_rich_type)
                if is_last_block_divider and not is_2nd_last_block_header:
                    last_rich_type["elements"].append({"type": "rich_text_section", "elements": []})
                    last_rich_type["elements"].append(
                        {"type": "rich_text_section", "elements": [{"type": "text", "text": ""}]}
                    )
                    add_blank_line = False
                elif (
                    not is_first
                    and not is_last_block_header
                    and not (is_last_block_divider and is_2nd_last_block_header)
                    and (is_different_section_type or add_blank_line)
                ):
                    last_rich_type["elements"].append(
                        {"type": "rich_text_section", "elements": [{"type": "text", "text": "\n"}]}
                    )
                    add_blank_line = False
                is_first = False
                last_section = section
                last_rich_type["elements"].append(section)
                last_rich_type["elements"] = _collapse_rich(last_rich_type["elements"])
            else:  # header / divider
                if section["type"] == "divider" and last_rich_type:
                    last_rich_type["elements"].append(
                        {"type": "rich_text_section", "elements": [{"type": "text", "text": "\n"}]}
                    )
                    last_rich_type["elements"] = _collapse_rich(last_rich_type["elements"])

                blocks.append(section)
                is_first = False
                last_section = section
                last_rich_type = None
                add_blank_line = False

        # Strip and leading whitespace
        if (
            blocks
            and blocks[0]["type"] == "rich_text"
            and blocks[0]["elements"]
            and blocks[0]["elements"][0]["type"] in {"rich_text_section", "rich_text_quote"}
            and blocks[0]["elements"][0]["elements"]
            and blocks[0]["elements"][0]["elements"][0]["type"] == "text"
        ):
            first_text = blocks[0]["elements"][0]["elements"][0]["text"]
            blocks[0]["elements"][0]["elements"][0]["text"] = first_text.lstrip("\n")
        return blocks

    def render_tokens(self, tokens: Iterable[Dict[str, Any]], state: BlockState) -> list[dict]:  # type: ignore
        children = self.iter_tokens(tokens, state)
        return [x for xs in children for x in xs]  # type: ignore

    #################### Inline Level ####################
    def slack_user(self, token, state: BlockState):
        yield _add_style({"type": "user", "user_id": token["attrs"]["user_id"]}, state)

    def slack_channel(self, token, state: BlockState):
        yield _add_style({"type": "channel", "channel_id": token["attrs"]["channel_id"]}, state)

    def slack_usergroup(self, token, state: BlockState):
        yield _add_style({"type": "usergroup", "usergroup_id": token["attrs"]["usergroup_id"]}, state)

    def slack_broadcast(self, token, state: BlockState):
        yield _add_style({"type": "broadcast", "range": token["attrs"]["range"]}, state)

    def slack_emoji(self, token, state: BlockState):
        yield _add_style({"type": "emoji", "name": token["attrs"]["emoji"]}, state)

    def text(self, token, state: BlockState):
        text = token["raw"]
        if text:
            yield _add_style({"type": "text", "text": text}, state)

    def image(self, token, state: BlockState):
        raise NotImplementedError(f"Images not supported yet, unsure how to handle {token}")

    def emphasis(self, token, state: BlockState):
        yield from self.render_tokens(token["children"], _get_next_state(state, italic=True))

    def strong(self, token, state: BlockState):
        yield from self.render_tokens(token["children"], _get_next_state(state, bold=True))

    def strikethrough(self, token, state: BlockState):
        yield from self.render_tokens(token["children"], _get_next_state(state, strike=True))

    def codespan(self, token, state: BlockState):
        assert "raw" in token
        assert "children" not in token
        yield from self.text({"type": "text", "raw": token["raw"]}, _get_next_state(state, code=True))

    def linebreak(self, token, state: BlockState):
        yield {"type": "text", "text": "\n\n"}

    def softbreak(self, token, state: BlockState):
        yield {"type": "text", "text": "\n"}

    def inline_html(self, token, state: BlockState):
        yield from self.text({"type": "text", "raw": token["raw"]}, _get_next_state(state))

    def link(self, token, state: BlockState):
        children = self.render_tokens(token["children"], _get_next_state(state))
        url = token["attrs"]["url"]
        url = url.strip("\t\r\n ")
        if not url:
            yield from children
        else:
            style = _get_text_style_from_state(state)
            text = ""
            for child in children:
                if child["type"] != "text" or "text" not in child:
                    raise NotImplementedError(f"Cannot create child text, unknown child: {child}")
                style = {**style, **child.get("style", {})}
                text += child["text"]
            item = {"type": "link", "text": text, "url": url}
            if style:
                item["style"] = style
            yield item

    #################### Block Level ####################
    def paragraph(self, token, state: BlockState):
        border = state.env.get("border", 0)
        elements = self.render_tokens(token["children"], state)
        elements = _collapse_rich_text_elements(elements)
        if border == 0:
            yield {"type": "rich_text_section", "elements": elements}
        else:
            item = {"type": "rich_text_quote", "elements": elements}
            if border >= 2:
                item["border"] = 1
            yield item

    def heading(self, token, state: BlockState):
        level = token["attrs"]["level"]
        if level <= self.HEADING_USE_HEADER_LTE:
            yield from self._heading_block(token, state)
            if level <= self.HEADING_ADD_DIVIDER_LTE:
                yield self.DIVIDER_BLOCK
        else:
            yield from self._heading_bold(token, state)

    def _heading_bold(self, token, state: BlockState):
        token_paragraph = {"type": "paragraph", "children": token["children"]}
        pargraph_list = list(self.paragraph(token_paragraph, _get_next_state(state, bold=True)))
        assert len(pargraph_list) == 1 and pargraph_list[0]["type"] == "rich_text_section"
        paragraph = pargraph_list[0]
        elements = paragraph["elements"]
        elements = [{"type": "text", "text": "\n"}, *elements]
        elements = _collapse_rich_text_elements(elements)
        yield {**paragraph, "elements": elements}

    def _heading_block(self, token, state: BlockState):
        text = ""

        def walk(obj):
            nonlocal text

            if obj["type"] == "text":
                before, after = "", ""
            elif obj["type"] == "emphasis":
                before, after = "", ""
            elif obj["type"] == "strong":
                before, after = "", ""
            elif obj["type"] == "strikethrough":
                before, after = "~~", "~~"
            elif obj["type"] == "codespan":
                before, after = "", ""
            elif obj["type"] == "inline_html":
                before, after = "", ""
            else:
                raise NotImplementedError(f"Cannot create child text, unknown child: {obj}")

            text += before
            if "raw" in obj:
                text += obj["raw"]
            for child in obj.get("children", []):
                walk(child)
            text += after

        for child in token["children"]:
            walk(child)

        if len(text) > self.HEADING_MAX_LENGTH:
            text = text[: self.HEADING_MAX_LENGTH - len(self.HEADING_OVERFLOW_MESSAGE)] + self.HEADING_OVERFLOW_MESSAGE
        text = text[: self.HEADING_MAX_LENGTH]  # Just incase!

        yield {"type": "header", "text": {"type": "plain_text", "text": text}}

    def blank_line(self, token, state: BlockState):
        yield self.BLANK_LINE_PLACEHOLDER

    def thematic_break(self, token, state: BlockState):
        yield self.DIVIDER_BLOCK

    def block_code(self, token, state: BlockState):
        _lang = token.get("attr", {}).get("info", None)
        text = token["raw"]
        match = self.BLOCK_CODE_SPILL_LANG_REGEXP.match(text)
        if match:
            _lang = _lang or match.group("lang")
            text = self.BLOCK_CODE_SPILL_LANG_REGEXP.sub("", text)
        item = {
            "type": "rich_text_preformatted",
            "elements": [{"type": "text", "text": text}],
        }
        if state.env.get("border", 0) >= 1:
            item["border"] = 1
        yield item

    def block_quote(self, token, state: BlockState):
        child_state = _get_next_state(state, border=state.env.get("border", 0) + 1)
        yield from self.render_tokens(token["children"], child_state)

    def block_html(self, token, state: BlockState):
        token_block_code = {
            "type": "block_code",
            "raw": token["raw"],
            "style": "fenced",
            "marker": "```",
            "attrs": {"info": "html"},
        }
        yield from self.block_code(token_block_code, state)

    def list(self, token, state: BlockState):
        list_indent = token["attrs"]["depth"]
        list_style = "ordered" if token["attrs"]["ordered"] else "bullet"
        child_state = _get_next_state(state, list_indent=list_indent, list_style=list_style)
        yield from self.render_tokens(token["children"], child_state)

    def list_item(self, token, state: BlockState):
        try:
            list_indent = state.env["list_indent"]
            list_style = state.env["list_style"]
            border = state.env.get("border", 0)
        except Exception as e:
            raise NotImplementedError(f"Block text can only be called from list item, got: {token}") from e
        task_checked = token.get("attrs", {}).get("checked")

        children = self.render_tokens(token["children"], state)
        elements = []
        nested_lists = []
        added_task = False
        for child in children:
            if child["type"] == "rich_text_section":
                if task_checked is not None and not added_task:
                    check_mark = "✅ " if task_checked else "❌ "
                    child["elements"] = [{"type": "text", "text": check_mark}, *child["elements"]]
                    added_task = True
                elements.append(child)
            elif child["type"] == "rich_text_list":
                nested_lists.append(child)
            elif child == self.BLANK_LINE_PLACEHOLDER:
                # elements.append({"type": "rich_text_section", "elements": [{"type": "text", "text": "\n"}]})
                pass  # TODO not sure if we want this
            else:
                raise NotImplementedError(f"Cannot create list item with child: {child}")

        elements = _collapse_rich_text_elements(elements)
        item = {"type": "rich_text_list", "style": list_style, "elements": elements}
        if list_indent > 0:
            if list_indent > self.LIST_MAX_INDENT:
                list_indent = self.LIST_MAX_INDENT
            item["indent"] = list_indent
        if border >= 1:
            item["border"] = 1
        yield item
        yield from nested_lists

    def task_list_item(self, token, state: BlockState):
        token = token.copy()
        token["type"] = "list_item"
        yield from self.list_item(token, state)

    def block_text(self, token, state: BlockState):
        try:
            assert "list_indent" in state.env
            assert "list_style" in state.env
        except Exception as e:
            raise NotImplementedError(f"Block text can only be called from list item, got: {token}") from e

        elements = self.render_tokens(token["children"], state)
        elements = _collapse_rich_text_elements(elements)
        yield {"type": "rich_text_section", "elements": elements}


def _get_next_state(state: BlockState, **kwargs) -> BlockState:
    next_state = BlockState(state)
    next_state.env = {**state.env, **kwargs}
    return next_state


def _get_text_style_from_state(state: BlockState):
    style = {}
    if state.env.get("bold", False):
        style["bold"] = True
    if state.env.get("italic", False):
        style["italic"] = True
    if state.env.get("strike", False):
        style["strike"] = True
    if state.env.get("code", False):
        style["code"] = True
    return style


def _add_style(output, state: BlockState):
    style = _get_text_style_from_state(state)
    if style:
        output["style"] = style
    return output


def _collapse_rich(sections: list[dict]) -> list[dict]:
    collapsed = []
    last_section = None
    for section in sections:
        is_last_section_empty = last_section and not last_section["elements"]
        if (
            section["type"] == "rich_text_section"
            and last_section
            and last_section["type"] == "rich_text_section"
            and not is_last_section_empty
        ):
            elements = [*last_section["elements"], {"type": "text", "text": "\n"}, *section["elements"]]
            last_section["elements"] = _collapse_rich_text_elements(elements)
        elif (
            section["type"] == "rich_text_list"
            and last_section
            and last_section["type"] == "rich_text_list"
            and section.get("style") == last_section.get("style")
            and section.get("indent") == last_section.get("indent")
            and section.get("border") == last_section.get("border")
        ):
            last_section["elements"] = [*last_section["elements"], *section["elements"]]
            last_section["elements"] = _collapse_rich_text_elements(last_section["elements"])
        elif (
            section["type"] == "rich_text_list"
            and last_section
            and last_section["type"] == "rich_text_list"
            and section.get("style") != last_section.get("style")
        ):
            # Bug in slack, sequential rich_text_list are collapsed even if different styles
            collapsed.append({"type": "rich_text_section", "elements": []})
            section = section.copy()
            collapsed.append(section)
            last_section = section
        elif (
            section["type"] == "rich_text_quote"
            and last_section
            and last_section["type"] == "rich_text_quote"
            and section.get("border") == last_section.get("border")
        ):
            last_section["elements"] = [*last_section["elements"], *section["elements"]]
        else:
            section = section.copy()
            collapsed.append(section)
            last_section = section
    return collapsed


def _collapse_rich_text_elements(elements: list[dict]) -> list[dict]:
    collapsed = []
    last_text_element = None
    for item in elements:
        if item["type"] == "text":
            if last_text_element is None:
                last_text_element = item
                collapsed.append(item)
            elif last_text_element.get("style") == item.get("style") or _is_all_newlines(item["text"]):
                last_text_element["text"] += item["text"]
            elif _is_all_newlines(last_text_element["text"]):
                last_text_element["text"] += item["text"]
                if "style" in item:
                    last_text_element["style"] = item["style"]
                else:
                    last_text_element.pop("style", None)
            else:
                last_text_element = item
                collapsed.append(item)
        else:
            last_text_element = None
            collapsed.append(item)
    filtered = []
    for item in collapsed:
        if item["type"] == "text" and item["text"] == "":
            continue
        filtered.append(item)
    return filtered


def _is_all_newlines(text: str) -> bool:
    return text.replace("\n", "") == ""
