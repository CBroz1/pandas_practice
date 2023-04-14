import os
import sys
import pytest
import logging
from contextlib import nullcontext
from pandas_practice import import_tools

# ---------------------- CONSTANTS ---------------------

data_src = "data"
data_csv = f"{data_src}/survey_results_public.csv"
data_schema = f"{data_src}/survey_results_schema.csv"


def pytest_addoption(parser):
    """
    Permit constants when calling pytest at commandline e.g., pytest --my-verbose False

    Parameters
    ----------
    --my-verbose (bool):  Default True. Pass print statements from Elements.
    --my-teardown (bool): Default True. Delete pipeline on close.
    --my-datadir (str):  Default ./tests/user_data. Relative path of test CSV data.
    """
    parser.addoption(
        "--my-verbose",
        action="store",
        default="True",
        help="Verbose for items: True or False",
        choices=("True", "False"),
    )
    parser.addoption(
        "--my-teardown",
        action="store",
        default="True",
        help="Verbose for items: True or False",
        choices=("True", "False"),
    )


@pytest.fixture(scope="session")
def setup(request):
    """Take passed commandline variables, set as global"""
    global verbose, _tear_down, verbose_context

    verbose = str_to_bool(request.config.getoption("--my-verbose"))
    _tear_down = str_to_bool(request.config.getoption("--my-teardown"))

    if not verbose:
        logging.getLogger("pandas").setLevel(logging.CRITICAL)

    verbose_context = nullcontext() if verbose else QuietStdOut()

    yield verbose_context, _tear_down


# ------------------ GENERAL FUCNTION ------------------


def str_to_bool(value) -> bool:
    """Return whether the provided string represents true. Otherwise false.
    Args:
        value (any): Any input
    Returns:
        bool (bool): True if value in ("y", "yes", "t", "true", "on", "1")
    """
    # Due to distutils equivalent depreciation in 3.10
    # Adopted from github.com/PostHog/posthog/blob/master/posthog/utils.py
    if not value:
        return False
    return str(value).lower() in ("y", "yes", "t", "true", "on", "1")


def write_csv(path, content):
    """
    General function for writing strings to lines in CSV
    :param path: pathlib PosixPath
    :param content: list of strings, each as row of CSV
    """
    with open(path, "w") as f:
        for line in content:
            f.write(line + "\n")


class QuietStdOut:
    """If verbose set to false, used to quiet tear_down table.delete prints"""

    def __enter__(self):
        os.environ["LOG_LEVEL"] = "WARNING"
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.environ["LOG_LEVEL"] = "INFO"
        sys.stdout.close()
        sys.stdout = self._original_stdout


# ------------------- FIXTURES -------------------


@pytest.fixture(scope="session")
def example_session_scope(setup):
    """Any default objects"""
    verbose_context, _ = setup


@pytest.fixture()
def ingest_data(example_session_scope):
    """Any specific fixtures"""

    yield import_tools.import_csv(csv_fp=data_csv)

    if _tear_down:
        pass
