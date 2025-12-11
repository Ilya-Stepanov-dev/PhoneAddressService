run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-docker:
	docker compose up -d

stop:
	docker compose down

restart:
	docker compose restart
