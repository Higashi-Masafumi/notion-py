#!/usr/bin/env python3
"""Scan notion-py for high-signal Notion API compatibility gaps."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Match:
    path: str
    line: int
    text: str


@dataclass
class CheckResult:
    check_id: str
    title: str
    classification: str
    summary: str
    rationale: str
    old_matches: list[Match]
    new_matches: list[Match]


@dataclass
class ScanReport:
    repo_root: str
    repo_ok: bool
    checks: list[CheckResult]


def run_rg(repo_root: Path, pattern: str) -> list[Match]:
    cmd = [
        "rg",
        "-n",
        "--no-heading",
        "--color",
        "never",
        "-g",
        "!notion-api-changelog-pr/**",
        pattern,
        str(repo_root),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.strip() or f"rg failed for pattern: {pattern}")
    matches: list[Match] = []
    for line in result.stdout.splitlines():
        try:
            path, line_no, text = line.split(":", 2)
        except ValueError:
            continue
        matches.append(Match(path=str(Path(path).resolve()), line=int(line_no), text=text.strip()))
    return matches


def any_match(repo_root: Path, patterns: list[str]) -> list[Match]:
    combined: list[Match] = []
    for pattern in patterns:
        combined.extend(run_rg(repo_root, pattern))
    deduped: dict[tuple[str, int, str], Match] = {}
    for match in combined:
        deduped[(match.path, match.line, match.text)] = match
    return list(sorted(deduped.values(), key=lambda item: (item.path, item.line, item.text)))


def ensure_repo(repo_root: Path) -> tuple[bool, str]:
    pyproject = repo_root / "pyproject.toml"
    package_dir = repo_root / "notion_py_client"
    git_dir = repo_root / ".git"
    if not pyproject.exists() or not package_dir.exists() or not git_dir.exists():
        return False, "repo root is missing pyproject.toml, notion_py_client/, or .git"
    try:
        content = pyproject.read_text()
    except OSError as exc:
        return False, f"failed to read pyproject.toml: {exc}"
    if 'name = "notion-py-client"' not in content:
        return False, 'pyproject.toml does not look like notion-py-client'
    return True, "repo looks like notion-py"


def classify_version_support(repo_root: Path) -> CheckResult:
    old_matches = any_match(repo_root, [r"default_notion_version\s*=\s*\"2025-09-03\""])
    new_matches = any_match(repo_root, [r"2026-03-11", r"notionVersion:\s*\"2026-03-11\""])
    if old_matches and not new_matches:
        classification = "auto-fix"
        summary = "Repo still defaults to or documents 2025-09-03 without any visible 2026-03-11 support."
    elif new_matches:
        classification = "no-op"
        summary = "Repo already mentions 2026-03-11 support somewhere; verify whether it is opt-in or complete."
    else:
        classification = "auto-fix"
        summary = "No visible 2026-03-11 support markers were found."
    return CheckResult(
        check_id="version-support",
        title="2026-03-11 version support",
        classification=classification,
        summary=summary,
        rationale="Breaking API versions should be added as opt-in support before changing defaults.",
        old_matches=old_matches,
        new_matches=new_matches,
    )


def classify_simple_gap(
    *,
    repo_root: Path,
    check_id: str,
    title: str,
    old_patterns: list[str],
    new_patterns: list[str],
    rationale: str,
    default_when_missing: str = "auto-fix",
    summary_when_missing: str,
    summary_when_present: str,
) -> CheckResult:
    old_matches = any_match(repo_root, old_patterns)
    new_matches = any_match(repo_root, new_patterns)
    if old_matches and new_matches:
        classification = "auto-fix"
        summary = f"{summary_when_present} Legacy markers are still present, so the migration looks incomplete."
    elif old_matches and not new_matches:
        classification = "auto-fix"
        summary = summary_when_missing
    elif new_matches:
        classification = "no-op"
        summary = summary_when_present
    else:
        classification = default_when_missing
        summary = summary_when_missing
    return CheckResult(
        check_id=check_id,
        title=title,
        classification=classification,
        summary=summary,
        rationale=rationale,
        old_matches=old_matches,
        new_matches=new_matches,
    )


def classify_report_only(
    *,
    repo_root: Path,
    check_id: str,
    title: str,
    new_patterns: list[str],
    rationale: str,
    summary_when_missing: str,
    summary_when_present: str,
) -> CheckResult:
    new_matches = any_match(repo_root, new_patterns)
    if new_matches:
        classification = "no-op"
        summary = summary_when_present
    else:
        classification = "report-only"
        summary = summary_when_missing
    return CheckResult(
        check_id=check_id,
        title=title,
        classification=classification,
        summary=summary,
        rationale=rationale,
        old_matches=[],
        new_matches=new_matches,
    )


def build_report(repo_root: Path) -> ScanReport:
    repo_ok, _ = ensure_repo(repo_root)
    checks = [
        classify_version_support(repo_root),
        classify_simple_gap(
            repo_root=repo_root,
            check_id="append-position",
            title="Append block children position object",
            old_patterns=[
                r"after:\s+str\s+\|\s+None\s+=\s+None",
                r"after:\s+NotRequired\[str\]",
                r"\{\"after\":\s+after\}",
            ],
            new_patterns=[
                r"position:\s",
                r"after_block",
                r"type:\s*Literal\[\"after_block\"",
            ],
            rationale="2026-03-11 replaces the flat after parameter with the position object.",
            summary_when_missing="Legacy after-based insertion is still present without clear position support.",
            summary_when_present="Position-related support is already present somewhere in the repo.",
        ),
        classify_simple_gap(
            repo_root=repo_root,
            check_id="trash-semantics",
            title="in_trash request and response handling",
            old_patterns=[r"\barchived\b"],
            new_patterns=[r"\bin_trash\b"],
            rationale="Request and response handling should move from archived to in_trash.",
            summary_when_missing="The repo still uses archived without visible in_trash coverage.",
            summary_when_present="The repo already contains in_trash support; inspect remaining archived uses before patching.",
        ),
        classify_simple_gap(
            repo_root=repo_root,
            check_id="meeting-notes",
            title="meeting_notes block rename",
            old_patterns=[r"\btranscription\b"],
            new_patterns=[r"\bmeeting_notes\b"],
            rationale="2026-03-11 renames the transcription block type to meeting_notes.",
            summary_when_missing="No visible meeting_notes support was found.",
            summary_when_present="The repo already contains meeting_notes references.",
        ),
        classify_simple_gap(
            repo_root=repo_root,
            check_id="heading-4",
            title="heading_4 block support",
            old_patterns=[],
            new_patterns=[r"heading_4"],
            rationale="Heading level 4 support is a bounded model addition when upstream supports it.",
            summary_when_missing="No heading_4 support markers were found.",
            summary_when_present="The repo already contains heading_4 support markers.",
        ),
        classify_simple_gap(
            repo_root=repo_root,
            check_id="tab-block",
            title="tab block support",
            old_patterns=[],
            new_patterns=[r"\btab\b"],
            rationale="Tab support is a bounded block-model addition if the upstream API exposes it.",
            summary_when_missing="No clear tab block support markers were found.",
            summary_when_present="The repo already contains tab support markers.",
        ),
        classify_simple_gap(
            repo_root=repo_root,
            check_id="custom-emojis",
            title="custom_emojis support",
            old_patterns=[r"custom_emoji"],
            new_patterns=[r"custom_emojis"],
            rationale="Listing or endpoint-level custom_emojis support is separate from singular custom_emoji model fields.",
            summary_when_missing="The repo has singular custom_emoji support but no visible custom_emojis API support.",
            summary_when_present="The repo already contains custom_emojis support markers.",
        ),
        classify_report_only(
            repo_root=repo_root,
            check_id="views-api",
            title="Views API",
            new_patterns=[r"_ViewsAPI", r"\bviews\s*=", r"/v1/views", r"\bviews\."],
            rationale="Views is a likely large API surface and should default to report-only unless the repo already has a façade.",
            summary_when_missing="No Views API façade was found; treat this as report-only work.",
            summary_when_present="The repo already contains Views API markers.",
        ),
        classify_simple_gap(
            repo_root=repo_root,
            check_id="markdown-endpoints",
            title="Markdown endpoints",
            old_patterns=[],
            new_patterns=[r"retrieveMarkdown", r"updateMarkdown", r"/markdown", r"Working with markdown content"],
            rationale="Thin markdown endpoint support can stay inside bounded scope if the official request and response shapes are small.",
            summary_when_missing="No clear markdown endpoint support markers were found.",
            summary_when_present="The repo already contains markdown endpoint markers or docs references.",
        ),
        classify_simple_gap(
            repo_root=repo_root,
            check_id="verification-write",
            title="Writable verification property support",
            old_patterns=[r"VerificationProperty", r"verification_property"],
            new_patterns=[r"class\s+VerificationPropertyRequest"],
            rationale="Writable verification support is bounded when it fits the existing property request layout.",
            summary_when_missing="Verification exists in responses but no writable verification request support is visible.",
            summary_when_present="Writable verification request markers are already present.",
        ),
        classify_simple_gap(
            repo_root=repo_root,
            check_id="native-icon",
            title="Native icon request and response support",
            old_patterns=[],
            new_patterns=[r"NotionIcon", r"PageIconRequest", r"custom_emoji"],
            rationale="Native icon support is bounded if it only extends existing icon models and request fragments.",
            summary_when_missing="No native icon support markers were found.",
            summary_when_present="The repo already contains native icon support markers.",
        ),
    ]
    return ScanReport(repo_root=str(repo_root.resolve()), repo_ok=repo_ok, checks=checks)


def render_markdown(report: ScanReport, include_noop: bool) -> str:
    lines = [
        f"# Notion API gap scan for `{report.repo_root}`",
        "",
        f"- repo_ok: `{str(report.repo_ok).lower()}`",
        "",
    ]
    for bucket in ("auto-fix", "report-only", "no-op"):
        bucket_checks = [check for check in report.checks if check.classification == bucket]
        if bucket == "no-op" and not include_noop:
            continue
        lines.append(f"## {bucket}")
        if not bucket_checks:
            lines.append("")
            lines.append("- none")
            lines.append("")
            continue
        lines.append("")
        for check in bucket_checks:
            lines.append(f"### {check.title}")
            lines.append("")
            lines.append(f"- id: `{check.check_id}`")
            lines.append(f"- summary: {check.summary}")
            lines.append(f"- rationale: {check.rationale}")
            lines.append(f"- old_matches: {len(check.old_matches)}")
            lines.append(f"- new_matches: {len(check.new_matches)}")
            sample_matches = (check.old_matches + check.new_matches)[:3]
            if sample_matches:
                lines.append("- evidence:")
                for match in sample_matches:
                    lines.append(
                        f"  - `{Path(match.path).name}:{match.line}` {match.text}"
                    )
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_json(report: ScanReport) -> str:
    return json.dumps(asdict(report), indent=2, ensure_ascii=False) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        default="..",
        help="Path to the notion-py repo root. Defaults to the parent of the skill directory.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--include-noop",
        action="store_true",
        help="Include no-op checks in markdown output.",
    )
    return parser.parse_args()


def main() -> int:
    if shutil.which("rg") is None:
        print("rg is required but was not found in PATH.", file=sys.stderr)
        return 1

    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)

    repo_ok, message = ensure_repo(repo_root)
    if not repo_ok:
        print(f"Repository check failed: {message}", file=sys.stderr)
        return 2

    if args.format == "json":
        sys.stdout.write(render_json(report))
    else:
        sys.stdout.write(render_markdown(report, include_noop=args.include_noop))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
