from fastapi import FastAPI
from fastapi.responses import JSONResponse
from get_all_player_stats import get_all_player_stats
from get_player_agent_stats import get_player_agent_stats
from fastapi.responses import FileResponse


app = FastAPI()

@app.get("/favicon.ico")
def favicon():
    return FileResponse("favicon.ico")

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