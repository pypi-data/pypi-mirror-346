import json
from typing import Union, List
from enum import Enum
from .result import ChatficValidationResult
from .error import ChatficValidationError


class ChatficFormat(Enum):
    COMPILED_JSON = 'chatficbasic'
    BASIC_JSON = 'chatficbasicjson'


class ChatficVersion(Enum):
    V0_9 = "0.9"
    V1 = "1"
    V1_1 = "1.1"

SUPPORTED_VERSIONS: List[str] = [v.value for v in ChatficVersion]
DEFAULT_VERSION: str = ChatficVersion.V1_1.value


class ChatficValidator:
    @staticmethod
    def validate(data: Union[str, dict],
                 chatfic_format: ChatficFormat,
                 multimedia_list: list = None) -> ChatficValidationResult:
        """

        :param chatfic_format: The chatfic format to validate against.
        :param data:  The JSON text or python dict to validate.
        :param multimedia_list: List of files WITHOUT the 'media/' prefix
        :return:
        """
        if multimedia_list is None:
            multimedia_list = []
        if isinstance(data, str):
            return ChatficValidator.validate_json_text(
                data,
                chatfic_format,
                multimedia_list
            )
        elif isinstance(data, dict):
            return ChatficValidator.validate_dict(
                data,
                chatfic_format,
                multimedia_list
            )
        else:
            raise ValueError(
                "Input data must be either a JSON text (str) or a dictionary "
                "(dict)")

    @staticmethod
    def validate_json_text(json_text: str,
                           chatfic_format: ChatficFormat,
                           multimedia_list: list) -> ChatficValidationResult:
        """
        Validate JSON text according to the specified chatfic format.

        Args:
            :param chatfic_format: The chatfic format to validate against.
            :param json_text:  The JSON text to validate.
            :param multimedia_list: List of files WITHOUT the 'media/' prefix

        Returns:
            :return: ChatficValidationResult: The validation result object.
        """
        # Perform validation logic for JSON text
        errors = []
        # Example validation logic for chatfic_format:
        if type(chatfic_format) is not ChatficFormat:
            errors.append(ChatficValidationError("Invalid chatfic format"))

        if errors:
            return ChatficValidationResult(is_valid=False, errors=errors,
                                           warnings=[])

        # parse json and if success, validate_dict:
        try:
            data_dict = json.loads(json_text)
            return ChatficValidator.validate_dict(
                data_dict,
                chatfic_format,
                multimedia_list
            )
        except json.JSONDecodeError as e:
            errors.append(ChatficValidationError(f"Invalid JSON: {e}"))

        # Construct validation result object
        is_valid = not errors
        return ChatficValidationResult(is_valid=is_valid, errors=errors,
                                       warnings=[])

    @staticmethod
    def validate_dict(data_dict: dict,
                      chatfic_format: ChatficFormat,
                      multimedia_list: list) -> ChatficValidationResult:
        """
        Validate a Python dictionary according to the specified chatfic format.

        Args:
            :param chatfic_format: The chatfic format to validate against.
            :param data_dict:   The dictionary to validate.
            :param multimedia_list: List of files WITHOUT the 'media/' prefix

        Returns:
            ChatficValidationResult: The validation result object.
        """
        # Perform validation logic for dictionary
        errors = []
        # Example validation logic for chatfic_format:
        if type(chatfic_format) is not ChatficFormat:
            errors.append(ChatficValidationError("Invalid chatfic format"))
            return ChatficValidationResult(is_valid=False, errors=errors,
                                           warnings=[])

        if chatfic_format == ChatficFormat.BASIC_JSON:
            return BasicChatficValidator.validate(data_dict, multimedia_list)

        if chatfic_format == ChatficFormat.COMPILED_JSON:
            return CompiledChatficValidator.validate(data_dict,
                                                     multimedia_list)

        raise ValueError("Invalid chatfic format")


