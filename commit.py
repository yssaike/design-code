#!/usr/bin/env python3
"""
Design Code — Daily commit script for design engineers.
Run this from your terminal each day to log design work to GitHub.
"""

import argparse
import os
import random
import subprocess
import sys
import time
import json
from datetime import datetime, date, timedelta

# ---------------------------------------------------------------------------
# Design-themed commit messages grouped by category
# ---------------------------------------------------------------------------
COMMIT_MESSAGES = {
    "color": [
        "primary color update",
        "secondary palette refinement",
        "accent color adjustment",
        "color contrast fix",
        "dark mode color tweak",
        "color palette expansion",
        "brand color alignment",
        "surface color update",
        "semantic color token fix",
        "update neutral palette to reflect new brand direction",
        "fix off-brand blue in CTA components",
        "tweak surface colors for better light-mode legibility",
        "remap semantic color tokens to new primitives",
        "sync color tokens with latest Figma variables export",
        "bump gray scale contrast levels",
        "adjust alpha values on overlay tokens",
        "patch inconsistent error color across states",
        "align info color with accessibility requirements",
        "refine success and warning color tokens",
        "update background color for elevated surfaces",
    ],
    "brand": [
        "brand token change",
        "brand font update",
        "brand spacing alignment",
        "brand asset refresh",
        "brand guideline sync",
        "sync brand tokens with latest identity refresh",
        "update logo sizing constraints",
        "pull latest brand variables from design system",
        "align brand palette with updated guidelines",
        "refresh brand gradient values",
        "update wordmark sizing token",
        "reconcile brand color with new creative direction",
    ],
    "typography": [
        "typography scale update",
        "font weight adjustment",
        "line height refinement",
        "heading hierarchy fix",
        "body text improvement",
        "font family swap",
        "letter spacing tweak",
        "normalize font stack across platforms",
        "fix responsive type scale breakpoints",
        "update display heading tokens",
        "audit and clean up unused type styles",
        "bump body font size for readability",
        "align caption text tokens with spec",
        "tighten heading line height for large screens",
        "update monospace font token",
        "add fluid type scale tokens",
        "fix missing italic weight token",
    ],
    "spacing": [
        "spacing token update",
        "padding consistency fix",
        "margin alignment",
        "grid gap adjustment",
        "layout spacing refinement",
        "section spacing update",
        "normalize spacing scale to 8pt grid",
        "fix inconsistent inner padding on form elements",
        "audit spacing tokens for duplicate values",
        "tighten compact density spacing",
        "update page-level layout margins",
        "add missing spacing token for inline elements",
        "fix content spacing inside card variants",
        "align vertical rhythm tokens with type scale",
    ],
    "components": [
        "button style update",
        "input field refinement",
        "card component update",
        "modal design update",
        "tooltip design tweak",
        "navigation styling fix",
        "dropdown menu update",
        "checkbox style refresh",
        "tab component refinement",
        "badge design update",
        "update link component underline style",
        "refine avatar sizing tokens",
        "fix icon size inconsistency in nav",
        "clean up form field error state styles",
        "refresh skeleton loader animation timing",
        "adjust chip component padding",
        "fix inline alert padding",
        "update stepper component tokens",
        "refine popover arrow token values",
        "patch divider component thickness",
        "update progress bar color tokens",
        "tighten list item component spacing",
        "update switch component track tokens",
        "fix breadcrumb separator sizing",
        "refine table row hover state tokens",
    ],
    "ui_fixes": [
        "hover state fix",
        "focus ring update",
        "active state refinement",
        "disabled state styling",
        "responsive layout tweak",
        "border radius update",
        "shadow refinement",
        "z-index adjustment",
        "overflow fix",
        "alignment correction",
        "visual regression fix",
        "fix broken outline on focus for keyboard users",
        "patch stacking context issue in overlay",
        "correct misaligned icon in button component",
        "fix ghost button hover color",
        "resolve visual glitch in dark mode",
        "patch spacing regression from last merge",
        "clean up leftover debug border",
        "fix clipped text in compact variant",
        "resolve color bleed on adjacent components",
        "fix broken transition on theme toggle",
        "patch off-by-one pixel alignment in grid",
        "fix missing border on selected state",
        "correct elevation token on sticky header",
        "patch inconsistent corner radius in form inputs",
    ],
    "motion": [
        "animation duration update",
        "transition easing change",
        "micro-interaction refinement",
        "loading animation tweak",
        "scroll animation fix",
        "add entrance animation for modal overlay",
        "smooth out tab transition timing",
        "remove jarring jump in accordion open",
        "refine easing curve on drawer slide",
        "update stagger delay for list animations",
        "tune reduced-motion fallback tokens",
        "fix bounce effect on toast notification",
        "normalize exit animation duration tokens",
        "update skeleton shimmer timing",
    ],
    "accessibility": [
        "accessibility contrast fix",
        "focus indicator update",
        "screen reader label add",
        "aria attribute update",
        "keyboard navigation fix",
        "improve color contrast on disabled text",
        "add skip-to-content link tokens",
        "fix missing label on icon-only button",
        "update focus-visible styles for interactive elements",
        "ensure touch target meets 44px minimum",
        "audit color pairs for WCAG AA compliance",
        "patch low-contrast placeholder text",
        "add high-visibility focus token for forced-colors mode",
    ],
    "refactor": [
        "clean up token naming inconsistencies",
        "reorganize token file structure",
        "remove deprecated spacing tokens",
        "consolidate duplicate component tokens",
        "rename tokens to match new naming convention",
        "flatten nested token structure for clarity",
        "split color tokens into primitives and semantics",
        "move hardcoded values to tokens",
        "deduplicate shadow definitions",
        "normalize token key casing",
        "extract repeated values into shared base tokens",
        "tidy up token category groupings",
    ],
    "tooling": [
        "update design token build script",
        "fix token export pipeline",
        "update Figma token sync config",
        "improve token validation script",
        "bump token schema version",
        "add token format checks to pre-commit",
        "fix broken token transformer",
        "clean up generated output artifacts",
        "update style dictionary config",
        "fix output path in token build config",
    ],
    "docs": [
        "update token documentation",
        "add usage examples to component tokens",
        "document new color semantics",
        "update changelog format",
        "add inline docs to spacing scale",
        "document token alias conventions",
        "update README with latest token structure",
        "add migration notes for renamed tokens",
        "document dark mode token usage",
        "add token decision rationale to comments",
    ],
    "tokens": [
        "export latest tokens from Figma",
        "resolve token alias circular references",
        "add missing dark mode token variants",
        "add new surface token for overlay backgrounds",
        "patch broken token reference in components",
        "add responsive token breakpoints",
        "add high-contrast mode token set",
        "update token output format to CSS variables",
        "sync token schema with style dictionary config",
        "add compact density token tier",
        "wire up new semantic elevation tokens",
        "add focus token for custom components",
    ],
}

