#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg_1):
    curl_brac = re.search(r"\{(.*?)\}", arg_1)
    sq_brac = re.search(r"\[(.*?)\]", arg_1)
    if curl_brac is None:
        if sq_brac is None:
            return [q.strip(",") for q in split(arg_1)]
        else:
            le = split(arg_1[:sq_brac.span()[0]])
            rel = [q.strip(",") for q in le]
            rel.append(sq_brac.group())
            return rel
    else:
        le = split(arg_1[:curl_brac.span()[0]])
        rel = [q.strip(",") for q in le]
        rel.append(curl_brac.group())
        return rel


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg_1):
        """Default behavior for cmd module when input is invalid"""
        argdict_1 = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        equal = re.search(r"\.", arg_1)
        if equal is not None:
            argle = [arg_1[:equal.span()[0]], arg_1[equal.span()[1]:]]
            equal = re.search(r"\((.*?)\)", argle[1])
            if equal is not None:
                command_0 = [argle[1][:equal.span()[0]], equal.group()[1:-1]]
                if command_0[0] in argdict_1.keys():
                    call_0 = "{} {}".format(argle[0], command_0[1])
                    return argdict_1[command_0[0]](call_0)
        print("*** Unknown syntax: {}".format(arg_1))
        return False

    def do_quit(self, arg_0):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg_0):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg_0):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        argle = parse(arg_0)
        if len(argle) == 0:
            print("** class name missing **")
        elif argle[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argle[0])().id)
            storage.save()

    def do_show(self, arg_0):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        argle = parse(arg_0)
        objdict_1 = storage.all()
        if len(argle) == 0:
            print("** class name missing **")
        elif argle[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argle) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argle[0], argle[1]) not in objdict_1:
            print("** no instance found **")
        else:
            print(objdict_1["{}.{}".format(argle[0], argle[1])])

    def do_destroy(self, arg_0):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        argle = parse(arg_0)
        objdict_1 = storage.all()
        if len(argle) == 0:
            print("** class name missing **")
        elif argle[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argle) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argle[0], argle[1]) not in objdict_1.keys():
            print("** no instance found **")
        else:
            del objdict_1["{}.{}".format(argle[0], argle[1])]
            storage.save()

    def do_all(self, arg_0):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argle = parse(arg_0)
        if len(argle) > 0 and argle[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objle = []
            for obj1 in storage.all().values():
                if len(argle) > 0 and argle[0] == obj1.__class__.__name__:
                    objle.append(obj1.__str__())
                elif len(argle) == 0:
                    objle.append(obj1.__str__())
            print(objle)

    def do_count(self, arg_0):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argle = parse(arg_0)
        countl = 0
        for obj1 in storage.all().values():
            if argle[0] == obj1.__class__.__name__:
                countl += 1
        print(countl)

    def do_update(self, arg_0):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argle = parse(arg_0)
        obj_dict = storage.all()

        if len(argle) == 0:
            print("** class name missing **")
            return False
        if argle[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argle) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argle[0], argle[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(argle) == 2:
            print("** attribute name missing **")
            return False
        if len(argle) == 3:
            try:
                type(eval(argle[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argle) == 4:
            obj1 = obj_dict["{}.{}".format(argle[0], argle[1])]
            if argle[2] in obj1.__class__.__dict__.keys():
                val_type = type(obj1.__class__.__dict__[argle[2]])
                obj1.__dict__[argle[2]] = val_type(argle[3])
            else:
                obj1.__dict__[argle[2]] = argle[3]
        elif type(eval(argle[2])) == dict:
            obj1 = obj_dict["{}.{}".format(argle[0], argle[1])]
            for z, f in eval(argle[2]).items():
                if (z in obj1.__class__.__dict__.keys() and
                        type(obj1.__class__.__dict__[z]) in {str, int, float}):
                    val_type = type(obj1.__class__.__dict__[z])
                    obj1.__dict__[z] = val_type(f)
                else:
                    obj1.__dict__[z] = f
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
