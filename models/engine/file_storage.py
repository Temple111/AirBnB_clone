#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel



class FileStorage:
    """Represent an abstracted storage engine.
    Attributes:
        __file_path (str): The name of the file to save objects to.
       __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        d_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(d_name, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        nw_dict1 = FileStorage.__objects
        obj_dict1 = {obj: nw_dict1[obj].to_dict() for obj in nw_dict1.keys()}
        with open(FileStorage.__file_path, "w") as fp:
            json.dump(obj_dict1, fp)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as fp:
                obj_dict1 = json.load(fp)
                for q in obj_dict1.values():
                    cl_name1 = q["__class__"]
                    del q["__class__"]
                    self.new(eval(cl_name1)(**q))
        except FileNotFoundError:
            return
