#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from models.state import State
from models import storage_type
from sqlalchemy.orm import relationship
from models.place import Place


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'

    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        state_id = Column(
            String(60),
            ForeignKey('states.id'),
            nullable=False)
        places = relationship('Place',
                              backref='cities',
                              cascade='all, delete-orphan')
    else:
        name = ''
        state_id = ''