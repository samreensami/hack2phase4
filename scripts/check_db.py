import sys
from sqlmodel import Session, select
from backend.core.database import get_session, init_db
from backend.models import User

def check_connection():
    """
    Establishes a database connection and performs a simple query.
    """
    print("Attempting to connect to the database...")
    try:
        # The get_session function is a generator, so we need to iterate it
        session: Session = next(get_session())
        print("Database session obtained successfully.")
        
        # Perform a simple query to verify the connection and table access
        print("Querying for one user...")
        user = session.exec(select(User).limit(1)).first()
        
        if user:
            print(f"✅ Success! Connected to the database and found a user: {user.email}")
        else:
            # This is not necessarily an error; the table could be empty.
            print("✅ Success! Connected to the database, but the 'user' table is empty.")

    except Exception as e:
        print(f"❌ Failure! An error occurred while connecting to the database.")
        print(f"Error details: {e}")
        # Add a specific hint for the most common issue
        if "fe_sendauth" in str(e) or "password authentication failed" in str(e):
            print("\nHint: This often means the DATABASE_URL in your .env file is incorrect or the credentials are wrong.")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure the backend directory is in the python path
    # This is a bit of a hack to make the script runnable from the root directory
    sys.path.append('backend')
    
    # We need to re-import after modifying the path
    from backend.core.database import get_session, init_db
    from backend.models import User

    check_connection()