from pydantic import BaseModel, Field

ALLOWED_CATEGORIES = {"Gaming", "Podcasts", "Cricket", "Other Sports", "Other"}


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    category: str
    video_filename: str | None = None
    video_size_bytes: int | None = Field(default=None, ge=0)


class Project(ProjectCreate):
    id: str