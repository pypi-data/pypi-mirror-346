# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 09:10:54
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-13 08:41:55


# Standard imports
from typing import List, Any, Dict

# import re
from copy import deepcopy

# Local imports
from GailBotTools.plugin_structures.plugin import Plugin
from GailBotTools.plugin_structures.methods import GBPluginMethods
from GailBotTools.plugin_structures.marker_utterance_dict import UttObj
from GailBotTools.plugin_structures.format.nodes import Node, Word


class SpeakerMapPlugin(Plugin):
    def __init__(self) -> None:
        super().__init__()

    def apply(
        self, dependency_outputs: Dict[str, Any], methods: GBPluginMethods
    ) -> Dict[str, Dict[str, List[List[Node]]]]:
        """
        Creates a dictionary for speaker-level analysis of transcription.

        1. Create a new speaker dictionary
        2. Iterates through every utterance in the given word-level dictionary
        3. If the speaker dictionary has an existing speaker label for the
           current utterance being iterated over in the word-level dictionary,
           add the utterance to the speaker dictionary.
           Else, create a new list of utterances with that speaker label in the
           speaker dictionary.

        Args:
            dependency_outputs (Dict[str, Any]):
            methods (PluginMethodSuite):

        Returns:
           Dict[str, Dict[str, List[List[Node]]]]: Dict of Dicts for each speaker
        """
        utteranceDict: Dict[str, List[Node]] = dependency_outputs["UtteranceMapPlugin"]

        # create the dictionary here
        speakerDict: Dict[str, Dict[str, List[List[Node]]]] = dict()

        # iterate through each utterance in the utterance dictionary
        for utteranceList in utteranceDict.values():

            # if speaker label in dictionary, add utterance to dict
            if utteranceList[0].val.sLabel in speakerDict:
                speakerDict[utteranceList[0].val.sLabel]["utteranceList"].append(
                    utteranceList
                )
            else:
                # if not, create new utterance list for the speaker dictionary
                newList = list()
                newDict = dict()
                speakerDict[utteranceList[0].val.sLabel] = newDict
                speakerDict[utteranceList[0].val.sLabel]["utteranceList"] = newList

        self.successful = True
        return speakerDict
