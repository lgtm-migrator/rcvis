"""
Describes what happened in each round of an RCV Election in plain English.
"""

from visualizer.common import intify
from visualizer.descriptors import common
from visualizer.descriptors import textForWinnerUtils


class Describer:
    """ Describes a graph in plain English.
        Iteratively call describe_round() on each round for the given graph. """

    def __init__(self, graph, config, summarizeAsParagraph):
        """
        Initializes the Describer

        :param graph: The graph to summarize
        :param summarizeAsParagraph: If true, the summary for each round is a paragraph.\
            If false, the summary is a list of events for each round.
        """
        self.graph = graph
        self.config = config
        self.summarizeAsParagraph = summarizeAsParagraph

        self.textOnlyDescribers = [
            self._describe_the_round_number,
            self._describe_transfers_this_round,
            self._describe_eliminated_this_round,
            self._describe_most_nonwinner_votes_this_round,
            self._describe_winners_this_round,
            self._describe_redistribution_this_round
        ]
        self.listOnlyDescribers = [
            self._describe_first_round,
            self._describe_eliminated_this_round,
            self._describe_transfers_this_round,
            self._describe_winners_this_round,
            self._describe_redistribution_this_round
        ]

    @classmethod
    def _describe_the_round_number(cls, roundNum):
        """ e.g. "In the third round, " """
        roundDescribers = [
            "first",
            "second",
            "third",
            "fourth",
            "fifth",
            "sixth",
            "seventh",
            "eighth",
            "ninth",
            "tenth"]
        if roundNum < 10:
            return f"In the {roundDescribers[roundNum]} round, "
        # I'm being lazy, but...this many rounds is rare
        return f"In round {roundNum}, "

    def _describe_most_nonwinner_votes_this_round(self, roundNum):
        """ e.g. "Foo received the most votes. "
            Returns empty string if there are any winners this round. """
        candidates = self.graph.summarize().candidates
        rounds = self.graph.summarize().rounds

        # Don't return who has the most votes if there are winners
        if rounds[roundNum].winnerNames:
            return ""

        def _num_votes_this_round(item):
            # Gets the number of votes for this item on this round
            candidateInfo = candidates[item]
            if roundNum >= len(candidateInfo.totalVotesPerRound):
                return 0  # already eliminated
            return candidateInfo.totalVotesPerRound[roundNum]
        mostVotes = max(candidates, key=_num_votes_this_round)

        return mostVotes.name + " received the most votes. "

    @classmethod
    def _list_to_describe_list_of_names(cls, listOfNames, verb, whatHappenedToThemDescription):
        """
        e.g. With listOfNames = [Foo,Bar,Baz], verb="ate", and whatHappenedToThem="ate chips":
        [ {summary: "Foo ate", verb: "ate", description: "Foo at chips"},
          {summary: "Bar ate", verb: "ate", description: "Bar at chips"},
          {summary: "Baz ate", verb: "ate", description: "Baz at chips"} ]
        listOfNames can be empty, in which case an empty list is returned.
        """
        return [{'summary': name + verb,
                 'description': whatHappenedToThemDescription.format(name=name),
                 'verb': verb}
                for name in listOfNames]

    def _describe_list_of_names(self, listOfNames, verb, whatHappenedToThemDescription):
        """
            Calls either common.text_to_describe_list_of_names or _list_to_describe_list_of_names

            :param listOfNames: A list of names to whom this happened
            :param verb: A short description, only used when !summarizeAsParagraph
            :param whatHappenedToThemDescription: A f-string that must contain {name}, \
                where {name} will be replaced with either a single name or a list of names.
        """
        # verb is ignored when self.summarizeAsParagraph
        if self.summarizeAsParagraph:
            result = common.text_to_describe_list_of_names(
                listOfNames, whatHappenedToThemDescription)
        else:
            result = self._list_to_describe_list_of_names(
                listOfNames, verb, whatHappenedToThemDescription)

        return result

    def _describe_eliminated_this_round(self, roundNum):
        """ e.g. "Foo had the fewest votes and was eliminated. "
            Returns empty string if nobody was eliminated."""
        rounds = self.graph.summarize().rounds
        eliminated = rounds[roundNum].eliminatedNames
        whatHappened = "{name} had the fewest votes and was eliminated. "
        return self._describe_list_of_names(eliminated, " eliminated", whatHappened)

    def _describe_transfers_this_round(self, roundNum):
        """ e.g. "Foo had the fewest votes and was eliminated. "
            Returns empty string if nobody was eliminated.
            Note that we look at the next round for eliminations, so it
            lines up with the visualizations."""
        rounds = self.graph.summarize().rounds
        transfers = rounds[roundNum].eliminatedNames
        whatHappened = "People who voted for {name} had their votes "\
                       "transferred to their next choice. "
        return self._describe_list_of_names(transfers, " transferred votes", whatHappened)

    def _describe_redistribution_this_round(self, roundNum):
        """ Describes redistribution, if there was any.
            Returns empty string if there wasn't. """
        redistributionData = common.get_redistribution_data(self.graph, roundNum)
        redistributedNames = redistributionData['names']
        redistributedSum = redistributionData['sum']

        surplusNumVotes = common.intify_or_aboutify(redistributedSum)
        whatHappened = "{name} had more than enough votes to win, so to ensure no vote is wasted, "\
            f"{surplusNumVotes} surplus votes were redistributed to other candidates. "
        return self._describe_list_of_names(
            redistributedNames, " redistributed votes", whatHappened)

    def _describe_winners_this_round(self, roundNum):
        """ e.g. "Foo reached the threshold of X and was elected. "
            Returns empty string if there wasn't a winner. """
        rounds = self.graph.summarize().rounds
        winners = rounds[roundNum].winnerNames

        # Note: each event shows just one winner. If there are multiple winners,
        # there will be multiple sentences in the main vis. (Not true in the video...)
        # So, set numWinners to 1, not len(winners)
        event = textForWinnerUtils.as_event(self.config, 1)

        if self.graph.threshold is not None:
            thresholdString = intify(self.graph.threshold)
            whatHappened = "{name} reached the threshold of "\
                f"{thresholdString} votes and {event}. "
        else:
            whatHappened = "{name} " + event + ". "
        return self._describe_list_of_names(winners, " won", whatHappened)

    @classmethod
    def _describe_first_round(cls, roundNum):
        if roundNum != 0:
            return []

        return [{"summary": "Initial votes",
                 "description": "The results of everybody's first-choice candidates. ",
                 "verb": "initial"}]

    def describe_round(self, roundNum):
        """ Returns a long string of all the interesting things that happened this round. """
        if self.summarizeAsParagraph:
            result = ''.join([func(roundNum) for func in self.textOnlyDescribers])
        else:
            result = []
            for func in self.listOnlyDescribers:
                result += func(roundNum)
        return result

    def describe_all_rounds(self):
        """ Returns an array corresponding to the description of each round """
        return [self.describe_round(i) for i in range(self.graph.numRounds)]

    def describe_initial_summary(self, isForVideo):
        """ Summarizes the entire election. """
        summary = self.graph.summarize()
        winners = [winner for round in summary.rounds for winner in round.winnerNames]
        numRounds = len(summary.rounds)

        if len(winners) == 0:
            return "This election does not have any winners, "\
                   "perhaps because the results are still preliminary. "

        # Initial summary is always just text
        try:
            originalSummarizeAsParagraph = self.summarizeAsParagraph
            self.summarizeAsParagraph = True
            event = textForWinnerUtils.as_event(self.config, len(winners))
            winnerText = self._describe_list_of_names(winners, None, "{name} " + event)
        finally:
            self.summarizeAsParagraph = originalSummarizeAsParagraph

        if len(winners) > 1:
            electionType = "Proportional, Multi-Winner Ranked Choice Voting election"
        else:
            electionType = "Ranked Choice Voting election"

        if isForVideo:
            wereOrWas = "was" if numRounds == 1 else "were"
            text = f"In this {electionType}, there {wereOrWas} {numRounds} rounds, "\
                   f"after which {winnerText}. Here's what happened in each round. "
        else:
            text = f"After {numRounds} rounds of this {electionType}, "\
                   f"{winnerText}. Move the slider to see what happened in each round."

        return text
