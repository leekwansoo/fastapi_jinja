from sqlalchemy import Column, Integer, String, Boolean,Date, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Image(Base):
    id = Column(Integer,primary_key = True, index=True)
    title = Column(String,nullable= False)
    image_url = Column(String)
    location = Column(String,nullable = False)
    description = Column(String,nullable=False)
    date_posted = Column(Date)
    owner =  Column(Integer,ForeignKey("user.id"))
    