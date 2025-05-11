class BaseObject(object):

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {str(self)}>"