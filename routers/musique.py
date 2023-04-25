import shutil

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, FileResponse

from dependencies import templates
from utils.dbConn import client

router = APIRouter()

@router.get("/ajouterTitre")
async def get_ajouter_titre(request: Request):
    return templates.TemplateResponse("ajouterTitre.html", {"request": request})


@router.post('/ajouterTitre')
def post_ajouter_titre(
        musique: UploadFile = File(...),
        titre: str = Form(...),
        artiste: str = Form(...)):
    db = client['spotiflop']
    collection = db['titres']
    new_titre = {'titre': titre, 'artiste': artiste, 'musiquePath': musique.filename}
    new_musique = collection.insert_one(new_titre)

    if not new_musique:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save track to database"
        )
    musique_path = musique.filename.replace(' ', '')
    with open(f"musique/{musique_path}", "wb") as buffer:
        shutil.copyfileobj(musique.file, buffer)

    return Response(content="Music has been successfully saved", status_code=200)


@router.get('/titres')
async def get_titres(request: Request):
    db = client['spotiflop']
    users = db['titres'].find()
    result = []
    for user in users:
        result.append({
            'titre': user['titre'],
            'artiste': user['artiste'],
            'musiquePath': user['musiquePath']
        })
    return templates.TemplateResponse("titres.html", {"request": request, "result": result})

@router.get("/download/{file_name}")
async def download_music(file_name: str):
    file_path = f"musique/{file_name}"
    return FileResponse(file_path)