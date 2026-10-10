
from app.modules.processing.dto import ProcessRequest


def validate_process_request(request: ProcessRequest) -> ProcessRequest:
    return request