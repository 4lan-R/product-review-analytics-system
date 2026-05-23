"""Database management utilities"""
from database import engine, Base, SessionLocal
from models import Review


def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


def reset_db():
    """Reset database - drop all tables and recreate"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database reset successfully!")


def get_session():
    """Get a database session"""
    return SessionLocal()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "init":
            init_db()
        elif command == "reset":
            reset_db()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: init, reset")
    else:
        print("Database management utility")
        print("Usage: python manage_db.py [command]")
        print("Commands:")
        print("  init  - Initialize database (create tables)")
        print("  reset - Reset database (drop and recreate tables)")
