from sqlalchemy import Boolean, TIMESTAMP, text, String, Integer, Column

from app.db.base import Base

class Post(Base):
    __tablename__  = "posts"

    id= Column(Integer, primary_key=True, nullable=False)
    title= Column(String, nullable=False)
    description = Column(String, nullable = False)
    is_published = Column(Boolean, nullable = False, server_default=text('true'))
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False, 
        server_default=text('NOW()')
    )
class User(Base):
    __tablename__ = "users"

    id  = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False )
    name  = Column(String, nullable=False)
    job  = Column(String, nullable=False, server_default=text("'Nothing'"))
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('NOW()')
    ) 