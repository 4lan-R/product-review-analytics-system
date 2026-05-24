from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.reviews import router as reviews_router
from database import init_db

app = FastAPI(
    title="Product Review Analytics System",
    description="REST APIs for product review analytics. The application scrapes product reviews using Playwright and BeautifulSoup, stores data using SQLAlchemy ORM and SQLite, manages schema changes with Alembic, and performs sentiment analysis and keyword extraction using VADER Sentiment to generate actionable insights from customer reviews.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(reviews_router)


@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    init_db()



@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to Product Review Analytics System"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
