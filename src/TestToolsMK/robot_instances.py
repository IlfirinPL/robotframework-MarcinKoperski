from Selenium2Library import Selenium2Library
from robot.libraries import DateTime
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.libraries.OperatingSystem import OperatingSystem

__all__ = ('s2l', 'bi', 'dtl', 'osl', 'cl')


def s2l():
    """

        :rtype : Selenium2Library
        """
    s2l_instance = BuiltIn().get_library_instance('Selenium2Library')
    assert isinstance(s2l_instance, Selenium2Library)
    return s2l_instance


def bi():
    """

        :rtype : BuiltIn
        """
    bi_instance = BuiltIn().get_library_instance('BuiltIn')
    assert isinstance(bi_instance, BuiltIn)
    return bi_instance


def dtl():
    """

        :rtype : DateTime
        """
    dt_instance = BuiltIn().get_library_instance('DateTime')
    assert isinstance(dt_instance, DateTime)
    return dt_instance


def osl():
    """

        :rtype : OperatingSystem
        """
    os_instance = BuiltIn().get_library_instance('OperatingSystem')
    assert isinstance(os_instance, OperatingSystem)
    return os_instance


def cl():
    """

        :rtype : Collections
        """
    c_instance = BuiltIn().get_library_instance('Collections')
    assert isinstance(c_instance, Collections)
    return c_instance
