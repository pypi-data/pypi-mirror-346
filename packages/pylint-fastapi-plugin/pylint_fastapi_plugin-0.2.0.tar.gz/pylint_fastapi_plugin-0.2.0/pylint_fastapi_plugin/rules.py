from typing import Callable, Set

import astroid
from astroid import nodes

from .messages import (
    MSG_DESCRIPTION,
    MSG_OPERATION_ID,
    MSG_PAGE_SIZE_PARAM,
    MSG_PERMISSION_CHECKER,
    MSG_PYDANTIC_FIELD,
    MSG_QUERY_PARAMS,
    MSG_RESPONSE_MODEL,
    MSG_SUMMARY,
)

# -------------------------------------------------------------
# 公共工具
# -------------------------------------------------------------

_ROUTER_METHODS: Set[str] = {
    "get",
    "post",
    "put",
    "delete",
    "patch",
    "options",
    "head",
    "trace",
}


def _is_router_decorator(node: nodes.NodeNG) -> bool:
    """判断装饰器节点是否为 FastAPI 路由装饰器。"""
    if not isinstance(node, nodes.Call) or not hasattr(node.func, "attrname"):
        return False
    return node.func.attrname in _ROUTER_METHODS


# -------------------------------------------------------------
# Router decorator rules
# -------------------------------------------------------------

def check_router_decorator(node: nodes.Call, add_message: Callable) -> None:
    """校验路由装饰器关键字参数。"""
    _check_response_model(node, add_message)
    _check_summary(node, add_message)
    _check_operation_id(node, add_message)
    _check_description(node, add_message)
    _check_permission_checker(node, add_message)


def _check_response_model(node: nodes.Call, add_message: Callable) -> None:
    for kw in node.keywords:
        if kw.arg == "response_model" and isinstance(kw.value, astroid.Name):
            if kw.value.name == "BaseResponse":
                return
    add_message(MSG_RESPONSE_MODEL, node=node)


def _check_summary(node: nodes.Call, add_message: Callable) -> None:
    if not any(kw.arg == "summary" for kw in node.keywords):
        add_message(MSG_SUMMARY, node=node)


def _check_operation_id(node: nodes.Call, add_message: Callable) -> None:
    if not any(kw.arg == "operation_id" for kw in node.keywords):
        add_message(MSG_OPERATION_ID, node=node)


def _check_description(node: nodes.Call, add_message: Callable) -> None:
    if not any(kw.arg == "description" for kw in node.keywords):
        add_message(MSG_DESCRIPTION, node=node)


def _check_permission_checker(node: nodes.Call, add_message: Callable) -> None:
    """确保 dependencies 中包含 Depends(PermissionChecker(...))。"""
    for kw in node.keywords:
        if kw.arg != "dependencies" or not isinstance(kw.value, nodes.List):
            continue
        # dependencies=[Depends(...), ...]
        for elt in kw.value.elts:
            if (
                isinstance(elt, nodes.Call)
                and hasattr(elt.func, "name")
                and elt.func.name == "Depends"
                and elt.args
            ):
                arg0 = elt.args[0]
                if (
                    isinstance(arg0, nodes.Call)
                    and hasattr(arg0.func, "name")
                    and arg0.func.name == "PermissionChecker"
                    and arg0.args  # 必须带参数
                ):
                    return
    add_message(MSG_PERMISSION_CHECKER, node=node)


# -------------------------------------------------------------
# Query parameter rules
# -------------------------------------------------------------

def check_query_params(func_node: nodes.FunctionDef, add_message: Callable) -> None:
    """检查分页相关查询参数命名及注解。"""
    # 收集 import 名称，判断 Query 是否已导入
    imports = {name for name, _ in func_node.root().scope().locals.items()}

    total_args = func_node.args.args
    defaults = func_node.args.defaults or []
    offset = len(total_args) - len(defaults)

    for idx, arg in enumerate(total_args):
        if not hasattr(arg, "name"):
            continue
        default_val = None
        if idx >= offset:
            default_val = defaults[idx - offset]

        # 检查 title/description
        if default_val and isinstance(default_val, nodes.Call):
            _validate_query_title_description(arg, default_val, imports, add_message)

        # page size 相关
        _validate_page_size_param(arg, default_val, imports, add_message)


def _validate_query_title_description(
    arg: nodes.AssignName,
    default_val: nodes.Call,
    imports: Set[str],
    add_message: Callable,
) -> None:
    if not (
        hasattr(default_val.func, "name")
        and default_val.func.name == "Query"
        and "Query" in imports
    ):
        return

    has_title = any(kw.arg == "title" for kw in default_val.keywords)
    has_desc = any(kw.arg == "description" for kw in default_val.keywords)
    if not (has_title and has_desc):
        add_message(MSG_QUERY_PARAMS, node=arg)


def _validate_page_size_param(
    arg: nodes.AssignName,
    default_val: nodes.NodeNG | None,
    imports: Set[str],
    add_message: Callable,
) -> None:
    param_name = arg.name
    is_page_size = param_name.lower() in {"page_size", "pagesize"}

    has_alias_page_size = False
    if (
        default_val
        and isinstance(default_val, nodes.Call)
        and hasattr(default_val.func, "name")
        and default_val.func.name == "Query"
        and "Query" in imports
    ):
        for kw in default_val.keywords:
            if kw.arg == "alias" and isinstance(kw.value, nodes.Const):
                if kw.value.value in {"pageSize", "page_size"}:
                    has_alias_page_size = True
                    is_page_size = True
                    break

    if not is_page_size:
        return

    if param_name == "pageSize":
        add_message(MSG_PAGE_SIZE_PARAM, node=arg, args=(param_name, "page_size"))
    elif param_name == "page_size" and not has_alias_page_size:
        add_message(MSG_PAGE_SIZE_PARAM, node=arg, args=(param_name, "page_size with alias"))


# -------------------------------------------------------------
# Pydantic model field rules
# -------------------------------------------------------------

def check_pydantic_field(class_node: nodes.ClassDef, add_message: Callable) -> None:
    """Pydantic BaseModel 字段必须使用 Field 并包含 title/description。"""
    if not any(hasattr(base, "name") and base.name == "BaseModel" for base in class_node.bases):
        return

    for child in class_node.body:
        if not isinstance(child, nodes.AnnAssign):
            continue

        value = getattr(child, "value", None)
        if not (
            value
            and isinstance(value, nodes.Call)
            and hasattr(value.func, "name")
            and value.func.name == "Field"
        ):
            continue

        has_title = any(kw.arg == "title" for kw in value.keywords)
        has_desc = any(kw.arg == "description" for kw in value.keywords)

        if not (has_title and has_desc):
            add_message(MSG_PYDANTIC_FIELD, node=child) 