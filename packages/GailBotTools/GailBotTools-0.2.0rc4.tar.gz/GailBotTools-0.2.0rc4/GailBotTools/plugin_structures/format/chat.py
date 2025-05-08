# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 10:54:53
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-13 08:42:29
import os
import logging
from typing import Dict, Any
import shutil

# Local imports
from GailBotTools.plugin_structures.plugin import Plugin
from GailBotTools.plugin_structures.methods import GBPluginMethods
from GailBotTools.plugin_structures.format.conversation_model import ConversationModel
from GailBotTools.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    CHAT_FORMATTER
)

MARKER = INTERNAL_MARKER
LABEL = load_label().CHAT


class ChatPlugin(Plugin):

    def __init__(self) -> None:
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods):
        """
        Prints the entire tree in a user-specified chat format
        """
        cm: ConversationModel = dependency_outputs[PLUGIN_NAME.ConvModel]
        varDict = {
            MARKER.GAPS: LABEL.GAPMARKER,
            MARKER.OVERLAP_FIRST_START: LABEL.OVERLAPMARKER_CURR_START,
            MARKER.OVERLAP_FIRST_END: LABEL.OVERLAPMARKER_CURR_END,
            MARKER.OVERLAP_SECOND_START: LABEL.OVERLAPMARKER_NEXT_START,
            MARKER.OVERLAP_SECOND_END: LABEL.OVERLAPMARKER_NEXT_END,
            MARKER.PAUSES: LABEL.PAUSE,
            MARKER.FASTSPEECH_START: MARKER.FASTSPEECH_DELIM,
            MARKER.FASTSPEECH_END: MARKER.FASTSPEECH_DELIM,
            MARKER.SLOWSPEECH_START: MARKER.SLOWSPEECH_DELIM,
            MARKER.SLOWSPEECH_END: MARKER.SLOWSPEECH_DELIM,
        }
        # Gets tree and utterance map from conversation model generated from dependency map
        infoOnly = {MARKER.GAPS, MARKER.PAUSES}
        markerOnly = {
            MARKER.OVERLAP_FIRST_END,
            MARKER.OVERLAP_SECOND_START,
            MARKER.OVERLAP_SECOND_END,
            MARKER.FASTSPEECH_START,
            MARKER.FASTSPEECH_END,
            MARKER.SLOWSPEECH_START,
            MARKER.SLOWSPEECH_END,
        }
        root = cm.getTree(False)
        newUttMap = dict()
        myFunction = cm.outer_buildUttMapWithChange(0, infoOnly=infoOnly)
        myFunction(root, newUttMap, varDict)
        merged_file = shutil.copy(methods.merged_media, methods.output_path)
        filename, extension = os.path.splitext(os.path.basename(merged_file))
        audio_extensions = [".mp3", ".wav", ".aiff", ".flac"]
        video_extensions = [".mp4", ".mov", ".avi", ".mkv"]
        if extension in audio_extensions:
            file_format = "audio"
        elif extension in video_extensions:
            file_format = "video"
        else:
            file_format = "audio"  # default to be confirmed

        chat_output = []

        # Header metadata
        chat_output.append(CHAT_FORMATTER.HEADER_LANGUAGE.format("eng"))
        chat_output.append(CHAT_FORMATTER.AUDIO_PATH.format(filename, file_format))
        chat_output.append(CHAT_FORMATTER.TRANSCRIBER.format("GailBot"))

        # Utterance content
        for _, (_, nodeList) in enumerate(newUttMap.items()):
            curr_utt = cm.getWordFromNode(nodeList)
            txt = CHAT_FORMATTER.TXT_SEP.join(word.text for word in curr_utt)
            sLabel = LABEL.SPEAKERLABEL + str(curr_utt[0].sLabel)

            turn = CHAT_FORMATTER.TURN.format(
                sLabel,
                txt,
                int(curr_utt[0].startTime * 1000),
                int(curr_utt[-1].endTime * 1000),
                "\u0015",     # delimiter 1
                ".    ",      # delimiter 2
            )
            chat_output.append(turn)

        # End of file marker
        chat_output.append(CHAT_FORMATTER.END)

        # Join all lines and return as dict
        full_output = ''.join(chat_output)
        self.successful = True
        return {
            "filetype": "chat",
            "encoding_type": "utf-8",
            "data": full_output
        }