# Flatten for easy random selection
ALL_MESSAGES = [msg for group in COMMIT_MESSAGES.values() for msg in group]

# ---------------------------------------------------------------------------
# Combinatorial message generation
#
# The curated lists above read well but top out at ~170 messages. At 20-30
# commits a day a 3-week cooldown needs 400-600+ distinct messages, so the
# curated pool alone gets exhausted and messages start repeating within days.
# The vocabulary below composes into tens of thousands of natural-sounding
# messages, which keeps the cooldown window genuinely collision-free.
# ---------------------------------------------------------------------------

ELEMENTS = [
    "button", "input", "card", "modal", "tooltip", "nav", "dropdown",
    "checkbox", "tab", "badge", "avatar", "chip", "alert", "popover",
    "divider", "progress bar", "switch", "breadcrumb", "table row", "toast",
    "drawer", "accordion", "stepper", "slider", "radio group", "select",
    "textarea", "skeleton", "spinner", "pagination", "sidebar", "page header",
    "footer", "banner", "menu item", "list item", "tag", "icon button",
    "link", "form field", "search bar", "empty state", "dialog", "snackbar",
    "date picker", "file upload", "segmented control", "tree view",
]

PROPERTIES = [
    "padding", "border radius", "shadow", "hover state", "focus ring",
    "disabled state", "active state", "color token", "spacing", "font size",
    "line height", "border color", "background", "elevation", "transition",
    "gap", "min-width", "text color", "icon size", "alignment",
    "letter spacing", "outline", "opacity", "max-height", "font weight",
    "placeholder color", "divider color", "selected state", "loading state",
]

CONTEXTS = [
    "in dark mode", "on mobile", "at small breakpoints", "in compact density",
    "in the sidebar", "in nested layouts", "for RTL layouts",
    "in high-contrast mode", "in form layouts", "on touch devices",
    "in the settings view", "at tablet widths", "in the mobile nav",
    "for long content", "in modal context", "on wide screens",
]

SCALES = ["spacing", "type", "elevation", "radius", "color", "z-index", "opacity", "density"]

TOKEN_KINDS = [
    "color", "spacing", "typography", "radius", "shadow", "motion",
    "elevation", "border", "semantic", "primitive",
]

