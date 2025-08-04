from fastapi.exceptions import HTTPException


class UnkonwnRepoType(HTTPException):
    def __init__(self, repo_name: str):
        super().__init__(
            status_code=500, detail=f"Unknownn ShortUrlRepo type - {repo_name}"
        )
