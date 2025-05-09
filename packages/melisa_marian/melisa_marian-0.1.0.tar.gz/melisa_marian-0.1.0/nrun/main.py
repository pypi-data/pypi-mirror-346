#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import traceback
import requests # For sending HTTP requests to ntfy
import socket # To include hostname in notification
import subprocess # To run the command
import argparse # To parse CLI arguments
import shlex # To help display the command safely

# --- Configuration ---
# IMPORTANT: Change this to your actual ntfy topic URL!
# Public example: NTFY_TOPIC_URL = "https://ntfy.sh/my_python_script_alerts_xyz123"
# Self-hosted example: NTFY_TOPIC_URL = "http://your-server-ip:port/your_topic"
NTFY_TOPIC_URL = "https://ntfy.sh/topic_melisa" # <<< CHANGE THIS!

# Optional: ntfy authentication (if your topic requires it)
NTFY_USERNAME = None
NTFY_PASSWORD = None
NTFY_ACCESS_TOKEN = None # Takes precedence over user/pass if set

# --- ntfy Notification Function ---
def send_ntfy_notification(title, message, priority="default", tags=None):
    """Sends a notification to the configured ntfy topic."""
    if not NTFY_TOPIC_URL or "replace_this_with_your_topic" in NTFY_TOPIC_URL:
        print("--- NTFY SKIPPED: NTFY_TOPIC_URL not configured. ---", file=sys.stderr)
        return

    headers = {
        "Title": title.encode('utf-8'),
        "Priority": priority
    }
    if tags:
        headers["Tags"] = ",".join(tags)

    auth = None
    if NTFY_ACCESS_TOKEN:
        headers["Authorization"] = f"Bearer {NTFY_ACCESS_TOKEN}"
    elif NTFY_USERNAME and NTFY_PASSWORD:
        auth = (NTFY_USERNAME, NTFY_PASSWORD)

    print(f"\nAttempting to send ntfy notification to: {NTFY_TOPIC_URL}", file=sys.stderr)
    # Avoid printing potentially sensitive details from message to stderr here

    try:
        response = requests.post(
            NTFY_TOPIC_URL,
            data=message.encode('utf-8'),
            headers=headers,
            auth=auth,
            timeout=15 # Slightly longer timeout for network potentially
        )
        response.raise_for_status()
        print("--> ntfy notification sent successfully.", file=sys.stderr)

    except requests.exceptions.RequestException as e:
        print("\n--- NTFY Notification Failed ---", file=sys.stderr)
        print(f"Error sending notification to {NTFY_TOPIC_URL}:", file=sys.stderr)
        print(f"Error Type: {type(e).__name__}", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
             print(f"Status Code: {e.response.status_code}", file=sys.stderr)
             # Avoid printing potentially large/sensitive response body
             print(f"Response Text Hint: {e.response.text[:100]}...", file=sys.stderr)
        print("--------------------------------", file=sys.stderr)
    except Exception as e:
        print("\n--- NTFY Notification Failed (Unexpected Error) ---", file=sys.stderr)
        print(f"An unexpected error occurred: {type(e).__name__}: {e}", file=sys.stderr)
        print("---------------------------------------------------", file=sys.stderr)


# --- Main Execution Logic ---
def run_command_and_notify(command_args):
    """Runs the command, captures output, and sends notification."""
    if not command_args:
        print("Error: No command provided.", file=sys.stderr)
        return 1 # Return non-zero exit code

    # Get hostname and prepare command string for display/logging
    hostname = socket.gethostname()
    command_str = shlex.join(command_args) # Safely quote arguments for display

    print(f"Executing on {hostname}: {command_str}", file=sys.stderr)
    start_time = time.perf_counter() # More precise timer

    process_result = None
    exit_code = 1 # Default to failure
    stdout_str = ""
    stderr_str = ""

    try:
        # Run the command
        process_result = subprocess.run(
            command_args,
            capture_output=True, # Capture stdout/stderr
            text=True,           # Decode as text (usually utf-8)
            check=False          # Don't raise exception on non-zero exit; we handle it
        )
        exit_code = process_result.returncode
        stdout_str = process_result.stdout
        stderr_str = process_result.stderr

    except FileNotFoundError:
        print(f"Error: Command not found: {command_args[0]}", file=sys.stderr)
        exit_code = 127 # Standard exit code for command not found
        stderr_str = f"Command not found: {command_args[0]}"
    except Exception as e:
        print("\n--- Error Running Command ---", file=sys.stderr)
        print(f"An unexpected error occurred: {type(e).__name__}: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print("-----------------------------", file=sys.stderr)
        exit_code = 1 # Generic error
        stderr_str = f"nrun internal error: {type(e).__name__}: {e}"

    finally:
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"Command finished in {duration:.2f}s with exit code {exit_code}", file=sys.stderr)

        # --- Prepare and Send Notification ---
        status_icon = "✅" if exit_code == 0 else "❌"
        status_text = "Succeeded" if exit_code == 0 else "Failed"
        priority = "default" if exit_code == 0 else "high"
        tags = ["heavy_check_mark", "success"] if exit_code == 0 else ["bang", "error"]
        tags.append(hostname.split('.')[0]) # Add short hostname as tag

        notif_title = f"{status_icon} {status_text} ({exit_code}) on {hostname}: {command_args[0]}"

        # Limit output length in notification to avoid excessively large messages
        stdout_snippet = (stdout_str or "").strip()[:500]
        stderr_snippet = (stderr_str or "").strip()[:500]

        notif_message = (
            f"Host: {hostname}\n"
            f"Command: {command_str}\n"
            f"Duration: {duration:.2f}s\n"
            f"Exit Code: {exit_code}\n"
        )
        if stdout_snippet:
             notif_message += f"\n--- STDOUT ---\n{stdout_snippet}\n"
             if len(stdout_str.strip()) > 500: notif_message += "[...]\n"
        if stderr_snippet:
             notif_message += f"\n--- STDERR ---\n{stderr_snippet}\n"
             if len(stderr_str.strip()) > 500: notif_message += "[...]\n"

        send_ntfy_notification(
            title=notif_title,
            message=notif_message.strip(),
            priority=priority,
            tags=tags
        )

        # Optionally print captured output to the caller's terminal
        if stdout_str:
            print("\n--- Command STDOUT ---", file=sys.stdout)
            print(stdout_str, file=sys.stdout, end='') # Avoid extra newline if output has one
        if stderr_str:
             # Only print separator if there was also stdout
            if stdout_str: print("\n--- Command STDERR ---", file=sys.stderr)
            else: print("--- Command STDERR ---", file=sys.stderr)
            print(stderr_str, file=sys.stderr, end='') # Avoid extra newline

    return exit_code # Return the exit code of the executed command

# --- Argparse Setup ---
def main():
    parser = argparse.ArgumentParser(
        description="Run a command and send an ntfy notification on completion.",
        usage="nrun <command> [args...]"
    )
    # Capture the command and all its arguments
    parser.add_argument(
        'command',
        nargs=argparse.REMAINDER, # Collects all remaining arguments into a list
        help='The command to execute followed by its arguments.'
    )
    args = parser.parse_args()

    exit_code = run_command_and_notify(args.command)
    sys.exit(exit_code) # Exit nrun with the same code as the child command

if __name__ == "__main__":
    main() 
