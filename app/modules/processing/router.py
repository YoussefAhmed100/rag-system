
from fastapi import APIRouter

from app.modules.processing.controller import ProcessingController
from app.modules.processing.dto import ProcessRequest


router = APIRouter(
    prefix="/api/v1/data",
    tags=["processing"],
)


@router.post("/process/{project_id}")
def process_file(
    project_id: str,
    request: ProcessRequest,
):
    controller = ProcessingController()

    return controller.process_file(
        project_id=project_id,
        request=request,
    )