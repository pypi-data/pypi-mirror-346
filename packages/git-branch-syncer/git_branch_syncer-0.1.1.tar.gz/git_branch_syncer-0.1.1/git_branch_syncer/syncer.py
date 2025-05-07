import subprocess
import argparse
import re
import sys
import os
import fnmatch  # Import fnmatch for pattern matching

def sync_branches(pattern, mother, dry_run=False, verbose=False, force=False):
    if verbose:
        print(f"🔧 Pattern: {pattern}, Mother: {mother}, Dry-run: {dry_run}, Force: {force}")

    def run(cmd):
        if verbose:
            print(f"👉 Running: {cmd}")
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            sys.exit(result.returncode)

    try:
        subprocess.check_output("git rev-parse --is-inside-work-tree", shell=True)
    except subprocess.CalledProcessError:
        print("❌ Not a git repository. Exiting.")
        sys.exit(1)

    run("git fetch --all --prune")

    # Get all remote branches
    remote_branches = subprocess.check_output("git branch -r", shell=True, text=True).splitlines()

    # Debug: Print remote branches for debugging
    print("Remote branches fetched from Git:")
    for branch in remote_branches:
        print(repr(branch))  # Use repr() to reveal hidden characters, like extra spaces

    # Remove "origin/" prefix and use fnmatch to filter branches matching the pattern
    all_branches = [b.strip().replace("origin/", "") for b in remote_branches]
    print("Branches after removing 'origin/':")
    for b in all_branches:
        print(repr(b))

    matched = [b for b in all_branches if fnmatch.fnmatch(b, pattern)]

    if not matched:
        print(f"⚠️ No branches matched pattern '{pattern}'")
        return

    print(f"Matched branches: {matched}")

    for branch in matched:
        if dry_run:
            print(f"💤 Dry-run: would update '{branch}' from '{mother}'")
            continue

        if not force:
            diff = subprocess.run("git diff --quiet", shell=True)
            if diff.returncode != 0:
                print(f"⚠️ Skipping '{branch}' due to local changes (use --force to override)")
                continue

        run(f"git checkout -B {branch} origin/{mother}")

    print("✅ Done.")

def main():
    parser = argparse.ArgumentParser(description="Git Branch Syncer")
    parser.add_argument("-p", "--pattern", default="feature/*", help="Branch pattern to match")
    parser.add_argument("--mother", default="main", help="Mother branch to sync from")
    parser.add_argument("--dry-run", action="store_true", help="Dry-run mode")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--force", action="store_true", help="Force sync even if dirty")
    args = parser.parse_args()

    sync_branches(args.pattern, args.mother, args.dry_run, args.verbose, args.force)

if __name__ == "__main__":
    main()