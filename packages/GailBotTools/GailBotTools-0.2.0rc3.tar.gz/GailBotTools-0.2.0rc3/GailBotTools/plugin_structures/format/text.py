# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 10:54:53
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-13 08:42:53


from typing import Dict, Any, List, Tuple
import re
import io
import os

# Local imports
from GailBotTools.plugin_structures.plugin import Plugin
from GailBotTools.plugin_structures.methods import GBPluginMethods
from GailBotTools.plugin_structures.format.conversation_model import ConversationModel
from GailBotTools.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    OUTPUT_FILE,
    CON_FORMATTER)

MARKER = INTERNAL_MARKER
LABEL = load_label().TXT


class TextPlugin(Plugin):
    def __init__(self) -> None:
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods):
        """
        Prints the entire tree in a user-specified format
        """
        cm: ConversationModel = dependency_outputs[PLUGIN_NAME.ConvModel]

        varDict = {
            MARKER.GAPS: LABEL.GAPMARKER,
            MARKER.OVERLAPS: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_FIRST_START: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_FIRST_END: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_SECOND_START: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_SECOND_END: LABEL.OVERLAPMARKER,
            MARKER.PAUSES: LABEL.PAUSE,
        }

        root = cm.getTree(False)
        newUttMap = dict()
        myFunction = cm.outer_buildUttMapWithChange(0)
        myFunction(root, newUttMap, varDict)

        path = os.path.join(methods.output_path, OUTPUT_FILE.CON_TXT)
        utterances = newUttMap

        with io.open(path, "w", encoding="utf-8") as outfile:
            for i, (id, nodeList) in enumerate(utterances.items()):
                curr_utt = cm.getWordFromNode(nodeList)
                l = []
                for word in curr_utt:
                    l.append(word.text)
                txt = CON_FORMATTER.TXT_SEP.join(l)

                sLabel = LABEL.SPEAKERLABEL + str(curr_utt[0].sLabel)
                turn = CON_FORMATTER.TURN.format(
                    sLabel, txt, curr_utt[0].startTime, curr_utt[-1].endTime, 0x15
                )
                outfile.write(turn)
        self.successful = True
        return
