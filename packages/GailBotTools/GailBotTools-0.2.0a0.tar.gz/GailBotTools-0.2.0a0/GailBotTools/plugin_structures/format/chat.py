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
    OUTPUT_FILE,
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

        # start printing to file
        # header of the file
        # TODO: eng?
        data = [
            CHAT_FORMATTER.HEADER_LANGUAGE.format("eng"),
            CHAT_FORMATTER.AUDIO_PATH.format(filename, file_format),
            CHAT_FORMATTER.TRANSCRIBER.format("GailBot"),
        ]

        path = os.path.join(methods.output_path, OUTPUT_FILE.CHAT)
        utterances = newUttMap
        with open(path, "w", encoding="utf-8") as outfile:
            for item in data:
                outfile.write(item)
            for _, (_, nodeList) in enumerate(utterances.items()):
                curr_utt = cm.getWordFromNode(nodeList)

                l = []
                for word in curr_utt:
                    l.append(word.text)
                txt = CHAT_FORMATTER.TXT_SEP.join(l)
                sLabel = LABEL.SPEAKERLABEL + str(curr_utt[0].sLabel)
                # actual text content
                turn = CHAT_FORMATTER.TURN.format(
                    sLabel,
                    txt,
                    int(curr_utt[0].startTime * 1000),
                    int(curr_utt[-1].endTime * 1000),
                    "\u0015",
                    ".    ",
                )

                outfile.write(turn)
            outfile.write(CHAT_FORMATTER.END)
        self.successful = True
        return path
