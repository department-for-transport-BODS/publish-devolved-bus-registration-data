.PHONY: pytest

run:
	uvicorn src.main:app --reload --port 8000

pytest:
	pytest  --cov=. --cov-report term-missing #--cov-report=html

slocal:
	sam local start-api #--docker-network host

sbuild:
	sam build