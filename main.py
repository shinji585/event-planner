import webbrowser
from threading import Timer
from fastapi import FastAPI, status
from starlette.responses import RedirectResponse
from routes.users import user_router
import uvicorn


app = FastAPI()

# Register routes

@app.get("/", include_in_schema=True)
async def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_301_MODIFIED)

def open_browser():
    webbrowser.open(
        "https://stackoverflow.com/", new=1, autoraise=True
    )

app.include_router(user_router, prefix="/user")

if __name__ == "__main__":
    Timer(1, open_browser).start()

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)