from app.db.base import SessionLocal, Base, engine


def get_db():
    db = SessionLocal()
    try:
        yield db    #Give db to the route (endpoint function) pause this function
    finally:
        db.close()   #after req is done  resume func close this session 