from typing import TYPE_CHECKING, Optional

from astroid import nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def node_to_module_item(node: nodes.NodeNG) -> str:
    if isinstance(node, nodes.Name):
        return node.name
    if isinstance(node, nodes.Attribute):
        attrs = []
        while True:
            if isinstance(node, nodes.Attribute):
                attrs.append(node.attrname)
                node = node.expr
            elif isinstance(node, nodes.Name):
                attrs.append(node.name)
                break
            else:
                raise ValueError("unexpected node")
        attrs.reverse()
        return ".".join(attrs)
    raise ValueError("unexpected node")


def module_item_to_modname_and_name(module_item: str) -> tuple[str, str]:
    parts = module_item.split(".")
    if len(parts) < 2:
        raise ValueError(
            f"{module_item} is not a module item because it does not have a dot"
        )

    modname = ".".join(parts[:-1])
    name = parts[-1]
    return (modname, name)


def modname_and_name_to_module_item(modname: str, name: str) -> str:
    return f"{modname}.{name}"


class RestrictedModuleItemsChecker(BaseChecker):
    name = "restricted-module-items"
    msgs = {
        "E9601": (
            "%s is restricted",
            "restricted-module-items",
            "Consult your team members for why this is restricted",
        ),
    }
    options = (
        (
            "restricted-module-items",
            {
                "default": (),
                "type": "csv",
                "metavar": "<module-items>",
                "help": "e.g. urllib.parse.urlparse",
            },
        ),
    )

    def __init__(self, linter: Optional["PyLinter"] = None) -> None:
        super().__init__(linter)

    def open(self) -> None:
        super().open()
        self.module_item_map = {}
        self.modname_map = {}
        for module_item in self.linter.config.restricted_module_items:
            self.module_item_map[module_item] = True
            modname, name = module_item_to_modname_and_name(module_item)
            if modname not in self.modname_map:
                self.modname_map[modname] = {}
            self.modname_map[modname][name] = True

    def visit_call(self, node: nodes.Call) -> None:
        module_item = node_to_module_item(node.func)
        if module_item in self.module_item_map:
            self.add_message("restricted-module-items", node=node, args=module_item)

    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        # When modname is None, it is a relative import.
        # We do not support relative import.
        if node.modname is None:
            return
        if node.modname not in self.modname_map:
            return
        m = self.modname_map[node.modname]
        for name, _alias in node.names:
            if name in m:
                module_item = modname_and_name_to_module_item(node.modname, name)
                self.add_message("restricted-module-items", node=node, args=module_item)


def register(linter: "PyLinter") -> None:
    linter.register_checker(RestrictedModuleItemsChecker(linter))
