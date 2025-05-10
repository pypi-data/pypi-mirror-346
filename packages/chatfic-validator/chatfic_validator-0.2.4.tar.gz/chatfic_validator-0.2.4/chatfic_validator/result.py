class ChatficValidationResult:
    def __init__(self, is_valid, errors=None, warnings=None):
        """
        Initialize a ChatficValidationResult object.

        Args:
            is_valid (bool): Indicates whether the validation was successful.
            errors (list): A list of errors encountered during validation.
             Empty if is_valid is True.
            warnings (list): A list of warnings found in a valid chatfic story.
             Empty if is_valid is False.
        """
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []

    def __str__(self):
        name = "ChatficValidationResult: "
        if self.is_valid:
            name += "Valid Chatfic. No errors. Warnings: " + str(
                len(self.warnings))
        else:
            name += "Invalid Chatfic. Errors: " + str(
                len(self.errors)) + ", Warnings: " + str(
                len(self.warnings)) + " " + str(self.errors)

        name += "\n"
        name += "Readable attributes: is_valid, errors, warnings."

        return name