FIX_VERBS = ["fix", "patch", "correct", "resolve"]
TWEAK_VERBS = ["update", "tweak", "adjust", "refine", "tune", "polish", "normalize"]


def _g_fix_element():
    """e.g. 'fix dropdown alignment on mobile'"""
    msg = f"{random.choice(FIX_VERBS)} {random.choice(ELEMENTS)} {random.choice(PROPERTIES)}"
    if random.random() < 0.45:
        msg += f" {random.choice(CONTEXTS)}"
    return random.choice(["ui_fixes", "components"]), msg


def _g_tweak_element():
    """e.g. 'refine card shadow in dark mode'"""
    msg = f"{random.choice(TWEAK_VERBS)} {random.choice(ELEMENTS)} {random.choice(PROPERTIES)}"
    if random.random() < 0.4:
        msg += f" {random.choice(CONTEXTS)}"
    return "components", msg


def _g_scale():
    """e.g. 'tighten up the elevation scale'"""
    verb = random.choice(TWEAK_VERBS + ["rebalance", "simplify", "extend"])
    return random.choice(["spacing", "typography", "tokens"]), f"{verb} the {random.choice(SCALES)} scale"


def _g_token_work():
    """e.g. 'add missing motion token for drawer'"""
    kind = random.choice(TOKEN_KINDS)
    choice = random.randint(0, 4)
    if choice == 0:
        return "tokens", f"add missing {kind} token for {random.choice(ELEMENTS)}"
    if choice == 1:
        return "refactor", f"remove unused {kind} tokens"
    if choice == 2:
        return "refactor", f"rename {kind} tokens for consistency"
    if choice == 3:
        return "refactor", f"consolidate duplicate {kind} tokens"
    return "docs", f"document {kind} token usage"


def _g_a11y():
    """e.g. 'improve focus ring contrast on icon button'"""
    choice = random.randint(0, 3)
    el = random.choice(ELEMENTS)
    if choice == 0:
        msg = f"improve {random.choice(['contrast', 'focus visibility', 'touch target size'])} on {el}"
    elif choice == 1:
        msg = f"add aria label to {el}"
    elif choice == 2:
        msg = f"fix keyboard navigation in {el}"
    else:
        msg = f"meet WCAG AA contrast on {el}"
    return "accessibility", msg


def _g_motion():
    """e.g. 'ease the drawer transition timing'"""
    el = random.choice(ELEMENTS)
    choice = random.randint(0, 2)
    if choice == 0:
        msg = f"{random.choice(TWEAK_VERBS)} {el} transition timing"
    elif choice == 1:
        msg = f"soften {el} {random.choice(['entrance', 'exit', 'hover'])} animation"
    else:
        msg = f"respect reduced motion in {el}"
    return "motion", msg


GENERATORS = [
    (_g_fix_element, 26),
    (_g_tweak_element, 26),
    (_g_scale, 8),
    (_g_token_work, 16),
    (_g_a11y, 10),
    (_g_motion, 14),
]

# Occasionally prefix with a conventional-commit type, the way a solo dev
# drifts between styles over a long-running project.
PREFIXES = {
    "ui_fixes": "fix", "components": "style", "accessibility": "a11y",
    "motion": "style", "tokens": "feat", "refactor": "refactor",
    "docs": "docs", "spacing": "style", "typography": "style",
    "color": "style", "brand": "style", "tooling": "chore",
}


def _prefix_for(category: str, message: str):
    """Pick a conventional-commit prefix, or None when one would read oddly."""
    first = message.split()[0]
    # "fix: patch ..." is redundant — the verb already says it.
    if first in FIX_VERBS:
        return None
    if first == "document":
        return "docs"
    return PREFIXES.get(category)


def _generate():
    """Compose a fresh message from the vocabulary. Returns (category, message)."""
    gens, weights = zip(*GENERATORS)
    category, message = random.choices(gens, weights=weights, k=1)[0]()
    if random.random() < 0.18:
        prefix = _prefix_for(category, message)
        if prefix:
            message = f"{prefix}: {message}"
    return category, message


# ---------------------------------------------------------------------------
# Cooldown tracking — avoids repeating the same message within 3 weeks
# ---------------------------------------------------------------------------
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".commit_history.json")
COOLDOWN_DAYS = 21


def _load_history() -> dict:
    if not os.path.exists(HISTORY_FILE):
        return {}
    try:
        with open(HISTORY_FILE) as f:
            history = json.load(f)
    except (json.JSONDecodeError, OSError):
        # A corrupt history file should never block a commit run.
        return {}

    # Drop entries past the cooldown window — they no longer constrain
    # anything, and pruning keeps the file from growing without bound now
    # that messages are generated rather than drawn from a fixed list.
    today = date.today()
    fresh = {}
    for msg, stamp in history.items():
        try:
            if (today - datetime.strptime(stamp, "%Y-%m-%d").date()).days < COOLDOWN_DAYS:
                fresh[msg] = stamp
        except (ValueError, TypeError):
            continue
    return fresh


