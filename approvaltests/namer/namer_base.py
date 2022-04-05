import json
import os
from abc import abstractmethod
from typing import Optional, Dict

from approvaltests.core.namer import Namer


class NamerBase(Namer):

    def __init__(self, extension: Optional[str] = None) -> None:
        self.extension_with_dot = extension or ".txt"

    #@abstractmethod
    def get_file_name(self):
        raise Exception("This class is abstract, override this method in a subclass")

    @abstractmethod
    def get_directory(self):
        raise Exception("This class is abstract, override this method in a subclass")

    def get_config(self) -> Dict[str, str]:
        """lazy load config when we need it, then store it in the instance variable self.config"""
        if not self.config_loaded:
            config_file = os.path.join(
                self.config_directory(), "approvaltests_config.json"
            )
            if os.path.exists(config_file):
                with open(config_file, "r", encoding='utf8') as file:
                    self.config = json.load(file)
            else:
                self.config = {}
            self.config_loaded = True
        return self.config

    def get_basename(self) -> str:
        file_name = self.get_file_name()
        subdirectory = self.get_config().get("subdirectory", "")
        return str(os.path.join(self.get_directory(), subdirectory, file_name))

    def get_received_filename(self, basename: Optional[str] = None) -> str:
        basename = basename or self.get_basename()
        return basename + Namer.RECEIVED + self.extension_with_dot

    def get_approved_filename(self, basename: Optional[str] = None) -> str:
        basename = basename or self.get_basename()
        return basename + Namer.APPROVED + self.extension_with_dot

    def set_extension(self, extension):
        self.extension_with_dot = extension

