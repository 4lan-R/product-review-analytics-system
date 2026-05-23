"""Database management utilities"""
from database import engine, Base, SessionLocal
from models import Review
from alembic.config import Config
from alembic import command
import os


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


def get_alembic_config():
    """Get Alembic configuration"""
    config = Config("alembic.ini")
    return config


def migrate_upgrade(revision="head"):
    """Run database migrations"""
    config = get_alembic_config()
    command.upgrade(config, revision)
    print(f"Database upgraded to revision: {revision}")


def migrate_downgrade(revision):
    """Downgrade database to a specific revision"""
    config = get_alembic_config()
    command.downgrade(config, revision)
    print(f"Database downgraded to revision: {revision}")


def migrate_current():
    """Show current database revision"""
    config = get_alembic_config()
    command.current(config)


def migrate_history():
    """Show migration history"""
    config = get_alembic_config()
    command.history(config)


def migrate_create(message):
    """Create a new migration"""
    config = get_alembic_config()
    command.revision(config, autogenerate=True, message=message)
    print(f"Migration created: {message}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command_name = sys.argv[1]
        if command_name == "init":
            init_db()
        elif command_name == "reset":
            reset_db()
        elif command_name == "migrate":
            revision = sys.argv[2] if len(sys.argv) > 2 else "head"
            migrate_upgrade(revision)
        elif command_name == "downgrade":
            if len(sys.argv) < 3:
                print("Usage: python manage_db.py downgrade <revision>")
                sys.exit(1)
            migrate_downgrade(sys.argv[2])
        elif command_name == "current":
            migrate_current()
        elif command_name == "history":
            migrate_history()
        elif command_name == "create":
            if len(sys.argv) < 3:
                print("Usage: python manage_db.py create '<message>'")
                sys.exit(1)
            migrate_create(sys.argv[2])
        else:
            print(f"Unknown command: {command_name}")
            print_usage()
    else:
        print_usage()


def print_usage():
    print("Database management utility")
    print("Usage: python manage_db.py [command] [args]")
    print("\nCommands:")
    print("  init                    - Initialize database (create tables)")
    print("  reset                   - Reset database (drop and recreate tables)")
    print("  migrate [revision]      - Run migrations to revision (default: head)")
    print("  downgrade <revision>    - Downgrade to specific revision")
    print("  current                 - Show current database revision")
    print("  history                 - Show migration history")
    print("  create '<message>'      - Create new migration with autogenerate")

