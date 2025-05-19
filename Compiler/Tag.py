class Tag:
    """
    Class representing an HTML-like tag with open and close attributes.
    """

    def __init__(self, tag_name: str, value: str, text_size_limit: int = 10):
        """
        Initializes the Tag object.

        Args:
            tag_name (str): The name of the tag.
            value (str): The value containing open and close tag information.
            text_size_limit (int, optional): The maximum allowed text size. Defaults to 10.
        """
        self.tag_name = tag_name
        self.open_tag, self.close_tag = "", ""

        try:
            if value not in "}{":
                self.open_tag, self.close_tag = value.split("[]")
        except ValueError:
            print(f"Error processing tag: {self.tag_name}")

        self.text_size_limit = text_size_limit

    def __str__(self) -> str:
        """
        Returns a string representation of the tag.

        Returns:
            str: The tag name.
        """
        return f"Tag: {self.tag_name}"
