"""
MBTI Test Question Bank

This module contains the cognitive function test questions and their mappings.
Questions are designed to measure the 8 cognitive functions
(Ni, Ne, Si, Se, Ti, Te, Fi, Fe) through real-world scenarios
without revealing the function type to users.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class CognitiveFunction(Enum):
    """Cognitive function types"""

    NI = "Ni"  # Introverted Intuition
    NE = "Ne"  # Extraverted Intuition
    SI = "Si"  # Introverted Sensing
    SE = "Se"  # Extraverted Sensing
    TI = "Ti"  # Introverted Thinking
    TE = "Te"  # Extraverted Thinking
    FI = "Fi"  # Introverted Feeling
    FE = "Fe"  # Extraverted Feeling


@dataclass
class Question:
    """Question entity for MBTI test"""

    id: str
    text: str
    function_type: CognitiveFunction


# Question bank data
QUESTIONS = [
    # Ni (Introverted Intuition) questions
    Question(
        id="Ni_1",
        text=(
            "You sketch a one-page roadmap that shows where the team will be "
            "in six months and work backward to today's first step."
        ),
        function_type=CognitiveFunction.NI,
    ),
    Question(
        id="Ni_2",
        text=(
            "You ignore a flashy quick win because you can already see how it "
            "creates rework later, and you quietly steer toward the durable option."
        ),
        function_type=CognitiveFunction.NI,
    ),
    Question(
        id="Ni_3",
        text=(
            "Reading a few scattered metrics, you infer the core trend and "
            "propose a pivot before anyone else names it."
        ),
        function_type=CognitiveFunction.NI,
    ),
    Question(
        id="Ni_4",
        text=(
            "You block an hour of quiet, then emerge with a clear narrative "
            "that aligns everyone on the destination."
        ),
        function_type=CognitiveFunction.NI,
    ),
    Question(
        id="Ni_5",
        text=(
            "While others debate features, you describe the underlying customer "
            "journey arc and how each choice affects it long term."
        ),
        function_type=CognitiveFunction.NI,
    ),
    # Ne (Extraverted Intuition) questions
    Question(
        id="Ne_1",
        text=(
            "You turn a single customer request into five alternative concepts, "
            "whiteboarding connections no one had considered."
        ),
        function_type=CognitiveFunction.NE,
    ),
    Question(
        id="Ne_2",
        text=(
            "When the conversation stalls, you reframe the problem and spark "
            "a new round of ideas that energizes the group."
        ),
        function_type=CognitiveFunction.NE,
    ),
    Question(
        id="Ne_3",
        text=(
            "You spot a quirky use case from another industry and adapt it "
            "to your team's product."
        ),
        function_type=CognitiveFunction.NE,
    ),
    Question(
        id="Ne_4",
        text=(
            "You collect examples from podcasts, blogs, and competitors, "
            "then mash them into a fresh proposal."
        ),
        function_type=CognitiveFunction.NE,
    ),
    Question(
        id="Ne_5",
        text=(
            "Plans feel too tight, so you open the field, brainstorming "
            "bold what‑ifs before narrowing down."
        ),
        function_type=CognitiveFunction.NE,
    ),
    # Si (Introverted Sensing) questions
    Question(
        id="Si_1",
        text=(
            "You pull up last year's checklist and adjust it, ensuring "
            "proven steps aren't skipped."
        ),
        function_type=CognitiveFunction.SI,
    ),
    Question(
        id="Si_2",
        text=(
            "You notice the report's numbers don't match the usual format "
            "and correct them before they cause confusion."
        ),
        function_type=CognitiveFunction.SI,
    ),
    Question(
        id="Si_3",
        text=(
            "Faced with a new tool, you map it to a process you already "
            "know so everyone can follow reliably."
        ),
        function_type=CognitiveFunction.SI,
    ),
    Question(
        id="Si_4",
        text=(
            "You keep versioned notes so the team can trace what changed " "and why."
        ),
        function_type=CognitiveFunction.SI,
    ),
    Question(
        id="Si_5",
        text=(
            "Rather than overhaul everything, you recommend small, steady "
            "tweaks that preserve what works."
        ),
        function_type=CognitiveFunction.SI,
    ),
    # Se (Extraverted Sensing) questions
    Question(
        id="Se_1",
        text=(
            "You walk the shop floor, spot a bottleneck in real time, and "
            "move people to clear it immediately."
        ),
        function_type=CognitiveFunction.SE,
    ),
    Question(
        id="Se_2",
        text=(
            "In a live demo glitch, you stay calm, troubleshoot on the spot, "
            "and keep the audience engaged."
        ),
        function_type=CognitiveFunction.SE,
    ),
    Question(
        id="Se_3",
        text=(
            "You test the prototype hands‑on, noticing a subtle haptic issue "
            "others missed from the spreadsheet."
        ),
        function_type=CognitiveFunction.SE,
    ),
    Question(
        id="Se_4",
        text=(
            "During a negotiation, you read the room, shift tone, and seize "
            "the moment to close."
        ),
        function_type=CognitiveFunction.SE,
    ),
    Question(
        id="Se_5",
        text=(
            "Weather turns mid‑hike, you adjust the route and pace so the "
            "group finishes safely."
        ),
        function_type=CognitiveFunction.SE,
    ),
    # Ti (Introverted Thinking) questions
    Question(
        id="Ti_1",
        text=(
            "You define terms precisely, untangling a debate by separating "
            "assumptions from facts."
        ),
        function_type=CognitiveFunction.TI,
    ),
    Question(
        id="Ti_2",
        text=(
            "You rebuild the logic of the pricing model and find a "
            "contradiction that fixes downstream errors."
        ),
        function_type=CognitiveFunction.TI,
    ),
    Question(
        id="Ti_3",
        text=(
            "You design a minimalist framework that explains all edge cases "
            "without special rules."
        ),
        function_type=CognitiveFunction.TI,
    ),
    Question(
        id="Ti_4",
        text=(
            "Before agreeing, you stress‑test the idea with counterexamples "
            "until the argument holds."
        ),
        function_type=CognitiveFunction.TI,
    ),
    Question(
        id="Ti_5",
        text=(
            "You refactor a messy process into clear decision criteria "
            "that anyone can apply."
        ),
        function_type=CognitiveFunction.TI,
    ),
    # Te (Extraverted Thinking) questions
    Question(
        id="Te_1",
        text=(
            "You set a two‑week plan with owners, timelines, and a dashboard "
            "everyone can see."
        ),
        function_type=CognitiveFunction.TE,
    ),
    Question(
        id="Te_2",
        text=(
            "When blockers appear, you escalate early and reassign tasks "
            "to keep delivery on track."
        ),
        function_type=CognitiveFunction.TE,
    ),
    Question(
        id="Te_3",
        text=(
            "You standardize the intake form so requests are comparable "
            "and easy to prioritize."
        ),
        function_type=CognitiveFunction.TE,
    ),
    Question(
        id="Te_4",
        text=(
            "You choose a simpler tool that automates the busywork and "
            "improves throughput."
        ),
        function_type=CognitiveFunction.TE,
    ),
    Question(
        id="Te_5",
        text=(
            "You define success metrics and run a weekly review to "
            "course‑correct quickly."
        ),
        function_type=CognitiveFunction.TE,
    ),
    # Fi (Introverted Feeling) questions
    Question(
        id="Fi_1",
        text=(
            "You decline a lucrative partnership because the messaging "
            "conflicts with your values."
        ),
        function_type=CognitiveFunction.FI,
    ),
    Question(
        id="Fi_2",
        text=(
            "You take time to check how a decision sits with your conscience "
            "before giving a firm yes."
        ),
        function_type=CognitiveFunction.FI,
    ),
    Question(
        id="Fi_3",
        text=(
            "You back a quieter teammate whose idea feels deeply right, "
            "even if it's not trendy."
        ),
        function_type=CognitiveFunction.FI,
    ),
    Question(
        id="Fi_4",
        text=(
            "You set a boundary about after‑hours work to protect "
            "well‑being and meaning."
        ),
        function_type=CognitiveFunction.FI,
    ),
    Question(
        id="Fi_5",
        text=(
            "You choose a solution that preserves dignity for an affected "
            "group, even at extra cost."
        ),
        function_type=CognitiveFunction.FI,
    ),
    # Fe (Extraverted Feeling) questions
    Question(
        id="Fe_1",
        text=(
            "You notice tension in the room, invite each voice in, and guide "
            "the group to a shared outcome."
        ),
        function_type=CognitiveFunction.FE,
    ),
    Question(
        id="Fe_2",
        text=("You rephrase a harsh comment so it's heard, keeping trust " "intact."),
        function_type=CognitiveFunction.FE,
    ),
    Question(
        id="Fe_3",
        text=(
            "You organize expectations clearly and check that everyone "
            "feels the plan is fair."
        ),
        function_type=CognitiveFunction.FE,
    ),
    Question(
        id="Fe_4",
        text=(
            "You mediate a conflict by naming the unspoken needs and "
            "proposing ground rules."
        ),
        function_type=CognitiveFunction.FE,
    ),
    Question(
        id="Fe_5",
        text=(
            "You craft an announcement that anticipates reactions and "
            "keeps the team aligned."
        ),
        function_type=CognitiveFunction.FE,
    ),
]


def get_all_questions() -> List[Question]:
    """Get all questions in the bank"""
    return QUESTIONS.copy()


def get_questions_by_function(function_type: CognitiveFunction) -> List[Question]:
    """Get all questions for a specific cognitive function"""
    return [q for q in QUESTIONS if q.function_type == function_type]


def get_question_by_id(question_id: str) -> Optional[Question]:
    """Get a specific question by ID"""
    for question in QUESTIONS:
        if question.id == question_id:
            return question
    return None


def get_randomized_questions() -> List[Dict[str, str]]:
    """
    Get questions in randomized order without revealing function types.
    Returns list of dicts with only id and text for frontend display.
    """
    import random

    # Create a copy and shuffle
    shuffled_questions = QUESTIONS.copy()
    random.shuffle(shuffled_questions)

    # Return only id and text (hide function_type)
    return [
        {"id": question.id, "text": question.text} for question in shuffled_questions
    ]


def get_function_type_for_question(question_id: str) -> Optional[CognitiveFunction]:
    """Get the cognitive function type for a specific question (for scoring)"""
    question = get_question_by_id(question_id)
    return question.function_type if question else None


def get_total_questions_count() -> int:
    """Get total number of questions in the bank"""
    return len(QUESTIONS)


def get_questions_per_function() -> Dict[CognitiveFunction, int]:
    """Get count of questions per cognitive function"""
    counts = {}
    for function in CognitiveFunction:
        counts[function] = len(get_questions_by_function(function))
    return counts


# Validation function to ensure data integrity
def validate_question_bank() -> bool:
    """Validate that all questions have proper data"""
    for question in QUESTIONS:
        if not question.id or not question.text or not question.function_type:
            return False
        if not isinstance(question.function_type, CognitiveFunction):
            return False
    return True


if __name__ == "__main__":
    # Test the question bank
    print(f"Total questions: {get_total_questions_count()}")
    print(f"Questions per function: {get_questions_per_function()}")
    print(f"Question bank validation: {validate_question_bank()}")

    # Test randomization
    print("\nRandomized questions (first 3):")
    random_questions = get_randomized_questions()[:3]
    for q in random_questions:
        print(f"- {q['id']}: {q['text'][:50]}...")
