# Copyright (c) 2015 Cutting Edge QA Marcin Koperski
import os.path

from DatabaseLibrary import DatabaseLibrary
from SeleniumLibrary import SeleniumLibrary
from robot.libraries import DateTime
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.libraries.OperatingSystem import OperatingSystem
from robot.api import logger

__all__ = ('sl', 'bi', 'dtl', 'osl', 'cl', 'get_artifacts_dir')


def get_artifacts_dir(delta_path=""):
    output_path = bi().get_variable_value("${EXECDIR}")
    output_path += "/Artifacts/"
    output_path += delta_path
    output_path_normalized = validate_create_artifacts_dir(output_path)
    return output_path_normalized


def validate_create_artifacts_dir(path):
    """
    As input take path return normalized path,
    create directory for this path
    :param path:
    :return path_normalized:
    """
    output_dir_normalized = os.path.dirname(os.path.abspath(os.path.normpath(path)))
    output_path_normalized = os.path.abspath(os.path.normpath(path))
    if not os.path.exists(output_dir_normalized):
        os.makedirs(output_dir_normalized)
    return output_path_normalized


def sl():
    """
        :rtype : SeleniumLibrary
        """
    sl_instance = BuiltIn().get_library_instance('SeleniumLibrary')
    assert isinstance(sl_instance, SeleniumLibrary)
    return sl_instance


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


def dbl():
    """

        :rtype : DatabaseLibrary
        """
    c_instance = BuiltIn().get_library_instance('DatabaseLibrary')
    assert isinstance(c_instance, DatabaseLibrary)
    return c_instance


def ttmkl():
    """

        :rtype : TestToolsMK
        """
    c_instance = BuiltIn().get_library_instance('TestToolsMK')
    # assert isinstance(c_instance, TestToolsMK)
    return c_instance
