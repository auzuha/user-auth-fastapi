from fastapi import FastAPI
from routes.authentication import app as authRouter
from routes.user import app as userRouter
from services.authentication import validate_token


async def custom_middleware(request, call_next):
    """
    This is a middleware function for the app, this will be triggered first before the request is
    passed to any of the routes.
    This middleware checks and validates the Bearer token that is passed for all endpoints except
    the '/auth*' routes.
    """

    if request.url.path.startswith("/auth"):
        response = await call_next(request)
        return response    
    
    #get the token from the header
    auth_token = request.headers.get('Authorization')
    token = auth_token.split()[1]

    #validate the token and store user details in state
    validate_token(request, token)
    
    response = await call_next(request)
    return response




#create fastapi app
app = FastAPI()
app.middleware("http")(custom_middleware)

#include additional routers
app.include_router(authRouter)
app.include_router(userRouter)


@app.get('/')
def _main():
    return {'msg' : 'alive'}


