
class J2JSyntaxError(RuntimeError):
    """
    J2JSyntaxError Error in mini-language source
    """


class J2JInterpreterException (Exception):
    pass

class J2JCodeEmitterException (Exception):
    pass

class J2JFillException (Exception):
    """
    J2JFillException Reference to unbound variable during a fill operation
    """

class J2JPurityException (Exception):
    pass
