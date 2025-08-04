from fastapi import Depends, APIRouter

from app.dependencies import get_repo
from app.lib.data_access.short_url_repo import ShortUrlRepo
from app.models.short_url import ShortUrl

api_router = APIRouter(
    prefix="/api",
    tags=["api"],
)


@api_router.get("/short_url/{short_url_id}")
async def get_short_url(
    short_url_id: str, repo: ShortUrlRepo = Depends(get_repo)
) -> ShortUrl | None:
    return repo.get(short_url_id)


@api_router.get("/short_url")
async def get_all(repo: ShortUrlRepo = Depends(get_repo)) -> list[ShortUrl]:
    return repo.get_all()


@api_router.post("/short_url/")
async def create_short_url(
    short_url: ShortUrl, repo: ShortUrlRepo = Depends(get_repo)
) -> ShortUrl | None:
    if repo.set(short_url):
        return short_url
    return None


@api_router.delete("/short_url/{short_url_id}")
async def delete_short_url(short_url_id: str, repo: ShortUrlRepo = Depends(get_repo)):
    if repo.delete(short_url_id):
        return {"success": True}
    return {"success": False}


@api_router.put("/short_url/{short_url_id}")
async def update_short_url(
    short_url_id: str, short_url: ShortUrl, repo: ShortUrlRepo = Depends(get_repo)
):
    if repo.update(short_url_id, short_url):
        return {"success": True}
    return {"success": False}