class BaseChatficValidator:
    @staticmethod
    def checkConsecutive(lst: list) -> bool:
        return sorted(lst) == list(range(min(lst), max(lst) + 1))

    @staticmethod
    def validateCharacters(characters: dict) -> tuple:
        errors = []
        warnings = []

        character_slugs = set(characters.keys())
        for character, character_data in characters.items():
            character_keys = list(character_data.keys())
            if "name" not in character_keys:
                errors.append(
                    ChatficValidationError(
                        f"Missing required field 'name' in "
                        f"character '{character}'"
                    )
                )
            else:
                character_keys.remove("name")
            if "color" in character_keys:
                warnings.append("'color' attribute as a direct child of "
                                "character property is not recommended "
                                "as of chatfic-format v1.0.0")
                character_keys.remove("color")
            if "model" in character_keys:
                character_keys.remove("model")
            if character_keys:
                warnings.append(
                    f"Make sure these fields in character are expected "
                    f"'{character}': {character_keys}")
        if "player" not in characters:
            errors.append(
                ChatficValidationError(
                    "Missing required character 'player'"))
        # 2.2: Character model checks:
        for character, character_data in characters.items():
            if "model" in character_data:
                model = character_data["model"]
                if not isinstance(model, dict):
                    errors.append(ChatficValidationError(
                        f"Character '{character}' 'model' must be a dict"))
                else:
                    if "name" not in model:
                        errors.append(ChatficValidationError(
                            f"Character '{character}' 'model' must have a "
                            f"'name'"
                        ))

                    if "handles" in model:
                        if not isinstance(model["handles"],
                                          dict):
                            errors.append(ChatficValidationError(
                                f"Character '{character}' 'model' 'handles' "
                                f"must be a dict"
                            ))
                        else:
                            for handle, value in model["handles"].items():
                                if not isinstance(value, str):
                                    errors.append(ChatficValidationError(
                                        f"Character '{character}' 'model' "
                                        f"'handles' key '{handle}' must be a "
                                        f"string"
                                    ))

                    if set(model.keys()) - {"name", "handles"}:
                        errors.append(ChatficValidationError(
                            f"Character '{character}' 'model' should not "
                            f"have any keys other than 'name' or 'handles'"
                        ))

        return errors, warnings, character_slugs


