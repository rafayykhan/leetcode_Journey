#!/usr/bin/env python3
"""
Keeps README.md up to date automatically.

Scans problem folders in the repo root (the ones LeetPush creates, e.g.
"217-contains-duplicate"), looks up each problem's difficulty and topic tags
from LeetCode, and refills the four auto-generated regions of the README:
badges, topic tables, stats, milestones.

The README's wording, ordering and layout are never changed — only the numbers
and the table rows inside the markers.
"""

import json
import os
import re
import subprocess
import sys
import urllib.request
from collections import defaultdict
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
CACHE = os.path.join(ROOT, "scripts", "problem_cache.json")

FOLDER_RE = re.compile(r"^(\d{1,5})-([a-z0-9\-]+)$")
GRAPHQL = "https://leetcode.com/graphql"

# The 29 sections exactly as they appear in the README, in order.
# Each entry: (emoji, section heading, [LeetCode tags that belong to it])
SECTIONS = [
    ("🔢",   "Array",                     ["Array"]),
    ("🔤",   "String",                    ["String", "String Matching"]),
    ("#️⃣",   "Hash Table",                ["Hash Table", "Counting", "Hash Function"]),
    ("👉👈", "Two Pointers",               ["Two Pointers"]),
    ("🪟",   "Sliding Window",            ["Sliding Window"]),
    ("➕",   "Prefix Sum",                ["Prefix Sum"]),
    ("🔍",   "Binary Search",             ["Binary Search"]),
    ("🧮",   "Matrix",                    ["Matrix"]),
    ("📚",   "Stack & Queue",             ["Stack", "Queue", "Monotonic Queue"]),
    ("📈",   "Monotonic Stack",           ["Monotonic Stack"]),
    ("🔗",   "Linked List",               ["Linked List", "Doubly-Linked List"]),
    ("🌳",   "Binary Tree",               ["Tree", "Binary Tree"]),
    ("🌲",   "Binary Search Tree",        ["Binary Search Tree"]),
    ("⛰️",   "Heap / Priority Queue",     ["Heap (Priority Queue)"]),
    ("🌐",   "Graph — BFS / DFS",         ["Graph", "Breadth-First Search",
                                           "Depth-First Search"]),
    ("🔀",   "Topological Sort",          ["Topological Sort"]),
    ("🔗",   "Union-Find",                ["Union Find"]),
    ("🛣️",   "Shortest Path",             ["Shortest Path"]),
    ("🔙",   "Backtracking",              ["Backtracking"]),
    ("♻️",   "Recursion",                 ["Recursion", "Divide and Conquer"]),
    ("💰",   "Greedy",                    ["Greedy"]),
    ("🧊",   "Dynamic Programming",       ["Dynamic Programming", "Memoization"]),
    ("🎒",   "Knapsack / DP on Strings",  []),   # rule-based, see below
    ("🔣",   "Bit Manipulation",          ["Bit Manipulation", "Bitmask"]),
    ("📐",   "Intervals",                 ["Line Sweep"]),
    ("🌴",   "Trie",                      ["Trie", "Suffix Array"]),
    ("🏗️",   "Design (LRU, Iterators)",   ["Design", "Iterator", "Data Stream",
                                           "Ordered Set"]),
    ("🎲",   "Math & Simulation",         ["Math", "Simulation", "Number Theory",
                                           "Combinatorics", "Geometry",
                                           "Enumeration", "Randomized",
                                           "Probability and Statistics"]),
    ("🌡️",   "Segment Tree / Fenwick",    ["Segment Tree", "Binary Indexed Tree"]),
]

TAG_TO_SECTIONS = defaultdict(list)
for _emoji, _name, _tags in SECTIONS:
    for _tag in _tags:
        TAG_TO_SECTIONS[_tag].append(_name)

DIFF_LABEL = {"Easy": "🟩 Easy", "Medium": "🟨 Medium", "Hard": "🟥 Hard"}

