import subprocess
import platform
from typing import Dict, Any
import os
import logging
from GailBotTools.plugin_structures.plugin import Plugin
from GailBotTools.plugin_structures.methods import GBPluginMethods
from GailBotTools.configs.configs import PLUGIN_NAME


class CAPlugin(Plugin):
    def __init__(self) -> None:
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods):
        """
        Prints the entire tree in a user-specified chat format
        """
        chat_path = dependency_outputs[PLUGIN_NAME.Chat]
        try:
            cpu = platform.processor()
            if "arm" in cpu.lower():
                binary_path = os.path.join(
                    os.path.dirname(__file__), "jeffersonize-apple"
                )
            elif "i386" in cpu.lower() or "x86" in cpu.lower():
                binary_path = os.path.join(
                    os.path.dirname(__file__), "jeffersonize-intel"
                )
            else:
                self.successful = False
                return
            CHAT_TO_CA = "chat2calite"
            subprocess.run(["chmod", "+x", binary_path])
            subprocess.run([binary_path, CHAT_TO_CA, chat_path])
            self.successful = True
        except Exception as e:
            logging.error(e, exc_info=e)
            self.successful = False