def _save_history(history: dict) -> None:
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def _is_on_cooldown(message: str, history: dict) -> bool:
    if message not in history:
        return False
    last_used = datetime.strptime(history[message], "%Y-%m-%d").date()
    return (date.today() - last_used).days < COOLDOWN_DAYS


def _record_usage(message: str, history: dict) -> None:
    history[message] = date.today().isoformat()


# ---------------------------------------------------------------------------
# File-modification helpers — each one touches a different token file so
# the diffs look realistic in GitHub.
# ---------------------------------------------------------------------------

def _modify_colors(tokens_dir: str) -> None:
    path = os.path.join(tokens_dir, "colors.json")
    with open(path) as f:
        data = json.load(f)

    shades = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(3)]
    key = random.choice(list(data.keys()))
    if isinstance(data[key], dict):
        sub = random.choice(list(data[key].keys()))
        data[key][sub] = random.choice(shades)
    else:
        data[key] = random.choice(shades)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def _modify_typography(tokens_dir: str) -> None:
    path = os.path.join(tokens_dir, "typography.json")
    with open(path) as f:
        data = json.load(f)

    weights = [300, 400, 500, 600, 700]
    sizes = ["0.75rem", "0.875rem", "1rem", "1.125rem", "1.25rem", "1.5rem", "2rem", "2.5rem", "3rem"]
    heights = ["1.2", "1.4", "1.5", "1.6", "1.75"]

    key = random.choice(list(data.keys()))
    prop = random.choice(["fontSize", "fontWeight", "lineHeight"])
    if prop == "fontSize":
        data[key][prop] = random.choice(sizes)
    elif prop == "fontWeight":
        data[key][prop] = random.choice(weights)
    else:
        data[key][prop] = random.choice(heights)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def _modify_spacing(tokens_dir: str) -> None:
    path = os.path.join(tokens_dir, "spacing.json")
    with open(path) as f:
        data = json.load(f)

    key = random.choice(list(data.keys()))
    base = random.choice([2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64])
    data[key] = f"{base}px"

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def _modify_components(tokens_dir: str) -> None:
    path = os.path.join(tokens_dir, "components.json")
    with open(path) as f:
        data = json.load(f)

    component = random.choice(list(data.keys()))
    prop = random.choice(list(data[component].keys()))
    if "radius" in prop.lower():
        data[component][prop] = f"{random.choice([2, 4, 6, 8, 12, 16, 24, 9999])}px"
    elif "shadow" in prop.lower():
        x = random.randint(0, 4)
        y = random.randint(1, 8)
        blur = random.randint(4, 24)
        alpha = round(random.uniform(0.04, 0.2), 2)
        data[component][prop] = f"{x}px {y}px {blur}px rgba(0,0,0,{alpha})"
    elif "padding" in prop.lower() or "gap" in prop.lower():
        data[component][prop] = f"{random.choice([4, 8, 12, 16, 20, 24])}px"
    else:
        data[component][prop] = f"{random.choice([1, 2, 4, 8, 12, 16])}px"

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def _modify_random(tokens_dir: str) -> None:
    random.choice([_modify_colors, _modify_typography, _modify_spacing, _modify_components])(tokens_dir)


def _append_log(tokens_dir: str, message: str) -> None:
    log_path = os.path.join(tokens_dir, "..", "CHANGELOG.md")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(log_path, "a") as f:
        f.write(f"- `{timestamp}` — {message}\n")


# Map commit categories to file modifiers
MODIFIERS = {
    "color": _modify_colors,
    "brand": _modify_colors,
    "typography": _modify_typography,
    "spacing": _modify_spacing,
    "components": _modify_components,
    "ui_fixes": _modify_components,
    "motion": _modify_components,
    "accessibility": _modify_components,
    "refactor": _modify_random,
    "tooling": _modify_random,
    "docs": _modify_random,
    "tokens": _modify_random,
}


def _is_fresh(message: str, history: dict, session_used: set) -> bool:
    return message not in session_used and not _is_on_cooldown(message, history)


