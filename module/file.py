import os

import json
import configparser


class File():
    def __init__(self, filename: str):
        """
        :param filename: Path to the file or its name.
        :type filename: str
        
        Example Input: File("config.json")
        """
        self.filename = filename
        self.txt = self.txt_file(self)
        self.jsonf = self.json_file(self)
        self.ini = self.ini_file(self)

    class txt_file:
        def __init__(self, outer_instance):
            self.outer = outer_instance

        def read(self):
            """
            :return: The content of the text file.
            :rtype: str
            
            Example Output: "Hello World\\nLine 2"
            """
            with open(self.outer.filename, "r", encoding="utf-8") as f:
                return f.read()

        def write(self, data: str):
            """
            :param data: String data to write to the file (overwrites existing content).
            :type data: str
            
            Example Input: .write("New content")
            """
            with open(self.outer.filename, "w", encoding="utf-8") as f:
                f.write(data)

        def append(self, data: str):
            """
            :param data: String data to append to the end of the file.
            :type data: str
            
            Example Input: .append("\\nNew line")
            """
            with open(self.outer.filename, "a", encoding="utf-8") as f:
                f.write(data)

    class json_file:
        def __init__(self, outer_instance):
            self.outer = outer_instance
        
        def read(self):
            """
            :return: Data from the JSON file as a dictionary.
            :rtype: dict
            
            Example Output: {"user": "admin", "id": 1}
            """
            with open(self.outer.filename, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    return {}
                return json.loads(content)

        def write(self, data: dict):
            """
            :param data: Dictionary to save in JSON format.
            :type data: dict
            
            Example Input: .write({"status": "ok"})
            """
            with open(self.outer.filename, "w", encoding="utf-8") as f:
                ss = json.dumps(data, indent=4, ensure_ascii=False)
                f.write(ss)

        def update(self, data: dict):
            """
            :param data: Dictionary to merge with the existing JSON content.
            :type data: dict
            
            Example Input: .update({"new_key": 123})
            """
            current = self.read()
            current.update(data)
            self.write(current)
        
        def delete(self, key):
            """
            :param key: The key name to remove from the JSON root.
            :return: True if the key was deleted, False if not found.
            :rtype: bool
            
            Example Input: .delete("old_key")
            Example Output: True
            """
            current = self.read()
            if key in current:
                del current[key]
                self.write(current)
                return True
            return False
        
        def delete_nested(self, *keys):
            """
            :param keys: A sequence of keys leading to the target element.
            :return: True if successfully deleted, False otherwise.
            :rtype: bool
            
            Example Input: .delete_nested("users", "admin", "password")
            Example Output: True
            """
            current = self.read()
            temp = current
            
            for key in keys[:-1]:
                if key not in temp:
                    return False
                temp = temp[key]
            
            if keys[-1] in temp:
                del temp[keys[-1]]
                self.write(current)
                return True
            
            return False
    
    class ini_file:
        def __init__(self, outer_instance):
            self.config = configparser.ConfigParser()
            self.outer = outer_instance
        
        def read(self):
            """
            Loads the INI file into the internal parser.
            
            NOTE: This method does NOT return the file's data. 
            It returns a list of files that were successfully read.
            After calling this, use .get() to extract values.

            :return: List of read filenames.
            :rtype: list

            Example:
                ini = File("settings.ini").ini
                ini.read()  # Now the 'config' object is populated
            """
            self.config.clear()
            return self.config.read(self.outer.filename, encoding='utf-8')

        def write(self, name: str, data: dict):
            """
            :param name: Section name in the INI file.
            :type name: str

            :param data: Dictionary of keys and values for the section.
            :type data: dict
            
            Example Input: .write("Settings", {"volume": "100"})
            """
            self.config[name] = {str(k): str(v) for k, v in data.items()}

            with open(self.outer.filename, "w", encoding='utf-8') as configfile:
                self.config.write(configfile)
        
        def update(self, name: str, data: dict):
            """
            :param name: Name of the section to update.
            :type name: str

            :param data: Dictionary of keys and values to add/update in the section.
            :type data: dict
            
            Example Input: .update("Settings", {"theme": "dark"})
            """
            self.read()

            if not self.config.has_section(name): self.config.add_section(name)

            for key, value in data.items():
                self.config.set(name, str(key), str(value))

            with open(self.outer.filename, "w", encoding="utf-8") as configfile:
                self.config.write(configfile)
        
        def get(self, section: str, key: str, data_type=str, fallback=None):
            """
            Retrieves a value from a specific section and key, converting it to the specified type.
            
            :param section: The section name (e.g., 'Settings').
            :param key: The key name within the section.
            :param data_type: Target type: str, int, float, or bool.
            :param fallback: Value to return if the key or section is missing.

            Example:
                ini = File("config.ini").ini
                ini.read()
                # Get 'volume' from 'Audio' section as an integer, default to 50
                data = ini.get("Audio", "volume", int, 50)
                print(data, type(data))
                # Output: 100 <class 'int'> (if found) or 50 <class 'int'>
            """
            try:
                if data_type == int:
                    return self.config.getint(section, key, fallback=fallback)
                if data_type == bool:
                    return self.config.getboolean(section, key, fallback=fallback)
                if data_type == float:
                    return self.config.getfloat(section, key, fallback=fallback)
                return self.config.get(section, key, fallback=fallback)
            except (configparser.NoSectionError, configparser.NoOptionError):
                return fallback
