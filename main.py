import pickle
import os
from helpers import file_delete, file_write, obj_query

# Specific function imports
from advanced_query import advanced_query

class db:
    def __init__(self):
        #lists all things in the directory
        arr = os.listdir()
        self.db = {}
        if 'data.dict' in arr:
            self.file = open('data.dict', "rb+")
            if os.path.getsize("data.dict")==0:
                self.db = {}
            else:
                self.db = pickle.load(self.file)
        else:
            self.file = open("data.dict", "wb") 
    def __setname__(self, name):
        self.name = name    
    #To add an object
    def add(self, obj):
        self.obj = obj
        try:
            if self.name:
                self.db[self.obj] = {}
                #goes to the beginning of the file, deletes everything, and rewrites the file
                self.file.seek(0)
                self.file.truncate()
                pickle.dump(self.db, self.file)
        #gets rid of attributeerror saying name doesn't exist
        except AttributeError:
            print("Name not set, set with __setname__.")
    def remove_key(self, remove_path):
        #removes 
        #db.obj.key
        self.remove_path = remove_path
        ar = self.remove_path.split('.')
        try:
            if self.name:
                o = ar[1]
                ke = ar[2]
                try:
                    del self.db[o][ke]
                    print("Sucessfully removed from {}.".format(self.name))
                    file_delete(self.file)
                    file_write(self.db, self.file)
                except KeyError:
                    print("Key (or object) doesn't exist in {}.".format(self.name))
        except AttributeError:
            print("Name not set, set with __setname__")
    def remove_obj(self, remove_path_2):
        """
        removing an object is very simple in easy.db, all you have to do is provide the remove_path, which consists of db.obj
        """
        self.remove_path_2 = remove_path_2
        ar = self.remove_path_2.split(".")
        ob = ar[1]
        try:
            del self.db[ob]
            file_delete(self.file)
            file_write(self.db, self.file)

        except KeyError:
            print("Object doesn't exist in {}.".format(self.name))

    def set_var(self, path, var):
        #format:  path = "var"
        #path = db.obj.var = value
        #path = key, var = value
        try:
            self.name
            self.path = path
            self.var = var
            ar = self.path.split(".")
            #ar[1] is obj, ar[2] is var       
            get_obj = ar[1]         
            var_insert = ar[2]
            if (get_obj not in self.db):
                print("Object not found in {}, set it.". format(self.name))
                return
            self.file.seek(0)
            self.file.truncate()
            self.db[get_obj][var_insert] = self.var
            pickle.dump(self.db, self.file)
            print("Sucessfully inserted into the database {}.".format(self.name))
        
        except AttributeError:
            print("Name not set, set with __setname__.")
    def query(self, *args):
    #obj = db.obj or db.obj.key
        ar = [arg for arg in args]

        if len(ar)>=2:
            results = self.adv_query(ar)
            return results
        if len(ar)<1:
            print("Pass in correct number of arguments!")
            return
        else:
            if len(ar[0].split(".")) == 2:
                return obj_query(self.db, ar[0]) 
            elif len(ar[0].split(".")) == 3:
                print("not implemented")

    def adv_query(self, args):
        results = advanced_query(args, self.db)
        return results
    
    def all(self):
        return self.db