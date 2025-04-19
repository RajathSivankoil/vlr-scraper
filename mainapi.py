from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api.get_all_player_stats import get_all_player_stats
from api.get_player_agent_stats import get_player_agent_stats
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="vlr-scraper-api",
    description="API for VLR.gg player and team stats, Made by Rajath Sivankoil",
    docs_url="/",
    redoc_url=None,
)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/favicon.ico")
def favicon():
    return FileResponse(r"favicon.ico")

@app.get("/player/{player_id}")
def get_player_agent_stats_endpoint(player_id: int, timespan: int = 30):
    player_data = get_player_agent_stats(player_id, timespan)
    if player_data is None:
        return JSONResponse(status_code=404, content={"message": "Player not found"})
    return JSONResponse(content=player_data)

@app.get("/players/{region}")
def get_all_player_stats_endpoint(region: str = "all", timespan: int = 60):
    player_data = get_all_player_stats(region, timespan)
    if player_data is None:
        return JSONResponse(status_code=404, content={"message": "No data found"})
    return JSONResponse(content=player_data)