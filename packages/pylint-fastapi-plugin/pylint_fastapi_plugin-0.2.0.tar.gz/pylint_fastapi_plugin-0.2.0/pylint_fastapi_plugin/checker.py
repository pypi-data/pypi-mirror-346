from astroid import nodes
from pylint.checkers import BaseChecker

from .messages import MESSAGES
from . import rules as _rules


class FastAPIChecker(BaseChecker):
    """Pylint checker 为 FastAPI 项目提供额外的代码规范校验。"""

    name = "fastapi"
    priority = -1
    msgs = MESSAGES

    # -----------------------------
    # Function / class handlers
    # -----------------------------

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:  # noqa: D401
        """在函数定义节点触发。"""
        is_router_func = False
        if node.decorators:
            for dec in node.decorators.nodes:
                if _rules._is_router_decorator(dec):
                    is_router_func = True
                    _rules.check_router_decorator(dec, self.add_message)
        if is_router_func:
            _rules.check_query_params(node, self.add_message)

    # AsyncFunctionDef 直接复用逻辑
    visit_asyncfunctiondef = visit_functiondef  # type: ignore

    def visit_classdef(self, node: nodes.ClassDef) -> None:  # noqa: D401
        """在类定义节点触发。"""
        _rules.check_pydantic_field(node, self.add_message) 