class BasicChatficValidator(BaseChatficValidator):
    @staticmethod
    def validate(data: dict, multimedia_list: list) -> ChatficValidationResult:
        errors = []
        warnings = []

        # 1. Check Required Fields, and detect unnecessary fields:
        version = DEFAULT_VERSION
        if "version" in data:
            if data["version"] not in SUPPORTED_VERSIONS:
                errors.append(ChatficValidationError(
                    f"Unsupported version: {data["version"]}. Supported "
                    f"versions are: {SUPPORTED_VERSIONS}"))
            version = data["version"]
        else:
            warnings.append(
                f"Using default version: {version}. "
                f"Specifying a version is highly recommended.")

        required_fields = {
            "title": {"type": "str"},
            "description": {"type": "str"},
            "author": {"type": "str"},
            "episode": {"type": "int"},
            "characters": {"type": "dict"},
            "format": {"type": "str"},
            "pages": {"type": "list"},
            "handles": {"type": "dict"},
            "variables": {"type": "dict"},
        }

        for field, field_info in required_fields.items():
            if field not in data:
                errors.append(
                    ChatficValidationError(f"Missing required field: {field}"))
            else:
                # not a fan of E721
                if field_info["type"] != type(data[field]).__name__:
                    errors.append(ChatficValidationError(
                        f"Field '{field}' must be a {field_info['type']}"))
                else:
                    if field == "variables":
                        for variable, variable_data in data[
                            "variables"].items():
                            if not isinstance(variable_data, dict):
                                errors.append(ChatficValidationError(
                                    f"Variable '{variable}' must be a dict")
                                )
                            elif "value" not in variable_data:
                                errors.append(ChatficValidationError(
                                    f"Variable '{variable}' must have a "
                                    f"'value'")
                                )

        unused_multimedia = set(multimedia_list)
        bad_multimedia = []
        valid_apps = []
        if version == ChatficVersion.V1_1.value:
            if "apps" in data:
                if not isinstance(data["apps"], dict):
                    errors.append(ChatficValidationError(
                        f"'apps' should be an object with key-value pairs,"
                        f" not a '{type(data['apps'])}'"))
                else:
                    for app_key, app_value in data["apps"].items():
                        valid_apps.append(app_key)
                        if not isinstance(app_value, dict):
                            errors.append(ChatficValidationError(
                                f"The app '{app_key}' should be an object with"
                                f" key-value pairs, not a '{type(app_value)}'"))
                        else:
                            if "name" in app_value and not isinstance(app_value["name"],
                                                                str):
                                errors.append(ChatficValidationError(
                                    f"The app '{app_key}' has a name but it is"
                                    f" not a string"))
                            if "background" in app_value:
                                if not isinstance(app_value["background"], str):
                                    errors.append(ChatficValidationError(
                                        f"The app '{app_key}' has a background but"
                                        f" it is not a media link"))
                                if not app_value["background"].startswith(
                                        "media/") or app_value[
                                    "background"][6:] not in multimedia_list:
                                    bad_multimedia.append(app_value["background"])
                                else:
                                    unused_multimedia.discard(
                                        app_value["background"][6:])



        character_slugs = set()
        if "characters" in data and isinstance(data["characters"], dict):
            # 2. Validate character data:
            # 2.1: character keys check
            character_errors, character_warnings, character_slugs = BasicChatficValidator.validateCharacters(
                data["characters"])

            errors += character_errors
            warnings += character_warnings
        # 3. Validate format name:
        if "format" in data and data["format"] != "chatficbasicjson":
            errors.append(ChatficValidationError(f"Format should be "
                                                 f"'chatficbasicjson', "
                                                 f"not '{data['format']}'"))
        # 4. Validate pages:
        # 4.1 Pages length check
        if "pages" in data and len(data["pages"]) == 0:
            errors.append(ChatficValidationError("You need at least 1 page"))

        if "pages" in data:
            # 4.2 Page keys check
            unknown_character_slugs = []
            missing_required_message_fields = set()
            any_unknown_sides = False
            for page in data["pages"]:
                if "id" not in page or not isinstance(page["id"], int):
                    errors.append(ChatficValidationError(
                        f"Pages should have an integer 'id' key"))

                if "name" not in page or not isinstance(page["name"], str):
                    errors.append(ChatficValidationError(
                        f"Pages should have a string 'name' key"))

                if "messages" not in page or not isinstance(page["messages"],
                                                            list):
                    errors.append(ChatficValidationError(
                        f"Pages should have a 'messages' list"))

                # 4.3 Message checks
                required_message_fields = {
                    "message": {"type": "str", "nullable": False},
                    "from": {"type": "str", "nullable": False},
                    "multimedia": {"type": "str", "nullable": True},
                    "chatroom": {"type": "str", "nullable": False},
                }
                for message in page["messages"]:
                    message_keys = message.keys()
                    if version == ChatficVersion.V1_1.value:
                        if "app" in message_keys:
                            message_app = message["app"]
                            if message_app is not None and message_app != "chat" and message_app != "home":
                                if not isinstance(message_app, str):
                                    errors.append(ChatficValidationError(
                                        f"Message app should be a string"))
                                else:
                                    if not message_app in valid_apps:
                                        errors.append(
                                            ChatficValidationError(
                                            f"Message app '{message_app}' is"
                                            f" unknown. Options: {valid_apps}"
                                            )
                                        )
                        if "notification" in message_keys:
                            message_notification = message["notification"]
                            if not isinstance(
                                    message_notification, str):
                                errors.append(ChatficValidationError(
                                    f"Message notification should be a string")
                                )
                        if "type" in message_keys:
                            message_type = message["type"]
                            if not isinstance(
                                    message_type, str):
                                errors.append(ChatficValidationError(
                                    f"Message type should be a string")
                                )

                    if "side" not in message_keys:
                        if "type" not in message_keys or message["type"] != "thought" or version != ChatficVersion.V1_1.value:
                            missing_required_message_fields.add("side")
                    else:
                        if message["side"] is None:
                            if "type" not in message_keys or message["type"] != "thought" or version != ChatficVersion.V1_1.value:
                                any_unknown_sides = True
                        elif message["side"] not in [0, 1, 2, "0", "1", "2"]:
                            any_unknown_sides = True

                    for field, field_info in required_message_fields.items():
                        if field not in message_keys:
                            missing_required_message_fields.add(field)
                        elif (
                                field_info["type"] != type(
                            message[field]).__name__
                                and
                                not (
                                        field_info["nullable"] is True and
                                        message[field] is None
                                )
                        ):
                            errors.append(
                                ChatficValidationError(
                                    f"Message '{field}' must be "
                                    f"a {field_info['type']}"
                                )
                            )
                        if field == "from" and "from" in message and message[
                            "from"] not in character_slugs:
                            unknown_character_slugs.append(message["from"])
                        # TODO: CHECK UNUSED CHARACTER SLUGS FOR A WARNING
                        if field == "multimedia" and "multimedia" in message:
                            if message["multimedia"] is not None:
                                if not message["multimedia"].startswith(
                                        "media/") or message["multimedia"][
                                                     6:] not in multimedia_list:

                                    bad_multimedia.append(
                                        message["multimedia"])
                                elif message["multimedia"].startswith(
                                        "media/"):
                                    unused_multimedia.discard(
                                        message["multimedia"][6:])

            if unused_multimedia:
                for multimedia in sorted(unused_multimedia):
                    warnings.append("Multimedia not used: " + multimedia)
            if bad_multimedia:
                for multimedia in sorted(bad_multimedia):
                    errors.append(
                        ChatficValidationError(
                            "Reference to unknown multimedia: " + multimedia
                        )
                    )
            if any_unknown_sides:
                errors.append(ChatficValidationError(
                    "There are messages with unknown 'side' values (only 0, "
                    "1 and 2 are allowed)"
                ))
            if missing_required_message_fields:
                errors.append(ChatficValidationError(
                    f"There are messages missing required"
                    f" fields: {sorted(missing_required_message_fields)}"
                ))
            if unknown_character_slugs:
                errors.append(ChatficValidationError(
                    f"Messages have "
                    f"unknown 'from': {sorted(unknown_character_slugs)}"
                ))

            # 4.3 Page ids check
            page_ids = [page["id"] for page in data["pages"] if "id" in page]
            # detect and make a list of duplicate ids if any:
            seen_page_ids = set()
            duplicate_page_ids = set()

            for x in page_ids:
                if x in seen_page_ids:
                    duplicate_page_ids.add(x)
                else:
                    seen_page_ids.add(x)

            if duplicate_page_ids:
                errors.append(ChatficValidationError(
                    f"There are duplicate page ids: {duplicate_page_ids}"))

            page_ids = list(seen_page_ids)
            if (
                    len(page_ids) > 1 and
                    not BasicChatficValidator.checkConsecutive(page_ids)
            ):
                errors.append(ChatficValidationError(
                    "Page ids are not consecutive"
                ))

            page_ids_without_links = seen_page_ids.copy()
            # 4.4 Page option check
            for page in data["pages"]:
                if "options" not in page or not isinstance(page["options"],
                                                           list):
                    errors.append(ChatficValidationError(
                        "One page is missing 'option' key or it is not a list: " +
                        str(page)))
                else:
                    option_message_required = False
                    if len(page["options"]) > 1:
                        option_message_required = True
                    for option in page["options"]:
                        if option_message_required and "message" not in option:
                            errors.append(ChatficValidationError(
                                "A page with more than 1 options, should have a "
                                "'message' for each option."))
                        elif not option_message_required and "message" in option:
                            warnings.append(
                                "There is an option 'message' that "
                                "will be ignored, because there is "
                                "only 1 option in that page.")
                        if "to" not in option:
                            errors.append(ChatficValidationError(
                                "Each option should have a 'to' key"))
                        elif option["to"] not in page_ids:
                            errors.append(ChatficValidationError(
                                f"Option with a 'to' value that points to an "
                                f"unknown page id: {option['to']}"))
                        else:
                            page_ids_without_links.discard(option["to"])
            if len(page_ids_without_links) > 1:
                warnings.append(
                    f"There are more than 1 pages with "
                    f"no page options pointing "
                    f"them: {page_ids_without_links}"
                )

        return ChatficValidationResult(is_valid=not errors, errors=errors,
                                       warnings=warnings)


