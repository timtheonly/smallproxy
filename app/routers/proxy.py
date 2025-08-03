import requests
from fastapi import APIRouter, HTTPException, Depends, Response
from starlette.requests import Request
from urllib.parse import urlparse

from app.dependencies import get_repo
from app.lib.data_access.short_url_repo import ShortUrlRepo
from app.models.short_url import ShortUrl

proxy_router = APIRouter(
    prefix="/s",
    tags=["proxy"],
)


@proxy_router.api_route("/{short_url_id}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_request(
    request: Request, short_url_id: str, repo: ShortUrlRepo = Depends(get_repo)
):
    short_url: ShortUrl | None = repo.get(short_url_id)
    if not short_url:
        raise HTTPException(status_code=404, detail="Short url not found")

    body = await request.body()
    target_url = urlparse(short_url.long_url)

    headers: dict[str, str] = dict(request.headers)
    if headers.get("referer"):
        del headers["referer"]
    if headers.get("origin"):
        del headers["origin"]

    headers.update(
        {
            "host": target_url.netloc,
            "path": target_url.path,
        }
    )

    proxied_response = requests.request(
        request.method, short_url.long_url, headers=headers, data=body
    )

    response_headers = dict(proxied_response.headers)
    del response_headers[
        "Content-Encoding"
    ]  # requests will have already decompressed the response

    return Response(
        proxied_response.text,
        status_code=proxied_response.status_code,
        headers=response_headers,
    )
