class Attribute:
    """
    Abstract attribute class
    """

    def __init__(self, data):
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dict")

        self.name = ""
        if "attribute_name" in data.keys():
            self.name = data["attribute_name"]
        elif "Attribute_Name" in data.keys():
            self.name = data["Attribute_Name"]
        elif "attribute_identifier" in data.keys():
            self.name = data["attribute_identifier"]


class Timeseries(Attribute):
    """
    Timeseries attribute class
    """

    def __init__(self, data):
        super().__init__(data)
        self.timeseries_id = ""
        self.tag = ""
        if "TAG_ID" in data.keys():
            self.tag = data["TAG_ID"]
        elif "Tag_Id" in data.keys():
            self.tag = data["Tag_Id"]
        elif "timeseries_name" in data.keys():
            self.tag = data["timeseries_name"]

        self.source = ""
        if "source" in data.keys():
            self.source = data["source"]
        elif "Attribute_Source_Name" in data.keys():
            self.source = data["Attribute_Source_Name"]

    def __str__(self):
        return f"Timeseries: {self.name} - ({self.tag}) @ {self.source}"


class Constant(Attribute):
    """
    Constant attribute class
    """

    def __init__(self, data):
        super().__init__(data)
        self.value = ""
        if "value" in data.keys():
            self.value = data["value"]
        elif "Attribute_Value" in data.keys():
            self.value = data["Attribute_Value"]

    def __str__(self):
        return f"Constant: {self.name} - ({self.value})"
