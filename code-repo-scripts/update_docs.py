#!/usr/bin/env python3
"""
Reads the PR diff (pr_diff.txt), sends it to Claude (via Amazon Bedrock)
along with the current contents of each doc file listed in DOC_PATHS, and
overwrites those files with Claude's updated version if it thinks a change
is warranted.

Auth: uses the standard AWS credential chain (env vars / OIDC role assumed
by the GitHub Actions step, ~/.aws/credentials, etc.) via boto3 under the
hood — no ANTHROPIC_API_KEY needed.

Env vars:
  AWS_REGION          - required, e.g. "us-east-1" (must be a region where
                         the chosen model/inference profile is available)
  BEDROCK_MODEL_ID     - Bedrock model ID or cross-region inference profile.
                         Default is Claude Haiku 4.5 (cheapest/fastest).
  DOC_PATHS           - comma-separated list of doc files to keep in sync
                         (default: "README.md")
  DOC_ROOT            - directory doc paths are relative to (default: ".")
  PR_TITLE, PR_BODY, PR_URL - optional context passed to the model
  MAX_DIFF_CHARS       - safety cap on diff size sent to the model
"""

import os
import sys
from pathlib import Path

from anthropic import AnthropicBedrock

# Cheapest current-generation model by default. Bump to a Sonnet model
# (e.g. "us.anthropic.claude-sonnet-5-...") if doc quality needs improving.
DEFAULT_MODEL_ID = "global.anthropic.claude-haiku-4-5-20251001-v1:0"
MAX_DIFF_CHARS = int(os.environ.get("MAX_DIFF_CHARS", "60000"))

SYSTEM_PROMPT = """You are a meticulous technical writer who keeps a repository's \
documentation in sync with its code.

You will be given:
1. A unified git diff of changes made in a pull request.
2. The current full contents of one documentation file.

Your job:
- Decide whether the diff introduces changes that make the documentation \
  outdated, incomplete, or incorrect (new features, changed CLI flags, \
  renamed config keys, new env vars, changed API signatures, removed \
  functionality, etc).
- If no doc update is warranted, output exactly the original file content \
  unchanged.
- If an update is warranted, output the FULL updated file content, \
  preserving the existing style, tone, and structure as much as possible. \
  Make the smallest edit that keeps the docs accurate — do not rewrite \
  unrelated sections.
- Never invent details that aren't supported by the diff. If something is \
  ambiguous, leave a `<!-- TODO(docs-bot): verify ... -->` comment instead \
  of guessing.

Output ONLY the raw file content. No preamble, no code fences, no \
explanation."""


def read_diff() -> str:
    diff_path = Path("pr_diff.txt")
    if not diff_path.exists():
        print("No pr_diff.txt found; nothing to do.")
        sys.exit(0)
    diff = diff_path.read_text(errors="ignore")
    if not diff.strip():
        print("Empty diff; nothing to do.")
        sys.exit(0)
    if len(diff) > MAX_DIFF_CHARS:
        print(f"Diff truncated from {len(diff)} to {MAX_DIFF_CHARS} chars.")
        diff = diff[:MAX_DIFF_CHARS] + "\n...[diff truncated]..."
    return diff


def update_doc(client: AnthropicBedrock, model_id: str, diff: str, doc_path: Path, pr_context: str) -> bool:
    if not doc_path.exists():
        print(f"Skipping {doc_path}: file does not exist.")
        return False

    original = doc_path.read_text()

    user_message = f"""PR context:
{pr_context or '(no title/description provided)'}

--- BEGIN DIFF ---
{diff}
--- END DIFF ---

--- BEGIN CURRENT CONTENT OF {doc_path} ---
{original}
--- END CURRENT CONTENT OF {doc_path} ---
"""

    response = client.messages.create(
        model=model_id,
        max_tokens=8000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    updated = "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()

    if not updated or updated == original.strip():
        print(f"{doc_path}: no changes needed.")
        return False

    doc_path.write_text(updated + ("\n" if not updated.endswith("\n") else ""))
    print(f"{doc_path}: updated.")
    return True


def main() -> None:
    region = os.environ.get("AWS_REGION")
    if not region:
        print("AWS_REGION is not set.", file=sys.stderr)
        sys.exit(1)

    model_id = os.environ.get("BEDROCK_MODEL_ID", DEFAULT_MODEL_ID)

    doc_root = Path(os.environ.get("DOC_ROOT", "."))
    doc_paths = [
        doc_root / p.strip()
        for p in os.environ.get("DOC_PATHS", "README.md").split(",")
        if p.strip()
    ]
    pr_title = os.environ.get("PR_TITLE", "")
    pr_body = os.environ.get("PR_BODY", "")
    pr_url = os.environ.get("PR_URL", "")
    pr_context = f"Title: {pr_title}\nURL: {pr_url}\n\nDescription:\n{pr_body}"

    diff = read_diff()

    # Picks up credentials from the environment (AWS_ACCESS_KEY_ID /
    # AWS_SECRET_ACCESS_KEY / AWS_SESSION_TOKEN), which the GitHub Actions
    # OIDC step below will have exported.
    client = AnthropicBedrock(aws_region=region)

    any_changed = False
    changed_files = []
    for doc_path in doc_paths:
        if update_doc(client, model_id, diff, doc_path, pr_context):
            any_changed = True
            changed_files.append(str(doc_path))

    # Expose a short summary for the "Comment summary on PR" workflow step.
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            if any_changed:
                f.write(f"summary=Updated {', '.join(changed_files)} based on this PR's changes.\n")
            else:
                f.write("summary=\n")


if __name__ == "__main__":
    main()
