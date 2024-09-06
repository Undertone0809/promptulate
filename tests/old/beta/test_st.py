from unittest.mock import MagicMock, patch

import pytest

from promptulate.beta.st.sidebar import ModelConfig, model_sidebar


@pytest.fixture
def mock_streamlit():
    with patch("promptulate.beta.st.sidebar.streamlit", create=True) as mock_st:
        mock_st.sidebar = MagicMock()
        mock_st.selectbox.return_value = "openai/gpt-4o"
        mock_st.text_input.side_effect = ["test_api_key", "test_api_base"]
        yield mock_st


def test_model_sidebar(mock_streamlit):
    # Test with default model options
    config = model_sidebar()
    assert isinstance(config, ModelConfig)
    assert config.model_name == ""
    assert config.api_key == ""
    assert config.api_base == ""
