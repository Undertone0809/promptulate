import tiktoken


def num_tokens_from_string(string: str, model="gpt-3.5-turbo-0613") -> int:
    """Returns the number of tokens in a text string based on the specified model's
    encoding."""
    try:
        encoding = tiktoken.encoding_for_model(
            model
        )  # Attempt to get encoding for the specified model
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding(
            "cl100k_base"
        )  # Fallback encoding if model's encoding not found

    num_tokens = len(
        encoding.encode(string, disallowed_special=())
    )  # Calculate number of
    # tokens based on encoding
    return num_tokens


def num_messages(messages: dict, model="gpt-3.5-turbo-0613") -> int:
    """Returns the number of tokens in a chat message based on the specified model's
    encoding."""
    num_tokens = 0
    for msg in messages:
        num_tokens += num_tokens_from_string(msg["content"], model=model)
    return num_tokens
