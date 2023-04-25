from fastapi import APIRouter
from starlette.requests import Request
import json

from dependencies import templates
from utils import log_user, db
from utils.dbConn import users_collection

router = APIRouter()


@router.get("/connexion")
async def get_connexion(request: Request):
    return templates.TemplateResponse("connexion.html", {"request": request})


@router.post("/connexion")
async def post_connexion(request: Request):
    # Log the user
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    result = await log_user(db, username, password)
    if result.get("success"):
        response = templates.TemplateResponse("index.html", {"request": request, "result": result})
        response.set_cookie(key="user_id", value=result["user_id"])
        return response
    else:
        return templates.TemplateResponse("connexion.html", {"request": request, "result": result})


@router.get("/inscription")
async def get_inscription(request: Request):
    return templates.TemplateResponse("inscription.html", {"request": request})


@router.post("/inscription")
async def register_user(request: Request):
    # Récupération des données du formulaire
    form_data = await request.form()
    # Conversion en dictionnaire
    user = dict(form_data)
    # Conversion en JSON si ce n'est pas déjà fait
    try:
        user = json.loads(user)
    except:
        pass
    # Vérification si les données de l'utilisateur sont valides
    if not user:
        return templates.TemplateResponse("inscription.html", {"request": request, "data": "Données invalides"})
    # Vérification si l'utilisateur existe déjà
    if users_collection.find_one({"username": user.get("username")}):
        return templates.TemplateResponse("inscription.html",
                                          {"request": request, "data": "Nom d'utilisateur déjà existant"})
    # Ajout de l'utilisateur à la collection MongoDB
    result = users_collection.insert_one(user)
    # Renvoi des données de l'utilisateur ajouté
    return templates.TemplateResponse("connexion.html", {"request": request, "result": result})
