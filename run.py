import os

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 8000))
	# Use uvicorn to run the FastAPI app defined in app/main.py
	import uvicorn

	uvicorn.run("app.main:app", host="0.0.0.0", port=port)
