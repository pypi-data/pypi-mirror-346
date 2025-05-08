import io
from typing import Dict, Any
import csv

# Local imports
from GailBotTools.plugin_structures.plugin import Plugin
from GailBotTools.plugin_structures.methods import GBPluginMethods
from GailBotTools.plugin_structures.format.conversation_model import ConversationModel
from GailBotTools.configs.configs import (
    INTERNAL_MARKER,
    load_label,
    PLUGIN_NAME,
    FORMATTER
)

CSV_FORMATTER = FORMATTER.CSV

MARKER = INTERNAL_MARKER
LABEL = load_label().CSV

class CSVPlugin(Plugin):
    def __init__(self) -> None:
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods):
        utt_csv = self._utterance_level(dependency_outputs)
        word_csv = self._word_level(dependency_outputs)
        self.successful = True
        return [utt_csv, word_csv]

    def _utterance_level(self, dependency_outputs: Dict[str, Any]) -> Dict[str, str]:
        cm: ConversationModel = dependency_outputs[PLUGIN_NAME.ConvModel]
        varDict = {
            MARKER.GAPS: LABEL.GAPMARKER,
            MARKER.OVERLAPS: LABEL.OVERLAPMARKER,
            MARKER.OVERLAP_FIRST_START: LABEL.OVERLAPMARKER_CURR_START,
            MARKER.OVERLAP_FIRST_END: LABEL.OVERLAPMARKER_CURR_END,
            MARKER.OVERLAP_SECOND_START: LABEL.OVERLAPMARKER_NEXT_START,
            MARKER.OVERLAP_SECOND_END: LABEL.OVERLAPMARKER_NEXT_END,
            MARKER.PAUSES: LABEL.PAUSE,
        }

        root = cm.getTree(False)
        newUttMap = dict()
        cm.outer_buildUttMapWithChange(0)(root, newUttMap, varDict)

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(CSV_FORMATTER.HEADER)

        for _, (_, nodeList) in enumerate(newUttMap.items()):
            curr_utt = cm.getWordFromNode(nodeList)
            txt = CSV_FORMATTER.TXT_SEP.join(word.text for word in curr_utt)

            if curr_utt[0].sLabel not in {LABEL.PAUSE, LABEL.GAPMARKER}:
                sLabel = LABEL.SPEAKERLABEL + str(curr_utt[0].sLabel)
                writer.writerow([sLabel, txt, curr_utt[0].startTime, curr_utt[-1].endTime])
            else:
                writer.writerow(["", txt, curr_utt[0].startTime, curr_utt[-1].endTime])

        return {
            "filetype": "csv-utterance",
            "encoding_type": "utf-8",
            "data": output.getvalue()
        }

    def _word_level(self, dependency_outputs: Dict[str, Any]) -> Dict[str, str]:
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
        cm.outer_buildUttMapWithChange(0)(root, newUttMap, varDict)

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(CSV_FORMATTER.HEADER)

        for _, (_, nodeList) in enumerate(newUttMap.items()):
            curr_utt = cm.getWordFromNode(nodeList)
            for word in curr_utt:
                if word.sLabel not in MARKER.INTERNAL_MARKER_SET:
                    sLabel = LABEL.SPEAKERLABEL + str(word.sLabel)
                else:
                    sLabel = word.sLabel
                writer.writerow([sLabel, word.text, word.startTime, word.endTime])

        return {
            "filetype": "csv-word",
            "encoding_type": "utf-8",
            "data": output.getvalue()
        }
