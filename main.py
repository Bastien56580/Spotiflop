from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from dependencies import templates
from routers import auth, musique, user
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    auth.router,
    prefix="/auth"
)

app.include_router(
    musique.router,
    prefix="/musique"
)

app.include_router(
    user.router,
    prefix="/user"
)


# The index of the application
@app.route("/", methods=["GET", "POST"])
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
