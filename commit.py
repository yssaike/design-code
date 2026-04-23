#!/usr/bin/env python3
"""
Design Code — Daily commit script for design engineers.
Run this from your terminal each day to log design work to GitHub.
"""

import os
import random
import subprocess
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
# Cooldown tracking — avoids repeating the same message within 3 weeks
# ---------------------------------------------------------------------------
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".commit_history.json")
COOLDOWN_DAYS = 21


def _load_history() -> dict:
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE) as f:
        return json.load(f)


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


def _pick_commit(history: dict, session_used: set):
    """
    Return (category, message), skipping messages on 21-day cooldown
    and messages already used this session.
    Falls back to least-recently-used if the pool is exhausted.
    """
    all_pairs = [(cat, msg) for cat, msgs in COMMIT_MESSAGES.items() for msg in msgs]
    available = [
        (cat, msg) for cat, msg in all_pairs
        if msg not in session_used and not _is_on_cooldown(msg, history)
    ]

    if not available:
        # Everything is on cooldown — pick the least recently used
        def last_used_date(pair):
            _, msg = pair
            return datetime.strptime(history.get(msg, "2000-01-01"), "%Y-%m-%d").date()

        all_pairs.sort(key=last_used_date)
        # Filter out at least session dupes if possible
        filtered = [p for p in all_pairs if p[1] not in session_used]
        pool = filtered if filtered else all_pairs
        category, message = pool[0]
        return category, message

    category, message = random.choice(available)
    return category, message


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

def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_dir)
    tokens_dir = os.path.join(repo_dir, "design_tokens")

    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║         🎨  Design Code  🎨          ║")
    print("  ║    Daily design-token commit tool     ║")
    print("  ╚══════════════════════════════════════╝")
    print()

    while True:
        try:
            num = int(input("  How many commits would you like to make today? "))
            if num < 1:
                print("  Please enter at least 1.")
                continue
            break
        except ValueError:
            print("  Enter a number, e.g. 3")

    print()
    history = _load_history()
    session_used = set()

    for i in range(1, num + 1):
        category, message = _pick_commit(history, session_used)
        session_used.add(message)
        _record_usage(message, history)

        modifier = MODIFIERS.get(category, _modify_random)
        modifier(tokens_dir)
        _append_log(tokens_dir, message)

        _git("add", "-A")
        _git("commit", "-m", message)
        print(f"  [{i}/{num}] ✓ {message}")

    _save_history(history)

    print()
    print("  Pushing to GitHub …")
    result = _git("push")
    if result.returncode == 0:
        print(f"  Done! {num} commit{'s' if num != 1 else ''} pushed. Your graph just got greener 🟩")
    else:
        print("  Push failed — check your remote with: git remote -v")
    print()


if __name__ == "__main__":
    main()