class CompiledChatficValidator(BaseChatficValidator):
    @staticmethod
    def validate(data: dict, multimedia_list: list) -> ChatficValidationResult:

        character_slugs = set()
        errors = []
        warnings = []
        valid_apps = []
        unused_multimedia = set(multimedia_list)
        bad_multimedia = set()

        # 1. Check Required Fields, and detect unnecessary fields:
        version = DEFAULT_VERSION
        if "version" in data:
            if data["version"] not in SUPPORTED_VERSIONS:
                errors.append(ChatficValidationError(
                    f"Unsupported version: {data[version]}. Supported "
                    f"versions are: {SUPPORTED_VERSIONS}"))
            version = data["version"]
        else:
            errors.append(ChatficValidationError(
                f"Missing version field. Rest of the validation will be for"
                f" the default version: {version}."
            ))
        # 1 Check Required Fields
        # 1.1 Check Required Top Level Fields, and detect unnecessary fields:
        required_fields = {
            "format": {"type": "str"},
            "chatFic": {"type": "dict"},
            "bubble": {"type": "list"},
        }

        for field, field_info in required_fields.items():
            if field not in data:
                errors.append(
                    ChatficValidationError(f"Missing required field: {field}"))
            else:
                # not a fan of E721
                if field_info["type"] != type(data[field]).__name__:
                    errors.append(ChatficValidationError(
                        f"Field '{field}' must be a {field_info['type']}"))

        unknown_fields = set(data.keys()) - set(required_fields.keys())
        unknown_fields.discard("version")
        if unknown_fields:
            warnings.append(
                f"Unknown fields found: {sorted(unknown_fields)}")

        # 1.2 Check Required ChatFic Fields
        if "chatFic" in data:
            required_chatfic_fields = {
                "globalidentifier": {"type": "str"},
                "serverslug": {"type": "str"},
                "title": {"type": "str"},
                "description": {"type": "str"},
                "author": {"type": "str"},
                "handles": {"type": "dict"},
                "variables": {"type": "dict"},
                "episode": {"type": "int"},
                "characters": {"type": "dict"}
            }
            if version == ChatficVersion.V1_1.value:
                required_chatfic_fields["apps"] = {"type": "dict"}

            for field, field_info in required_chatfic_fields.items():
                if field not in data["chatFic"]:
                    errors.append(
                        ChatficValidationError(
                            f"Missing required field: chatFic.{field}"))
                else:
                    if field_info["type"] != type(
                            data["chatFic"][field]).__name__:
                        errors.append(ChatficValidationError(
                            f"Field 'chatFic.{field}' must be"
                            f" a {field_info['type']}"))
                    else:
                        if field == "variables":
                            for variable, variable_data in data["chatFic"][
                                "variables"].items():
                                if not isinstance(variable_data, dict):
                                    errors.append(ChatficValidationError(
                                        f"Variable '{variable}' must be a dict")
                                    )
                                elif "value" not in variable_data:
                                    errors.append(ChatficValidationError(
                                        f"Variable '{variable}' must have a "
                                        f"'value'")
                                    )
                        if field == "apps" and version == ChatficVersion.V1_1.value:
                            for app_key, app_value in data["chatFic"]["apps"].items():
                                valid_apps.append(app_key)
                                if not isinstance(app_value, dict):
                                    errors.append(ChatficValidationError(
                                        f"App '{app_key}' must be a dict")
                                    )
                                else:
                                    if "name" in app_value and not isinstance(
                                            app_value["name"], str):
                                        errors.append(ChatficValidationError(
                                            f"Name for '{app_key}' must be a"
                                            f" string")
                                        )
                                    if "background" in app_value:
                                        if not isinstance(
                                            app_value["background"], str):
                                            errors.append(ChatficValidationError(
                                                f"Background for '{app_key}' exists"
                                                f" but it is not a string")
                                            )
                                        else:
                                            if app_value["background"] not in multimedia_list:
                                                bad_multimedia.add(
                                                    app_value["background"])
                                            else:
                                                unused_multimedia.discard(
                                                    app_value["background"])

            unknown_fields = set(data["chatFic"].keys()) - set(
                required_chatfic_fields.keys())
            unknown_fields.discard("modified")
            unknown_fields.discard("version")
            if unknown_fields:
                warnings.append(
                    f"Unknown fields found in"
                    f" 'chatFic': {sorted(unknown_fields)}")

            # 2. Validate Characters:
            if "characters" in data["chatFic"] and isinstance(
                    data["chatFic"]["characters"], dict):
                # 2. Validate character data:
                # 2.1: character keys check
                character_errors, character_warnings, character_slugs = CompiledChatficValidator.validateCharacters(
                    data["chatFic"]["characters"])

                errors += character_errors
                warnings += character_warnings

        # 3. Validate Messages:

        all_message_indexes = set()
        all_option_target_indexes = set()
        missing_message_fields = set()
        wrong_type_message_fields = set()
        unknown_message_fields = set()
        unknown_message_sides = set()
        unknown_message_characters = set()
        used_characters = set()
        notnull_single_option_text = set()
        null_multiple_option_texts = False

        # 3.1 Check each message for:
        if "bubble" in data and isinstance(data["bubble"], list):
            required_fields = {
                "messageindex": {"type": "int"},
                "from": {"type": "str"},
                "side": {"type": "int"},
                "chatroom": {"type": "str"},
            }
            for bubble in data["bubble"]:
                #   - Fields
                for field, field_info in required_fields.items():
                    if field not in bubble:
                        if field == "chatroom" and version == ChatficVersion.V1_1.value:
                            if "app" in bubble and bubble["app"] != "chat" and bubble["app"] is not None:
                                # chatroom is not required for non-chat messages for v1.1
                                continue
                        missing_message_fields.add(field)
                    else:
                        if field_info["type"] != type(bubble[field]).__name__:
                            if field == "from" and bubble[
                                "from"] is None and "options" in bubble and isinstance(
                                    bubble["options"], list) and bubble[
                                "options"]:
                                # from can be null on bubbles with options.
                                pass
                            else:
                                wrong_type_message_fields.add(field)

                unknown = set(bubble.keys()) - set(required_fields.keys())
                unknown.discard("options")
                unknown.discard("sentiment")
                unknown.discard("multimedia")
                unknown.discard("message")
                if version == ChatficVersion.V1_1.value:
                    unknown.discard("extra")
                    unknown.discard("notification")
                    unknown.discard("app")
                    unknown.discard("type")
                if unknown:
                    unknown_message_fields.update(unknown)

                if "message" not in bubble:
                    missing_message_fields.add("message")
                elif bubble["message"] is not None and not isinstance(
                        bubble["message"], str):
                    wrong_type_message_fields.add("message")

                #   - Store a list of all messageindex
                #   - Check duplicate messageindex
                if "messageindex" in bubble and isinstance(
                        bubble["messageindex"], int):
                    if bubble["messageindex"] in all_message_indexes:
                        errors.append(ChatficValidationError(
                            f"Duplicate message index: "
                            f"{bubble['messageindex']}"))
                    all_message_indexes.add(bubble["messageindex"])
                #   - Side
                if "side" in bubble:
                    if bubble["side"] not in [0, 1, 2]:
                        unknown_message_sides.add(bubble["side"])
                #   - Unknown Characters
                if "from" in bubble:
                    if bubble["from"] not in character_slugs:
                        if bubble["from"] is not None:
                            unknown_message_characters.add(bubble["from"])
                    elif bubble["from"] not in ["app"]:
                        used_characters.add(bubble["from"])
                #   - Unknown Media
                if "multimedia" in bubble:
                    if bubble["multimedia"] is not None:
                        if bubble["multimedia"] not in multimedia_list:
                            bad_multimedia.add(bubble["multimedia"])
                        else:
                            unused_multimedia.discard(bubble["multimedia"])
                if "extra" in bubble and bubble[
                    "extra"] is not None and version == ChatficVersion.V1_1.value:
                    if not isinstance(bubble["extra"], dict):
                        wrong_type_message_fields.add("extra")
                if "app" in bubble and bubble[
                    "app"] is not None and version == ChatficVersion.V1_1.value:
                    if not isinstance(bubble["app"], str):
                        wrong_type_message_fields.add("app")
                    elif bubble["app"] not in valid_apps:
                        errors.append(ChatficValidationError(
                            f"Unknown app '{bubble['app']}'"))
                    else:
                        pass # for now
                if "type" in bubble and bubble[
                    "type"] is not None and version == ChatficVersion.V1_1.value:
                    if not isinstance(bubble["type"], str):
                        wrong_type_message_fields.add("type")
                if "sentiment" in bubble and bubble[
                    "sentiment"] is not None and version in [ChatficVersion.V1_1.value, ChatficVersion.V1]:
                    if not isinstance(bubble["sentiment"], str):
                        wrong_type_message_fields.add("sentiment")
                if "options" in bubble:
                    if not isinstance(bubble["options"], list):
                        wrong_type_message_fields.add("options")
                    else:
                        null_text_required = False
                        if len(bubble["options"]) == 1:
                            null_text_required = True
                        for option in bubble["options"]:
                            #   - Option Format
                            if not isinstance(option, dict):
                                wrong_type_message_fields.add("options")
                            else:
                                # A- check option.text
                                if "text" not in option:
                                    missing_message_fields.add("options.text")
                                elif option["text"] is None:
                                    if not null_text_required:
                                        null_multiple_option_texts = True
                                else:
                                    if null_text_required:
                                        notnull_single_option_text.add(
                                            option["text"])
                                    else:
                                        if not isinstance(option["text"], str):
                                            wrong_type_message_fields.add(
                                                "options.text")

                                # B- check option.to
                                if "to" not in option:
                                    missing_message_fields.add("options.to")
                                else:
                                    if isinstance(option["to"], int):
                                        all_option_target_indexes.add(
                                            option["to"])
                                    else:
                                        wrong_type_message_fields.add(
                                            "options.to")

            #   - Missing Fields (error):
            if missing_message_fields:
                errors.append(ChatficValidationError(
                    f"Missing message fields: "
                    f"{sorted(missing_message_fields)}"))

            #   - Wrong Type Fields (error):
            if wrong_type_message_fields:
                errors.append(
                    ChatficValidationError(
                        f"Wrong type fields found: "
                        f"{sorted(wrong_type_message_fields)}")
                )

            #    - Unknown Fields (error):
            if unknown_message_fields:
                errors.append(ChatficValidationError(
                    f"Unknown message fields found: "
                    f"{sorted(unknown_message_fields)}"))

            #   - Unknown Characters (error):
            if unknown_message_characters:
                errors.append(ChatficValidationError(
                    f"Unknown characters found: "
                    f"{sorted(unknown_message_characters)}"))

            #   - Unused Characters (warning)
            unused_characters = character_slugs - used_characters
            unused_characters = unused_characters - {"app"}
            if unused_characters:
                warnings.append(
                    f"Unused characters: "
                    f"{sorted(unused_characters)}")

            #   - Unused Media (warning)
            if unused_multimedia:
                warnings.append(
                    f"Unused multimedia: "
                    f"{sorted(unused_multimedia)}")
                for unused_multimedia_single in sorted(unused_multimedia):
                    warnings.append(
                        "Multimedia not used: " + unused_multimedia_single)

            #   - Bad Multimedia (error)
            if bad_multimedia:
                errors.append(ChatficValidationError(
                    f"Unknown multimedia: "
                    f"{sorted(bad_multimedia)}"
                ))

            #   - Notnull Single Option Text (warning)
            if notnull_single_option_text:
                warnings.append(
                    f"Text for single option will be ignored: "
                    f"{sorted(notnull_single_option_text)}")

            #   - Null Multiple Option Text (error)
            if null_multiple_option_texts:
                errors.append(ChatficValidationError(
                    "Text value on multiple options cannot be null"
                ))

            #   - Unknown Sides (error)
            if unknown_message_sides:
                errors.append(ChatficValidationError(
                    f"Unknown sides found: "
                    f"{sorted(unknown_message_sides)}"
                ))

        # 3.2 For all messages starting from the last one:
        #   - (Warning) Check if there is either i-1 in message index list
        #   or i in option targets list. Shouldn't be more than one,
        #   but it can be zero
        unreachable_indexes = set()
        all_message_indexes_list = list(all_message_indexes)
        for i in range(len(all_message_indexes) - 1, -1, -1):
            if all_message_indexes_list[
                i] - 1 not in all_message_indexes_list and \
                    all_message_indexes_list[
                        i] not in all_option_target_indexes:
                unreachable_indexes.add(all_message_indexes_list[i])

        if len(unreachable_indexes) > 1:
            unreachable_indexes = set(list(sorted(unreachable_indexes))[1:])
            warnings.append(
                f"Unreachable message indexes: "
                f"{sorted(unreachable_indexes)}")

        # 3.3 Check if each option points to an existing message index.
        bad_option_targets = all_option_target_indexes - all_message_indexes

        if bad_option_targets:
            errors.append(ChatficValidationError(
                f"Unknown option targets: "
                f"{sorted(bad_option_targets)}"
            ))

        return ChatficValidationResult(is_valid=not errors, errors=errors,
                                       warnings=warnings)