def _pick_commit(history: dict, session_used: set):
    """
    Return (category, message) that has not been used in the last
    COOLDOWN_DAYS days, nor already in this session.

    Prefers the hand-written pool while it still has unused entries, then
    falls back to composed messages, which are effectively unlimited.
    """
    # Hand-written messages read best, so use them first when available.
    curated = [
        (cat, msg) for cat, msgs in COMMIT_MESSAGES.items() for msg in msgs
        if _is_fresh(msg, history, session_used)
    ]
    if curated and random.random() < 0.35:
        return random.choice(curated)

    # Compose a fresh one. The vocabulary is large enough that a collision-free
    # draw lands almost immediately.
    for _ in range(200):
        category, message = _generate()
        if _is_fresh(message, history, session_used):
            return category, message

    # Vocabulary somehow saturated — fall back to any unused curated message.
    if curated:
        return random.choice(curated)

    # Last resort: disambiguate with a short suffix so we never repeat verbatim.
    category, message = _generate()
    return category, f"{message} ({date.today().strftime('%b %d').lower()})"


def _git(*args):
    result = subprocess.run(
        ["git"] + list(args),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 and result.stderr:
        print(f"  git {' '.join(args)}: {result.stderr.strip()}")
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

# Range used for unattended runs, so the daily count varies like real activity.
AUTO_MIN, AUTO_MAX = 4, 18


def _log(message: str, quiet: bool) -> None:
    """Print with a timestamp when running unattended, plainly when interactive."""
    if quiet:
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {message}", flush=True)
    else:
        print(message)


def _ask_count() -> int:
    while True:
        try:
            num = int(input("  How many commits would you like to make today? "))
            if num < 1:
                print("  Please enter at least 1.")
                continue
            return num
        except ValueError:
            print("  Enter a number, e.g. 3")


def run(num: int, push: bool = True, quiet: bool = False) -> int:
    """Create `num` commits and optionally push. Returns the exit code."""
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_dir)
    tokens_dir = os.path.join(repo_dir, "design_tokens")

    history = _load_history()
    session_used = set()
    made = 0

    for i in range(1, num + 1):
        category, message = _pick_commit(history, session_used)
        session_used.add(message)
        _record_usage(message, history)

        modifier = MODIFIERS.get(category, _modify_random)
        modifier(tokens_dir)
        _append_log(tokens_dir, message)

        _git("add", "-A")
        result = _git("commit", "-m", message)
        if result.returncode != 0:
            _log(f"  commit failed, stopping: {message}", quiet)
            break
        made += 1
        _log(f"  [{i}/{num}] ✓ {message}", quiet)

    # Save history even on a partial run so used messages stay on cooldown.
    _save_history(history)

    if made == 0:
        _log("  No commits were made.", quiet)
        return 1

    if not push:
        _log(f"  {made} commit(s) created. Skipping push (--no-push).", quiet)
        return 0

    _log("  Pushing to GitHub …", quiet)
    result = _git("push")
    if result.returncode == 0:
        _log(f"  Done! {made} commit{'s' if made != 1 else ''} pushed. Your graph just got greener 🟩", quiet)
        return 0

    # Leave the commits in place; the next run will push them along with its own.
    _log("  Push failed — commits are saved locally and will go out next run.", quiet)
    return 1


def main():
    parser = argparse.ArgumentParser(description="Design Code — design-token commit tool.")
    parser.add_argument("-n", "--count", type=int, help="number of commits to make")
    parser.add_argument("--auto", action="store_true",
                        help=f"unattended mode: random count ({AUTO_MIN}-{AUTO_MAX}), no prompts")
    parser.add_argument("--jitter", type=int, default=0, metavar="MIN",
                        help="sleep a random 0-MIN minutes before starting")
    parser.add_argument("--no-push", action="store_true", help="commit locally without pushing")
    args = parser.parse_args()

    unattended = args.auto or args.count is not None

    if not unattended:
        print()
        print("  ╔══════════════════════════════════════╗")
        print("  ║         🎨  Design Code  🎨          ║")
        print("  ║    Daily design-token commit tool     ║")
        print("  ╚══════════════════════════════════════╝")
        print()

    if args.jitter > 0:
        delay = random.randint(0, args.jitter * 60)
        _log(f"  Jitter: waiting {delay // 60}m {delay % 60}s before starting.", unattended)
        time.sleep(delay)

    num = args.count if args.count is not None else (
        random.randint(AUTO_MIN, AUTO_MAX) if args.auto else _ask_count()
    )
    if num < 1:
        parser.error("--count must be at least 1")

    if unattended:
        _log(f"Design Code: starting run of {num} commit(s).", True)
    else:
        print()

    code = run(num, push=not args.no_push, quiet=unattended)

    if not unattended:
        print()
    return code


if __name__ == "__main__":
    sys.exit(main())
