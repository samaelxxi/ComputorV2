"""Variable class implementation"""


class Variable:
    """
    Variable class
    """
    def __init__(self, name: str, val=None):
        """
        :param name: name of variable(would be lowercased)
        :param val: variable value(None by default)
        """
        self.name = name.lower()
        self.val = val

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        if self.val is not None:
            return "{} = {}".format(self.name, self.val)
        else:
            return self.name

    def __hash__(self):
        return hash(self.name)

    __repr__ = __str__
