#!/usr/bin/env python3
"""
Design Code — Daily commit script for design engineers.
Run this from your terminal each day to log design work to GitHub.
"""

import os
import random
import subprocess
import json
from datetime import datetime

# ---------------------------------------------------------------------------
# Design-themed commit messages grouped by category
# ---------------------------------------------------------------------------
COMMIT_MESSAGES = {
    "color": [
        "color change",
        "primary color update",
        "secondary palette refinement",
        "accent color adjustment",
        "color contrast fix",
        "dark mode color tweak",
        "color palette expansion",
        "brand color alignment",
        "surface color update",
        "semantic color token fix",
    ],
    "brand": [
        "brand token change",
        "brand font update",
        "brand spacing alignment",
        "brand asset refresh",
        "brand guideline sync",
    ],
    "typography": [
        "typography scale update",
        "font weight adjustment",
        "line height refinement",
        "heading hierarchy fix",
        "body text improvement",
        "font family swap",
        "letter spacing tweak",
    ],
    "spacing": [
        "spacing token update",
        "padding consistency fix",
        "margin alignment",
        "grid gap adjustment",
        "layout spacing refinement",
        "section spacing update",
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
    ],
    "ui_fixes": [
        "UI fixes",
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
    ],
    "motion": [
        "animation duration update",
        "transition easing change",
        "micro-interaction refinement",
        "loading animation tweak",
        "scroll animation fix",
    ],
    "accessibility": [
        "accessibility contrast fix",
        "focus indicator update",
        "screen reader label add",
        "aria attribute update",
        "keyboard navigation fix",
    ],
}

# Flatten for easy random selection
ALL_MESSAGES = [msg for group in COMMIT_MESSAGES.values() for msg in group]


# ---------------------------------------------------------------------------
# File-modification helpers — each one touches a different token file so
# the diffs look realistic in GitHub.
# ---------------------------------------------------------------------------

def _modify_colors(tokens_dir: str) -> None:
    """Tweak a value inside colors.json."""
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
    """Tweak a value inside typography.json."""
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
    """Tweak a value inside spacing.json."""
    path = os.path.join(tokens_dir, "spacing.json")
    with open(path) as f:
        data = json.load(f)

    key = random.choice(list(data.keys()))
    base = random.choice([2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64])
    data[key] = f"{base}px"

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def _modify_components(tokens_dir: str) -> None:
    """Tweak a value inside components.json."""
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


def _append_log(tokens_dir: str, message: str) -> None:
    """Append an entry to the design changelog."""
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
}


def _pick_commit():
    """Return (category, message)."""
    category = random.choice(list(COMMIT_MESSAGES.keys()))
    message = random.choice(COMMIT_MESSAGES[category])
    return category, message


def _git(*args):
    """Run a git command and return the result."""
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
    # Make sure we're in the repo root
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_dir)
    tokens_dir = os.path.join(repo_dir, "design_tokens")

    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║         🎨  Design Code  🎨          ║")
    print("  ║    Daily design-token commit tool     ║")
    print("  ╚══════════════════════════════════════╝")
    print()

    # Ask how many commits
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
    used_messages = set()

    for i in range(1, num + 1):
        # Pick a unique message when possible
        category, message = _pick_commit()
        attempts = 0
        while message in used_messages and attempts < 20:
            category, message = _pick_commit()
            attempts += 1
        used_messages.add(message)

        # Modify the relevant token file
        modifier = MODIFIERS.get(category, _modify_components)
        modifier(tokens_dir)
        _append_log(tokens_dir, message)

        # Stage & commit
        _git("add", "-A")
        _git("commit", "-m", message)
        print(f"  [{i}/{num}] ✓ {message}")

    # Push
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
