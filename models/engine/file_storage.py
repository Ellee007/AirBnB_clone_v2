#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage if cls
        is None else, returns a dict of models class name as cls

        Args:
            cls: Class name
        """
        cls_dict = {}
        if cls:
            for k, v in self.__objects.items():
                if cls.__name__ == v.to_dict()['__class__']:
                    cls_dict.update({k: v})
            return cls_dict

        else:
            return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__objects.update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w') as f:
            temp = {}
            temp.update(self.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            temp = {}
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ Deletes an obj from __objects """
        if obj:
            for k, v in FileStorage. __objects.items():
                if obj == v:
                    del FileStorage.__objects[k]
                    break

            self.save()

    def close(self):
        """Deserializing json file to objects"""
        self.reload()