from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter()


@router.get('/')
def index():
	return Response(
		content='{"status_code": 200, "detail": "ok", "result": "working"}',
		media_type='application/json'
	)
