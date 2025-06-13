from model.response import APIResponse

def make_response(data=None, code=200, error=None, message=None) -> APIResponse:
    return APIResponse(
        success = error is None,
        data = data,
        code = code,
        error = error,
        message = message
    )