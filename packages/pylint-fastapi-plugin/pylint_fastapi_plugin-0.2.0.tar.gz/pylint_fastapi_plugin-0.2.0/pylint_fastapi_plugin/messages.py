MSG_PAGE_SIZE_PARAM = 'W9007'
MSG_RESPONSE_MODEL = 'W9001'
MSG_SUMMARY = 'W9002'
MSG_OPERATION_ID = 'W9003'
MSG_QUERY_PARAMS = 'W9004'
MSG_DESCRIPTION = 'W9005'
MSG_PYDANTIC_FIELD = 'W9006'
MSG_PERMISSION_CHECKER = 'W9008'

# Pylint expects a mapping of message-id -> (template, symbol, help)
# 详情见 https://pylint.pycqa.org/  "Defining a checker" 章节
MESSAGES = {
    MSG_PAGE_SIZE_PARAM: (
        "Query parameter '%s' should be renamed to '%s' with alias",
        "fastapi-router-page-size-param",
        "FastAPI query parameters should use snake_case with camelCase alias",
    ),
    MSG_RESPONSE_MODEL: (
        "Router decorator missing response_model=BaseResponse",
        "fastapi-router-response-model",
        "FastAPI router decorators should include response_model=BaseResponse",
    ),
    MSG_SUMMARY: (
        "Router decorator missing summary parameter",
        "fastapi-router-summary",
        "FastAPI router decorators should include a summary parameter",
    ),
    MSG_OPERATION_ID: (
        "Router decorator missing operation_id parameter",
        "fastapi-router-operation-id",
        "FastAPI router decorators should include an operation_id parameter",
    ),
    MSG_QUERY_PARAMS: (
        "Query parameter should have title and description",
        "fastapi-router-query-params",
        "FastAPI query parameters should include title and description",
    ),
    MSG_DESCRIPTION: (
        "Router decorator missing description parameter",
        "fastapi-router-description",
        "FastAPI router decorators should include a description parameter",
    ),
    MSG_PYDANTIC_FIELD: (
        "Pydantic field must use Field with title and description",
        "pydantic-field-params",
        "Pydantic BaseModel fields must use Field with title and description parameters",
    ),
    MSG_PERMISSION_CHECKER: (
        "Router decorator missing dependencies=[Depends(PermissionChecker(...))]",
        "fastapi-router-permission-checker",
        "FastAPI router decorators should include dependencies=[Depends(PermissionChecker)] for permission control",
    ),
} 