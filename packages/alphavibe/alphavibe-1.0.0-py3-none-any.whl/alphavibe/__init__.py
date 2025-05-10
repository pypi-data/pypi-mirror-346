# alphavibe/__init__.py

import builtins
import re
# 🌈 Gen Alpha to Python Dictionary 
TRANSLATION = {
    r"\bvibe\b": "def",
    r"\bsus\b": "if",
    r"\bextraSus\b": "elif",
    r"\bnoCap\b": "else",
    r"\bzoom\b": "for",
    r"\bloopUntilBored\b": "while",
    r"\bspitItOut\b": "print",
    r"\bbounce\b": "return",
    r"\bfacts\b": "True",
    r"\bnah\b": "False",
    r"\bghost\b": "None",
    r"\&also\b": "and",
    r"\bmaybe\b": "or",
    r"\bthat\b": "not",
    r"\bamong\b": "in",
    r"\bsameVibe\b": "is",
    r"\bsquad\b": "class",
    r"\bbringIn\b": "import",
    r"\baka\b": "as",
    r"\bcook\b": "try",
    r"\bcatchFlop\b": "except",
    r"\bthrowDrama\b": "raise",
    r"\blockedIn\b": "with",
    r"\bmultiSlay\b": "async",
    r"\bholdUp\b": "await",
    r"\bspillTea\b": "input",
    r"\bvibeCheck\b": "len",
    r"\bslay\b": "exit",
    r"\bbet\b": "break",
    r"\bsussy\b": "continue",
    r"\bsussOut\b": "pass",
    r"\balpha\b": "def main",
    r"\bbeta\b": "def __init__",
    r"\bsigma\b": "def __str__",
    r"\bglowUp\b": "global",
    r"\blowKey\b": "nonlocal",
    r"\bbigMood\b": "True",
    r"\bnoMood\b": "False",
    r"\bchill\b": "pass",
    r"\bhype\b": "assert",
    r"\bdrip\b": "yield",
    r"\bflex\b": "lambda",
    r"\bsquadGoals\b": "super",
    r"\bmainCharacter\b": "__name__",
    r"\bplotTwist\b": "__init__",
    r"\bendGame\b": "__del__",
    r"\bbigBrain\b": "isinstance",
    r"\bsameEnergy\b": "issubclass",
    r"\bdeepDive\b": "open",
    r"\bteaSpill\b": "print",
    r"\bscreenshot\b": "repr",
    r"\bvibeShift\b": "set",
    r"\bsquadUp\b": "dict",
    r"\bsquadList\b": "list",
    r"\bsquadGoalsList\b": "tuple",
    r"\bsquadVibes\b": "set",
    r"\bsquadKeys\b": "keys",
    r"\bsquadValues\b": "values",
    r"\bsquadItems\b": "items",
    r"\bsquadPop\b": "pop",
    r"\bsquadAdd\b": "add",
    r"\bsquadRemove\b": "remove",
    r"\bsquadClear\b": "clear",
    r"\bsquadUpdate\b": "update",
    r"\bbigFlex\b": "map",
    r"\bbigZoom\b": "filter",
    r"\bbigDrip\b": "reduce",
    r"\bbigBet\b": "enumerate",
    r"\bbigTea\b": "zip",
    r"\bbigVibes\b": "sorted",
    r"\bbigChill\b": "reversed",
    r"\bbigGlowUp\b": "globals",
    r"\bbigLowKey\b": "locals",
    r"\bbigPlotTwist\b": "staticmethod",
    r"\bbigSquadGoals\b": "classmethod",
    r"\bbigMainCharacter\b": "__main__",
    r"\bbigFacts\b": "True",
    r"\bbigNah\b": "False",
    r"\bbigGhost\b": "None",
    r"\bbigCook\b": "try",
    r"\bbigCatchFlop\b": "except",
    r"\bbigThrowDrama\b": "raise",
    r"\bbigLockedIn\b": "with",
    r"\bbigMultiSlay\b": "async",
    r"\bbigHoldUp\b": "await",
    r"\bbigSussy\b": "continue",
    r"\bbigBetBet\b": "break",
    r"\bbigSussOut\b": "pass"
}
FORBIDDEN = [
    "def", "if", "for", "while", "return", "print", "try", "except",
    "class", "import", "input", "async", "await", "with", "raise",
    "len", "exit", "break", "continue", "pass"
]
REVERSE_TRANSLATION = {v: re.sub(r"\\b", "", k) for k, v in TRANSLATION.items()}
def block_boomer_builtins():
    """🚫 No Boomer Python allowed."""
    forbidden = [
        "def", "if", "for", "while", "return", "print", "try", "except",
        "class", "import", "input", "async", "await", "with", "raise",
        "len", "exit", "break", "continue", "pass"
    ]
    for word in forbidden:
        if word == "def":
            # Special case for def to avoid invalid syntax error
            exec(f"def {word}_boom(*args, **kwargs): raise SyntaxError('🚫 Gen Alpha only. No `{word}` allowed. Use the vibe.')", globals())
        else:
            exec(f"def {word}(*args, **kwargs): raise SyntaxError('🚫 Gen Alpha only. No `{word}` allowed. Use the vibe.')", globals())

def alphaRun(code: str):
    """
    Translates Gen Alpha code into Python, checks for forbidden syntax, then executes it.
    """
    lines = code.splitlines()
    for i, line in enumerate(lines, start=1):
        for word in FORBIDDEN:
            if re.search(rf"\\b{word}\\b", line):
                suggestion = REVERSE_TRANSLATION.get(word, "🧃 [no Gen Alpha slang known]")
                print(f"🚫 Boomer code at line {i}: `{word}` found.\n💡 Did you mean `{suggestion}` instead?\n")

    for ga_pattern, py_keyword in TRANSLATION.items():
        code = re.sub(ga_pattern, py_keyword, code)

    exec(code, globals())
builtins.spillTea = input
builtins.spitItOut = print
builtins.vibeCheck = len
block_boomer_builtins()
