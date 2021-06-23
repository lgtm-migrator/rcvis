"""
Helper functions for dealing with JsonConfig.textForWinner
No if/else switches for these should be placed anywhere else
in the codebase: when we add more, we'd like one central place for
all of them.
"""

from visualizer.models import TextForWinner
from visualizer.descriptors.common import comma_separated_names_with_and


def as_caption(config):
    """
    Depending on TextForWinner, creates a different caption or title
    to be used in cells describing the winner
    """
    if config.textForWinner == TextForWinner.ELECTED:
        return "Elected"
    if config.textForWinner == TextForWinner.WON:
        return "Won"
    if config.textForWinner == TextForWinner.PRIMARY:
        return "Advanced"

    raise RuntimeError("Unsupported TextForWinner.")


def as_sentence(config, names):
    """
    Describes the winner or list of winners, respecting the config option for
    how to refer to winners
    """
    nameText = comma_separated_names_with_and(names)
    if config.textForWinner == TextForWinner.ELECTED:
        wereOrWas = "was" if len(names) == 1 else "were"
        return f"{nameText} {wereOrWas} elected"
    if config.textForWinner == TextForWinner.WON:
        return f"{nameText} won"
    if config.textForWinner == TextForWinner.PRIMARY:
        return f"{nameText} advanced to the general"

    raise RuntimeError("Unsupported TextForWinner.")


def as_question(config, names):
    """
    A question asking why the winners won
    """
    nameText = comma_separated_names_with_and(names)
    if config.textForWinner == TextForWinner.ELECTED:
        wereOrWas = "was" if len(names) == 1 else "were"
        return f"Why {wereOrWas} {nameText} elected?"
    if config.textForWinner == TextForWinner.WON:
        return f"Why did {nameText} win?"
    if config.textForWinner == TextForWinner.PRIMARY:
        return f"Why did {nameText} advanced to the general?"

    raise RuntimeError("Unsupported TextForWinner.")


def as_present_perfect_tense(config, numWinners):
    """
    Describes what happens to winners as past tense ("have been...")
    """
    haveOrHas = "has" if numWinners == 1 else "have"
    if config.textForWinner == TextForWinner.ELECTED:
        return f"{haveOrHas} been elected"
    if config.textForWinner == TextForWinner.WON:
        return f"{haveOrHas} won"
    if config.textForWinner == TextForWinner.PRIMARY:
        return f"{haveOrHas} advanced to the general"

    raise RuntimeError("Unsupported TextForWinner.")
