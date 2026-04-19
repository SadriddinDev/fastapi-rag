from fastapi import FastAPI
from app.api.v1.routes import router
from app.api.v1.product_routes import router as product_router
from app.api.v1.rag_routes import router as rag_router

app = FastAPI()

app.include_router(router, prefix="/api/v1")
app.include_router(product_router, prefix="/api/v1/products")
app.include_router(rag_router, prefix="/api/v1/rag")