MILESTONES = [
    (10,  "🥉", "Day 10",  "first ten in the bag"),
    (25,  "🥈", "Day 25",  "a Medium solved cold, no hints"),
    (50,  "🥇", "Day 50",  "five topics genuinely comfortable"),
    (75,  "💎", "Day 75",  "first Hard cracked solo"),
    (100, "👑", "Day 100", "pattern recognised before the statement ends"),
]


# ── problem data ────────────────────────────────────────────────────────────

def load_cache():
    if os.path.exists(CACHE):
        try:
            with open(CACHE, encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, json.JSONDecodeError):
            pass
    return {}


def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w", encoding="utf-8") as fh:
        json.dump(cache, fh, indent=2, sort_keys=True, ensure_ascii=False)


def fetch(slug):
    payload = {
        "operationName": "questionData",
        "variables": {"titleSlug": slug},
        "query": """query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionFrontendId title difficulty topicTags { name }
            }
        }""",
    }
    req = urllib.request.Request(
        GRAPHQL,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (readme-updater)",
            "Referer": f"https://leetcode.com/problems/{slug}/",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        q = json.load(resp)["data"]["question"]
    return {
        "id": q["questionFrontendId"],
        "title": q["title"],
        "difficulty": q["difficulty"],
        "topics": [t["name"] for t in q["topicTags"]],
    }


def fallback(pid, slug):
    return {
        "id": pid,
        "title": slug.replace("-", " ").title(),
        "difficulty": "Unknown",
        "topics": [],
    }


def sections_for(problem):
    """Which README sections a problem belongs in."""
    names = []
    for tag in problem["topics"]:
        for name in TAG_TO_SECTIONS.get(tag, []):
            if name not in names:
                names.append(name)

    tags = set(problem["topics"])
    slug = problem["slug"]

    # Knapsack / DP on strings — no single LeetCode tag covers these.
    if "Dynamic Programming" in tags and (
        "String" in tags or "knapsack" in slug or "subset-sum" in slug
        or "partition" in slug
    ):
        names.append("Knapsack / DP on Strings")

    # Intervals — likewise no dedicated tag.
    if any(k in slug for k in ("interval", "meeting-rooms", "car-pooling",
                               "my-calendar", "range-module")):
        if "Intervals" not in names:
            names.append("Intervals")

    return names


# ── git history (for day numbering and streak) ──────────────────────────────

def first_seen_dates():
    """Map folder name -> date it was first committed."""
    try:
        out = subprocess.run(
            ["git", "log", "--reverse", "--diff-filter=A", "--date=short",
             "--pretty=format:@%ad", "--name-only"],
            cwd=ROOT, capture_output=True, text=True, timeout=60, check=True,
        ).stdout
    except Exception:                                     # noqa: BLE001
        return {}

    dates, current = {}, None
    for line in out.splitlines():
        if line.startswith("@"):
            current = line[1:].strip()
        elif line.strip() and current:
            folder = line.split("/")[0]
            dates.setdefault(folder, current)
    return dates


def streak(days):
    """Consecutive solving days ending today or yesterday."""
    if not days:
        return 0
    seen = {date.fromisoformat(d) for d in days}
    today = date.today()
    cursor = today if today in seen else today - timedelta(days=1)
    if cursor not in seen:
        return 0
    count = 0
    while cursor in seen:
        count += 1
        cursor -= timedelta(days=1)
    return count


# ── rendering ───────────────────────────────────────────────────────────────

def render_badges(problems, total_days):
    b = "https://img.shields.io/badge"
    s = "style=for-the-badge&labelColor=0D1117"
    return (
        f"![Day]({b}/Day-{total_days:03d}-7C3AED?{s})\n"
        f"![Solved]({b}/Solved-{len(problems)}-2563EB?{s})\n"
        f"![Python]({b}/Python-3.12-06B6D4?{s})\n"
        f"![Status]({b}/Status-Just_Started-22C55E?{s})"
    )


def render_topics(problems):
    buckets = defaultdict(list)
    for p in problems:
        for name in p["sections"]:
            buckets[name].append(p)

    blocks = []
    for emoji, name, _tags in SECTIONS:
        rows = sorted(buckets.get(name, []), key=lambda p: p["day"])
        block = [
            "<details>",
            f"<summary><b>{emoji} {name}</b> — {len(rows)} solved</summary>",
            "",
            "| Day | Problem | Difficulty |",
            "|-----|---------|------------|",
        ]
        if rows:
            for p in rows:
                link = f"https://leetcode.com/problems/{p['slug']}/"
                diff = DIFF_LABEL.get(p["difficulty"], p["difficulty"])
                block.append(
                    f"| Day {p['day']:03d} | [{p['title']}]({link}) | {diff} |"
                )
        else:
            block.append("| — | *coming soon* | — |")
        block += ["", "</details>"]
        blocks.append("\n".join(block))
    return "\n\n".join(blocks)


def render_stats(problems, total_days, current_streak):
    counts = defaultdict(int)
    for p in problems:
        counts[p["difficulty"]] += 1
    touched = len({name for p in problems for name in p["sections"]})
    return "\n".join([
        "| Metric | Count |",
        "|--------|-------|",
        f"| 📅 Total Days | {total_days} |",
        f"| 🟩 Easy | {counts['Easy']} |",
        f"| 🟨 Medium | {counts['Medium']} |",
        f"| 🟥 Hard | {counts['Hard']} |",
        f"| 🧩 Topics Covered | {touched} / {len(SECTIONS)} |",
        f"| 🔥 Current Streak | {current_streak} |",
    ])


def render_milestones(total_days):
    lines = []
    for threshold, emoji, label, text in MILESTONES:
        box = "x" if total_days >= threshold else " "
        lines.append(f"- [{box}] {emoji} **{label}** — {text}")
    return "\n".join(lines)


def splice(text, marker, body):
    start, end = f"<!-- {marker}:START -->", f"<!-- {marker}:END -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(text):
        print(f"  ! marker {marker} missing from README — skipped")
        return text
    return pattern.sub(lambda _m: f"{start}\n\n{body}\n\n{end}", text)


# ── main ────────────────────────────────────────────────────────────────────

def main():
    cache = load_cache()
    dates = first_seen_dates()
    folders = []

    for name in sorted(os.listdir(ROOT)):
        if name.startswith(".") or not os.path.isdir(os.path.join(ROOT, name)):
            continue
        m = FOLDER_RE.match(name)
        if m:
            folders.append((m.group(1), m.group(2), name))

    # Chronological order: by first-commit date, then by folder name.
    folders.sort(key=lambda f: (dates.get(f[2], "9999-99-99"), f[2]))

    problems, fetched = [], 0
    for day, (pid, slug, folder) in enumerate(folders, start=1):
        if slug in cache:
            data = cache[slug]
        else:
            try:
                data = fetch(slug)
                cache[slug] = data      # only real results get cached, so a
                fetched += 1            # failed lookup retries on the next run
                print(f"  + fetched {slug}")
            except Exception as exc:                      # noqa: BLE001
                print(f"  ! {slug}: {exc} — using fallback")
                data = fallback(pid, slug)
        problem = {**data, "slug": slug, "folder": folder, "day": day,
                   "date": dates.get(folder)}
        problem["sections"] = sections_for(problem)
        problems.append(problem)

    solve_days = sorted({p["date"] for p in problems if p["date"]})
    total_days = len(solve_days) if solve_days else len(problems)
    current_streak = streak(solve_days)

    print(f"{len(problems)} problem(s) · {fetched} newly fetched · "
          f"{total_days} day(s) · streak {current_streak}")
    save_cache(cache)

    if not os.path.exists(README):
        sys.exit("README.md not found")
    with open(README, encoding="utf-8") as fh:
        text = fh.read()

    text = splice(text, "BADGES", render_badges(problems, total_days))
    text = splice(text, "TOPICS", render_topics(problems))
    text = splice(text, "STATS", render_stats(problems, total_days, current_streak))
    text = splice(text, "MILESTONES", render_milestones(total_days))

    with open(README, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("README.md updated")


if __name__ == "__main__":
    main()
