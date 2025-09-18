from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import items, recipes, graph, algorithms
from .database import Base, engine


def create_app() -> FastAPI:
    app = FastAPI(title="Crafting API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(items.router, prefix="/items", tags=["items"])
    app.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
    app.include_router(graph.router, prefix="/graph", tags=["graph"])
    app.include_router(algorithms.router, prefix="/algorithms", tags=["algorithms"])

    @app.get("/")
    def root():
        return {"status": "ok"}

    return app


app = create_app()


