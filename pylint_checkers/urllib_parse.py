from typing import TYPE_CHECKING, Optional

from astroid import nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


NAME = "urllib-parse-rfc3986"
MESSAGE = "urlparse and urlunparse implements RFC1808, not RFC3986. Use urlsplit and urlunsplit instead."

BANNED_NAMES = ["urlparse", "urlunparse"]


class URLlibParseRFC3986Checker(BaseChecker):
    name = NAME
    msgs = {
        "E9501": (
            MESSAGE,
            NAME,
            MESSAGE,
        ),
    }

    def __init__(self, linter: Optional["PyLinter"] = None) -> None:
        super().__init__(linter)

    def visit_call(self, node: nodes.Call) -> None:
        if (isinstance(node.func, nodes.Name) and node.func.name in BANNED_NAMES) or (
            isinstance(node.func, nodes.Attribute)
            and node.func.attrname in BANNED_NAMES
        ):
            self.add_message(NAME, node=node)


def register(linter: "PyLinter") -> None:
    linter.register_checker(URLlibParseRFC3986Checker(linter))
