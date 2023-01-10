

class File:


    def __init__(self, basename, extension, last_mod):

        self.__basename = basename
        self.__ext = extension
        self.__last_mod = last_mod


    def __repr__(self):
        return self.basename + self.ext

    
    def __str__(self):
        return self.basename + self.ext
        
    
    @property
    def basename(self):
        return self.__basename


    @property
    def ext(self):
        return self.__ext


    @property
    def last_mod(self):
        return self.__last_mod