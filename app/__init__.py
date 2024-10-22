from fastapi import FastAPI
from app.routes import auth, report, template
from fastapi.middleware.cors import CORSMiddleware

def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins, use specific domains in production (e.g., ["http://localhost:3000"])
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE)
        allow_headers=["*"],  # Allows all headers
    )
    # Add routes
    app.include_router(auth.router)
    app.include_router(report.router)
    app.include_router(template.router)

    # Add middleware for authentication
    # app.middleware('http')(auth_middleware)

    return app
