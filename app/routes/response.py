from dataclasses import dataclass
from fastapi import status
from fastapi.responses import JSONResponse

@dataclass
class Response(dict):
    code: int
    doc: str
    content: dict

    def json(self):
        return JSONResponse(
            status_code=self.code,
            content=self.content
        )

r_200_UPDATE = Response(
    code=status.HTTP_200_OK,
    doc={
        "description": "Phone address updated successfully",
        "content": {
            "application/json": {
                "example": {
                    "details": "OK"
                }
            }
        }
    },
    content={
        "details": "OK"
    }
)

r_201_CREATED = Response(
    code=status.HTTP_201_CREATED,
    doc={
        "description": "Phone address created successfully",
        "content": {
            "application/json": {
                "example": {
                    "details": "Created"
                }
            }
        }
    },
    content={
        "details": "Created"
    }
)

r_204_NO_CONTENT = Response(
    code=status.HTTP_204_NO_CONTENT,
    doc={
        "description": "Phone address deleted successfully",
        "content": {
            "application/json": {
                "example": {
                    "details": "No Content"
                }
            }
        }
    },
    content={
        "details": "No Content"
    }
)

r_404_NOT_FOUND = Response(
    code=status.HTTP_404_NOT_FOUND,
    doc={
        "description": "Phone not found",
        "content": {
            "application/json": {
                "example": {
                    "details": "Phone '+79991234567' not found"
                }
            }
        }
    },
    content={
        "details": "Phone '+79991234567' not found"
    }
)

r_409_CONFLICT = Response(
    code=status.HTTP_409_CONFLICT,
    doc={
        "description": "Phone already exists",
        "content": {
            "application/json": {
                "example": {
                    "details": "Phone '+79991234567' already exists"
                }
            }
        }
    },
    content={
        "details": "Phone '+79991234567' already exists"
    }
)
