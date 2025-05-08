# Chatfic Validator

## Description

The Chatfic Validator is a Python package for validating chatfic data. It checks the format and structure of chatfic data to ensure it conforms to the specified schema.

## Installation

To install the Chatfic Validator, you can use pip:

```bash
pip install chatfic-validator
```

## Usage

Here's an example of how to use the Chatfic Validator:

```python
from chatfic_validator import ChatficValidator as validator

# Load the chatfic data from a file
with open('storybasic.json', 'r', encoding="utf-8") as file:
    json_text = file.read()

# Validate the chatfic data
result = validator.validate_json_text(
    json_text=json_text,
    chatfic_format=ChatficFormat.BASIC_JSON,
    multimedia_list=["time.jpeg"]
)

# Check if the validation was successful
if result.is_valid:
    print("Chatfic data is valid!")
else:
    print("Chatfic data is invalid.")
    for error in result.errors:
        print(error)
for warning in result.warnings:
    print(warning)
```

`ChatficFormat` enums: BASIC_JSON and COMPILED_JSON. These represent the storybasic.json and story.json file contents, respectively.

The `multimedia_list` parameter takes a list of the multimedia files that are expected to referenced within the story data.

`validate_json_text` method returns a `ChatficValidationResult` instance with 3 attributes:

is_valid:bool

errors: List[ChatficValidationError]

warnings: List[str]

`validate_json_text` method loads json text and runs `validate_dict` method. This second method can be used directly with the same parameters (chatfic_format and multimedia_list)

More information about the chatfic-format can be found here:

[https://gokhanmeteerturk.github.io/chatfic-format/](https://gokhanmeteerturk.github.io/chatfic-format/)
