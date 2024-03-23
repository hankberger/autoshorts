import xml.etree.ElementTree as ET

class Configuration():
    def __init__(self):
        # Parse XML from a file
        self.tree = ET.parse('config.xml')
        # Get the root element
        self.root = self.tree.getroot()

    def __getattribute__(self, name: str) -> str:
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            tag = self.root.find(name)
            if not tag is None:
                return self.root.find(name).text
            return None


configex = Configuration()
print(configex.ScriptSystemPrompt)