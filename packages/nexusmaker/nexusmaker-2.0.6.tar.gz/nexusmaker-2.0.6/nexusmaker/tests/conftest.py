from pathlib import Path

import pytest
from nexusmaker import Record
from nexusmaker import NexusMaker
from nexusmaker import NexusMakerAscertained
from nexusmaker import NexusMakerAscertainedParameters


@pytest.fixture
def test_dir():
    return Path(__file__).parent


@pytest.fixture(scope='class')
def testdata():
    return [
        Record(ID=1, Language="A", Parameter="eye", Item="", Cognacy="1", Loan=None),
        Record(ID=2, Language="A", Parameter="leg", Item="", Cognacy="1", Loan=None),
        Record(ID=3, Language="A", Parameter="arm", Item="", Cognacy="1", Loan=None),

        Record(ID=4, Language="B", Parameter="eye", Item="", Cognacy="1", Loan=None),
        Record(ID=5, Language="B", Parameter="leg", Item="", Cognacy="2", Loan=None),
        Record(ID=6, Language="B", Parameter="arm", Item="", Cognacy="2", Loan=None),

        Record(ID=7, Language="C", Parameter="eye", Item="", Cognacy="1", Loan=None),
        # No Record for C 'leg'
        Record(ID=8, Language="C", Parameter="arm", Item="", Cognacy="3", Loan=None),

        Record(ID=9, Language="D", Parameter="eye", Item="<LOANWORD>", Cognacy="1",
               Loan=True),
        Record(ID=10, Language="D", Parameter="leg", Item="", Cognacy="1", Loan=None),
        Record(ID=11, Language="D", Parameter="leg", Item="", Cognacy="2", Loan=None),
        Record(ID=12, Language="D", Parameter="arm", Item="", Cognacy="2,3", Loan=None),
    ]


@pytest.fixture(scope='class')
def nexusmaker(testdata):
    return NexusMaker(data=testdata, remove_loans=True)


@pytest.fixture(scope='class')
def nexusmakerasc(testdata):
    return NexusMakerAscertained(data=testdata, remove_loans=True)


@pytest.fixture(scope='class')
def nexusmakerascparameters(testdata):
    return NexusMakerAscertainedParameters(data=testdata, remove_loans=True)
