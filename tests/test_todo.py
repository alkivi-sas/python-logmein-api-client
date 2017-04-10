from logmeinapi import client as logmein


def test_connexion():
    """Test that using a false credentials."""
    client = logmein.Client(company_id='12345', psk='fake')
    response = client.test()
    assert 'success' in response
    assert not response['success']


def test_todo():
    assert 'toto'.capitalize() == 'Toto'
