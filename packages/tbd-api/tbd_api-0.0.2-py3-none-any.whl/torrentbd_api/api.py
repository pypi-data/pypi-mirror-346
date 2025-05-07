from fastapi import FastAPI, Query
from .search import search_torrents
from .profile import get_user_profile

app = FastAPI(title="TorrentBD API")

@app.get("/search")
def search(query: str = Query(..., description="Search term"), page: int = 1):
    """
    Search for torrents on TorrentBD.
    """
    result = search_torrents(query, page)
    return {"result": result}

@app.get("/profile")
def profile():
    """
    Get user profile information.
    """
    result = get_user_profile()
    return {"result": result}


