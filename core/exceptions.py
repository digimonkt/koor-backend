class UserNotPassed(Exception):
    '''
    Inherited from the Base `Exception` class. 
    User object must be passed to .save() method. If not received we can raise this UserNotPassed

    '''
    def __init__(self, f, *args):
        super().__init__(args)

    def __str__(self):
        return f'User object is missing with the save method.'