
from pydantic import BaseModel, Field, model_validator


class ProcessRequest(BaseModel):
    file_id: str = Field(min_length=1)
    chunk_size: int = Field(default=1000, ge=1)
    overlap_size: int = Field(default=200, ge=0)

    @model_validator(mode="after")
    def validate_overlap_size(self):
        if self.overlap_size >= self.chunk_size:
            raise ValueError("overlap_size must be less than chunk_size")

        return self