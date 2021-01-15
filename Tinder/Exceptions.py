class MyError(Exception):
    def __init__(self, message, error):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.error = error


class FBAuthError(MyError):
    pass

class TinderAuthError(MyError):
    pass

class TinderGetMatchesError(MyError):
    pass

class TinderGetRecsError(MyError):
    pass

class TinderLikeError(MyError):
    pass

class TinderPassError(MyError):
    pass