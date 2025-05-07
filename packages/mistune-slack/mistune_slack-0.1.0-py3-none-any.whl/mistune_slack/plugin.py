import re

from mistune import InlineParser, InlineState, Markdown


def slack_plugin(md: Markdown, *, no_backtick_relace: bool = False):
    USER_PATTERN = r"(?P<slack_user_raw><@(?P<slack_user_id>[UW][A-Z0-9]+)(?:\|[^>]*)?>)"
    CHANNEL_PATTERN = r"(?P<slack_channel_raw><#(?P<slack_channel_id>[CDG][A-Z0-9]+)(?:\|[^>]*)?>)"
    BROADCAST_PATTERN = r"(?P<slack_broadcast_raw>@(?P<slack_range>here|channel|everyone)\b)"
    EMOJI_PATTERN = r"(?P<slack_emoji_raw>:(?P<slack_emoji_name>[a-z0-9_\-]+):)"

    def parse_slack_user(block: InlineParser, m: re.Match, state: InlineState):
        raw = m.group("slack_user_raw")
        user_id = m.group("slack_user_id")
        state.append_token({"type": "slack_user", "raw": raw, "attrs": {"user_id": user_id}})
        return m.end()

    def parse_slack_channel(block: InlineParser, m: re.Match, state: InlineState):
        raw = m.group("slack_channel_raw")
        channel_id = m.group("slack_channel_id")
        state.append_token({"type": "slack_channel", "raw": raw, "attrs": {"channel_id": channel_id}})
        return m.end()

    def parse_slack_broadcast(block: InlineParser, m: re.Match, state: InlineState):
        raw = m.group("slack_broadcast_raw")
        range = m.group("slack_range")
        state.append_token({"type": "slack_broadcast", "raw": raw, "attrs": {"range": range}})
        return m.end()

    def parse_slack_emoji(block: InlineParser, m: re.Match, state: InlineState):
        raw = m.group("slack_emoji_raw")
        emoji = m.group("slack_emoji_name")
        state.append_token({"type": "slack_emoji", "raw": raw, "attrs": {"emoji": emoji}})
        return m.end()

    md.inline.register("slack_user", USER_PATTERN, parse_slack_user, before="link")
    md.inline.register("slack_channel", CHANNEL_PATTERN, parse_slack_channel, before="link")
    md.inline.register("slack_broadcast", BROADCAST_PATTERN, parse_slack_broadcast, before="link")
    md.inline.register("slack_emoji", EMOJI_PATTERN, parse_slack_emoji, before="link")
