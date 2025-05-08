from chatfic_validator import ChatficValidator, ChatficFormat


def test_input_valid_basic_one_page():
    # Load the valid JSON text from the test file
    with open('./tests/files/test_input_valid_basic_one_page.json', encoding='utf-8') as file:
        json_text = file.read()


    validator = ChatficValidator()

    result = validator.validate_json_text(json_text,
                                          ChatficFormat.BASIC_JSON,
                                          ["time.jpeg"])

    print(result.errors)

    assert result.is_valid is True
    assert len(result.errors) == 0
    assert result.warnings == ["Make sure these fields in character are "
                               "expected 'eve': ['gender', 'skin', 'eyes', "
                               "'dress', 'hair']"]


def test_input_valid_compiled_one_page():
    # Load the valid JSON text from the test file
    with open('./tests/files/test_input_valid_compiled_one_page.json', encoding='utf-8') as file:
        json_text = file.read()

    validator = ChatficValidator()

    result = validator.validate_json_text(json_text,
                                          ChatficFormat.COMPILED_JSON,
                                          ["time.jpeg", "school.jpg"])


    assert result.is_valid is True
    assert len(result.errors) == 0
    assert result.warnings == ["Make sure these fields in character are "
                               "expected 'eve': ['gender', 'skin', 'eyes', "
                               "'dress', 'hair']"]


def test_input_invalid_basic_one_page():
    with open('./tests/files/test_input_invalid_basic_one_page.json', encoding='utf-8') as file:
        json_text = file.read()

    validator = ChatficValidator()

    result = validator.validate_json_text(json_text,
                                          ChatficFormat.BASIC_JSON,
                                          ["unknown.jpg"])

    expected_errors = [
        "Missing required field: author",
        "Missing required field: handles",
        "Missing required character 'player'",
        "Format should be 'chatficbasicjson', not 'chatficbasic'",
        "Pages should have an integer 'id' key",
        "Pages should have a string 'name' key",
        "Reference to unknown multimedia: time.jpeg",
        "There are messages with unknown 'side' values (only 0, 1 and 2 are allowed)",
        "There are messages missing required fields: ['from', 'side']"
    ]

    error_messages = [str(error) for error in result.errors]

    assert sorted(error_messages) == sorted(expected_errors)
    assert result.is_valid is False
    assert len(result.warnings) == 2
    assert sorted(result.warnings) == sorted(["Multimedia not used: unknown.jpg",
                                              "Make sure these fields in "
                                              "character are expected 'eve': "
                                              "['gender', 'skin', 'eyes', "
                                              "'dress', 'hair']"])


def test_input_invalid_compiled_one_page():
    with open(
            './tests/files/test_input_invalid_compiled_one_page.json', encoding='utf-8') as file:
        json_text = file.read()

    validator = ChatficValidator()

    result = validator.validate_json_text(json_text,
                                          ChatficFormat.COMPILED_JSON,
                                          ["unknown.jpg"])

    expected_errors = ["Missing message fields: ['messageindex']",
                       'Missing required field: chatFic.author',
                       'Missing required field: chatFic.description',
                       'Missing required field: chatFic.handles',
                       'Missing required field: chatFic.apps',
                       "Unknown multimedia: ['time.jpeg']",
                       'Unknown sides found: [4]']

    expected_warnings = ["Unknown fields found in 'chatFic': ['idk']",
                         'Unreachable message indexes: [5]',
                         "Unused characters: ['adam']",
                         "Unused multimedia: ['unknown.jpg']",
                         "Multimedia not used: unknown.jpg",
                         "Make sure these fields in character are expected "
                         "'eve': ['gender', 'skin', 'eyes', 'dress', 'hair']"]

    error_messages = [str(error) for error in result.errors]

    assert sorted(error_messages) == sorted(expected_errors)
    assert sorted(result.warnings) == sorted(expected_warnings)
    assert result.is_valid is False
    assert len(result.warnings) == 6


def test_input_valid_basic_three_pages():
    # Load the valid JSON text from the test file
    with open('./tests/files/test_input_valid_basic_three_pages.json', encoding='utf-8') as file:
        json_text = file.read()

    validator = ChatficValidator()

    result = validator.validate_json_text(json_text,
                                          ChatficFormat.BASIC_JSON,
                                          ["time.jpeg"])

    assert result.is_valid is True
    assert len(result.errors) == 0
    assert result.warnings == ["Make sure these fields in character are "
                               "expected 'eve': ['gender', 'skin', 'eyes', "
                               "'dress', 'hair']"]


def test_input_valid_compiled_three_pages():
    # Load the valid JSON text from the test file
    with open(
            './tests/files/test_input_valid_compiled_three_pages.json', encoding='utf-8') as file:
        json_text = file.read()

    validator = ChatficValidator()

    result = validator.validate_json_text(json_text,
                                          ChatficFormat.COMPILED_JSON,
                                          ["time.jpeg"])

    assert result.is_valid is True
    assert len(result.errors) == 0
    assert result.warnings == ["Make sure these fields in character are "
                               "expected 'eve': ['gender', 'skin', 'eyes', "
                               "'dress', 'hair']"]


def test_input_invalid_basic_three_pages():
    # Load the valid JSON text from the test file
    with open(
            './tests/files/test_input_invalid_basic_three_pages.json', encoding='utf-8') as file:
        json_text = file.read()

    validator = ChatficValidator()

    result = validator.validate_json_text(json_text,
                                          ChatficFormat.BASIC_JSON,
                                          ["time.jpeg"])

    expected_errors = ["Each option should have a 'to' key",
                       "Option with a 'to' value that points"
                       " to an unknown page id: 5"]

    expected_warnings = ["There is an option 'message' that will be ignored,"
                         " because there is only 1 option in that page.",
                                              "Make sure these fields in "
                                              "character are expected 'eve': "
                                              "['gender', 'skin', 'eyes', "
                                              "'dress', 'hair']"]

    error_messages = [str(error) for error in result.errors]

    assert sorted(error_messages) == sorted(expected_errors)
    assert sorted(result.warnings) == sorted(expected_warnings)
    assert result.is_valid is False


def test_input_invalid_compiled_three_pages():
    # Load the valid JSON text from the test file
    with open(
            './tests/files/test_input_invalid_compiled_three_pages.json', encoding='utf-8') as file:
        json_text = file.read()

    validator = ChatficValidator()

    result = validator.validate_json_text(json_text,
                                          ChatficFormat.COMPILED_JSON,
                                          ["time.jpeg"])

    expected_errors = ["Missing message fields:"
                       " ['options.text', 'options.to']",
                       'Unknown option targets: [11]']

    error_messages = [str(error) for error in result.errors]

    assert sorted(error_messages) == sorted(expected_errors)
    assert result.warnings == ["Make sure these fields in character are "
                               "expected 'eve': ['gender', 'skin', 'eyes', "
                               "'dress', 'hair']"]
    assert result.is_valid is False


def test_invalid_chatfic_format():
    # Create an instance of ChatficValidator
    validator = ChatficValidator()

    # Call the validate_json_text method with an invalid chatfic format
    result = validator.validate_json_text(
        "{}", "invalid_format", []
    )

    # Assert that the result is invalid
    assert result.is_valid is False
    assert len(result.errors) > 0
    assert len(result.warnings) == 0
