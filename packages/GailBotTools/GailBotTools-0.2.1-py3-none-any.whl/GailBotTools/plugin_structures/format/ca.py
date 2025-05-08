import subprocess
import platform
from typing import Dict, Any
import os
import logging
import tempfile

from GailBotTools.plugin_structures.plugin import Plugin
from GailBotTools.plugin_structures.methods import GBPluginMethods
from GailBotTools.configs.configs import PLUGIN_NAME
from GailBotTools.configs.configs import (
    PLUGIN_NAME,
    OUTPUT_FILE
)


class CAPlugin(Plugin):
    def __init__(self) -> None:
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods):
        try:
            chat_output = dependency_outputs[PLUGIN_NAME.Chat]
            chat_data = chat_output["data"]
            temp_dir = methods.output_path

            # Create temp .chat file
            with tempfile.NamedTemporaryFile(mode="w", suffix=OUTPUT_FILE.CHAT, dir=temp_dir, delete=False, encoding="utf-8") as chat_file:
                chat_file.write(chat_data)
                chat_file_path = chat_file.name

            # Determine binary path
            cpu = platform.processor()
            if "arm" in cpu.lower():
                binary_path = os.path.join(os.path.dirname(__file__), "jeffersonize-apple")
            elif "i386" in cpu.lower() or "x86" in cpu.lower():
                binary_path = os.path.join(os.path.dirname(__file__), "jeffersonize-intel")
            else:
                self.successful = False
                return

            subprocess.run(["chmod", "+x", binary_path])
            subprocess.run([binary_path, "chat2calite", chat_file_path], check=True)

            # Read output .ca file
            ca_file_path = chat_file_path.replace(".cha", ".ca")
            with open(ca_file_path, "r", encoding="utf-8") as ca_file:
                ca_data = ca_file.read()

            # Clean up
            os.remove(chat_file_path)
            os.remove(ca_file_path)

            self.successful = True
            return {
                "filetype": "ca",
                "encoding_type": "utf-8",
                "data": ca_data
            }

        except Exception as e:
            logging.error("CAPlugin failed", exc_info=e)
            self.successful = False
            return
