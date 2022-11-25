
class WebgooseException(Exception):

    def __init__(self, exception_name="WebgooseException", message="There Was An Error Building The Site - No Cause Available"):
        self._name = exception_name
        self._message = message


    def __str__(self):
        return self.message

    
    @property
    def name(self):
        return self.name


    @property
    def message(self) -> str:
        return self.message

