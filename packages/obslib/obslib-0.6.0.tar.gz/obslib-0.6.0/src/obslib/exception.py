
class OBSValidationException(Exception):
    """
    Validation failed for a passed argument
    """
    pass

class OBSRecursionLimitException(Exception):
    """
    A recursive process reached maximum depth and aborted
    """
    pass

class OBSInternalException(Exception):
    """
    An internal error happened within an OBS function
    """
    pass

class OBSConversionException(Exception):
    """
    A value could not be converted to a target type
    """
    pass

class OBSResolveException(Exception):
    """
    Unable to resolve a variable reference
    """
    pass

