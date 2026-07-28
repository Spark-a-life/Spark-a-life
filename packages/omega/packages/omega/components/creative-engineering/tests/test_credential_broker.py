import pytest
from wisegen_creative_engineering.credential_broker.broker import CredentialBroker


def test_broker_issues_scoped_token():
    broker = CredentialBroker({'external_generation': ['prompt_submit']})
    token = broker.request('media_router', 'external_generation', ['prompt_submit'])
    assert token.tool == 'external_generation'
    assert not token.is_expired()


def test_broker_rejects_excess_scope():
    broker = CredentialBroker({'external_generation': ['prompt_submit']})
    with pytest.raises(PermissionError):
        broker.request('media_router', 'external_generation', ['publish'])
