from fastapi import APIRouter
from starlette.requests import Request

from dependencies import templates
from utils.dbConn import client

router = APIRouter()

@router.get("/profil")
async def get_profil(request: Request):
    return templates.TemplateResponse("profil.html", {"request": request})


@router.get('/utilisateurs')
def get_utilisateurs():
    db = client['spotiflop']
    collection = db['utilisateur']
    results = []
    for utilisateur in collection.find():
        results.append({
            'username': utilisateur['username'],
            'password': utilisateur['password']
        })
    return results