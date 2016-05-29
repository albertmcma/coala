"""
Module description.

Some more foobar-like text.
"""

def foobar_explosion(radius):
    """
    A nice and neat way of documenting code.
    :param radius: The explosion radius.
    """
    def get_55():
        """
        A function that returns 55.
        """
        return 55
    return get_55() * radius

"""
Docstring with layouted text.

    layouts inside docs are preserved for these documentation styles.
this is intended.
"""

""" Docstring directly besides triple quotes.
    Continues here. """


## Alternate documentation style in doxygen.
#  Subtext
# More subtext (not correctly aligned)
#      sub-sub-text
#

def best_docstring(param1, param2, param3):
    """
    This is the best docstring ever!

    :param param1:
        Very Very Long Parameter description.
    :param param2:
        Short Param description.

    :return: Long Return Description That Makes No Sense And Will
             Cut to the Next Line.
    """
    return None
