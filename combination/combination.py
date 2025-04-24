class Combination:
    """
    A class to represent a combination of strings.
    
    Attributes:
    - s : str
    - v : str
    - o : str"""

    def __init__(self, s=None, v=None, o=None):
        self.s = s if s is not None else ""
        self.v = v if v is not None else ""
        self.o = o if o is not None else ""

    def __repr__(self):
        return f" {self.s}{self.v}{self.o} "
