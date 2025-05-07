from nexusmaker import Record


def test_simple():
    r = Record(
        ID=1, Parameter_ID=2, Language_ID=3,
        Language='English', Parameter='Hand', Item='hand',
        Annotation='?', Cognacy=None, Loan="L"
    )
    assert r.ID == 1
    assert r.Parameter_ID == 2
    assert r.Language_ID == 3
    assert r.Language == 'English'
    assert r.Parameter == 'Hand'
    assert r.Item == 'hand'
    assert r.Annotation == '?'
    assert r.Loan == "L"
    assert r.Cognacy is None
    assert r.get_taxon() == 'English_3'
    
    assert repr(r).startswith("<Record")



def test_is_loan():
    # not loans
    assert not Record(Loan="").is_loan
    assert not Record(Loan=None).is_loan
    assert not Record(Loan=False).is_loan
    assert not Record(Loan="false").is_loan
    assert not Record(Loan="False").is_loan
    # loans
    assert Record(Loan="L").is_loan
    assert Record(Loan="English").is_loan
    assert Record(Loan=True).is_loan
    assert Record(Loan="B").is_loan
    assert Record(Loan="S").is_loan
    assert Record(Loan="X").is_loan
    assert Record(Loan="x").is_loan


def test_get_taxon():
    # language_ID is numeric => <language>_<id>
    r = Record(
        ID=1, Parameter_ID=2, Language_ID=3,
        Language='English', Parameter='Hand', Item='hand',
        Annotation='?', Cognacy=None, Loan="L"
    )
    assert r.get_taxon() == "English_3"
    # language_ID is missing => <language>
    r = Record(
        ID=1, Parameter_ID=2, Language_ID=None,
        Language='English', Parameter='Hand', Item='hand',
        Annotation='?', Cognacy=None, Loan="L"
    )
    assert r.get_taxon() == "English"
    # language_ID is not integer => <language_id>
    r = Record(
        ID=1, Parameter_ID=2, Language_ID="MyLanguage",
        Language='English', Parameter='Hand', Item='hand',
        Annotation='?', Cognacy=None, Loan="L"
    )
    assert r.get_taxon() == "MyLanguage"
    