from fastapi import FastAPI
from routes.authentication import app as authRouter
from routes.user import app as userRouter
from services.authentication import validate_token


async def custom_middleware(request, call_next):
    print('MIDDLEWARE TRIGGERED')
    print(request.url.path)
    if request.url.path.startswith("/auth"):
        response = await call_next(request)
        return response    
    auth_token = request.headers.get('Authorization')
    token = auth_token.split()[1]

    validate_token(request, token)
    
    response = await call_next(request)
    return response




#create fastapi app
app = FastAPI()
app.middleware("http")(custom_middleware)

app.include_router(authRouter)
app.include_router(userRouter)


@app.get('/')
def _main():
    return {'msg' : 'alive'}


