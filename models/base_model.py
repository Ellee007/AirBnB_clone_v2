#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from models import storage_type

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models

    Args:
        id (sqlalchemy string): unique id of basemodel
        created_at (sqlalchemy string): Time model was created
        updated_at (sqlalchmey string): Time model was last updated
    """
    id = Column(String(60),
                primary_key=True,
                unique=True,
                nullable=False)
    created_at = Column(DateTime,
                        nullable=False,
                        default=datetime.utcnow())

    updated_at = Column(DateTime,
                        nullable=False,
                        default=datetime.utcnow())
    """else:
        id = ''
        created_at = ''
        updated_at = ''"""

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for k in kwargs:
                if k in ['created_at', 'updated_at']:
                    setattr(self, k, datetime.fromisoformat(kwargs[k]))
                elif k != '__class__':
                    setattr(self, k, kwargs[k])
            # if storage_type == 'db':
                if not hasattr(kwargs, 'id'):
                    setattr(self, 'id', str(uuid.uuid4()))
                if not hasattr(kwargs, 'created_at'):
                    setattr(self, 'updated_at', datetime.now())
                if not hasattr(kwargs, 'updated_at'):
                    setattr(self, 'updated_at', datetime.now())

    def __str__(self):
        """Returns a string representation of the instance"""
        dct = self.__dict__.copy()
        if '_sa_instance_state' in dct.keys():
            del dct['_sa_instance_state']
        return '[{}] ({}) {}'.format(
            self.__class__.__name__, self.id, dct)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        # dictionary['created_at'] = self.created_at.isoformat()
        # dictionary['updated_at'] = self.updated_at.isoformat()

        for k in dictionary:
            if type(dictionary[k]) is datetime:
                dictionary[k] = dictionary[k].isoformat()
        if '_sa_instance_state' in dictionary.keys():
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """ Deletes current instance from storage """
        from models import storage
        storage.delete(self)
