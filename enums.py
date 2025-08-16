"""
NAMESPACE for LLM clients
"""

from enum import Enum


class LLMClient(str, Enum):
    """
    Namespace for LLM clients
    """

    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class DocumentationFormat(str, Enum):
    """
    Namespace for documentation formats
    """

    MARKDOWN: str = "markdown"
    RST: str = "rst"
    NUMPY: str = "numpy"
    GOOGLE: str = "google"
    SPHINX: str = "sphinx"
    PLAIN: str = "plain"
    EPYTEXT: str = "epytext"


class DocumentationFormatExamples(str, Enum):
    """
    Namespace for documentation format examples.
    """

    MARKDOWN: str = """Short summary.

    ### Parameters
    - `arg1` (`int`): Description.
    - `arg2` (`str`): Description.

    ### Returns
    `bool`: Description.

    ### Raises
    `ValueError`: Reason.
    """

    RST: str = """Short summary.

    :param int arg1: Description.
    :param str arg2: Description.
    :returns: Description.
    :rtype: bool
    :raises ValueError: Reason.
    """

    NUMPY: str = """Short summary.

    Parameters
    ----------
    arg1 : int
        Description.
    arg2 : str
        Description.

    Returns
    -------
    bool
        Description.

    Raises
    ------
    ValueError
        Reason.
    """

    GOOGLE: str = """Short summary.

    Args:
        arg1 (int): Description.
        arg2 (str): Description.

    Returns:
        bool: Description.

    Raises:
        ValueError: Reason.
    """

    SPHINX: str = """Short summary.

    .. note::
       You can use Sphinx directives and roles here.

    :param arg1: Description.
    :type arg1: int
    :param arg2: Description.
    :type arg2: str
    :return: Description.
    :rtype: bool
    :raises ValueError: Reason.
    """

    PLAIN: str = """Short summary. This function takes two arguments.
    arg1 is an integer and arg2 is a string. It returns True on success.
    """

    EPYTEXT: str = """Short summary.

    @param arg1: Description.
    @type arg1: int
    @param arg2: Description.
    @type arg2: str
    @return: Description.
    @rtype: bool
    @raise ValueError: Reason.
    """
