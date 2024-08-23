from fastapi import Request
import logging, time, sys
from auth import authorization


logger = logging.getLogger()

formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(message)s',
)
stream_handler = logging.StreamHandler(sys.stdout)
logger.handlers = [stream_handler]
logger.setLevel(logging.INFO)

async def log_middleware(request: Request, call_next):
    start = time.time()
    process_time = time.time() - start
    log_dict = {
        'url': request.url.path,
        'method': request.method, 
        'response_time': process_time
    }
    logger.info(log_dict)

    response = await call_next(request)
    return response


def authorize_user(request: Request, call_next):
    # get permissions json from authorization service (or cache)
    user_permissions_json = get_user_permissions_json()

    # get current resource id from uri
    resource = get_resource_type(request.url)

    # extract resource permissions from json
    allowed_resources = extract_resource_permissions(user_permissions_json, resource)

    # determine if permissions grant resource access
    permission_allowed = is_authorized(resource, allowed_resources)
    if not permission_allowed:
        raise HTTPException(
            status_code=401,
            detail="User does not have access to this resource.",
        )
    response = call_next(request)
    return response
