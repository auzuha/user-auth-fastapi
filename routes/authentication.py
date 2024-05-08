from fastapi import APIRouter, HTTPException, Depends
from models.api import GetTokenRequest, GetTokenResponse
from services.authentication import create_token

app = APIRouter(prefix="/auth")

@app.post('/get_token', response_model=GetTokenResponse)
async def get_token(request: GetTokenRequest):
    try:
        token = create_token(request.dict())
        return GetTokenResponse(token=token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'User not found.')