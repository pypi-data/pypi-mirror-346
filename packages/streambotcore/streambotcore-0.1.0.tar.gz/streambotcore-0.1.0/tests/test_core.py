# tests/test_core.py

import pytest
from streambotcore import StreamBot

def test_invalid_bot_type():
    with pytest.raises(ValueError):
        StreamBot(bot_type='invalid', token='dummy')
