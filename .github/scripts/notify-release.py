#!/usr/bin/env python3
"""Notify community about new release (placeholder for webhook integrations)."""

import json
import os
import subprocess
import sys
from pathlib import Path


def get_release_info() -> dict:
    """Get information about the current release."""
    result = subprocess.run(
        ['git', 'describe', '--tags', '--abbrev=0'],
        capture_output=True,
        text=True
    )
    tag = result.stdout.strip() if result.returncode == 0 else 'unknown'

    skill_count = len(list(Path('.').rglob('SKILL.md')))

    result = subprocess.run(
        ['git', 'log', '-1', '--pretty=format:%s'],
        capture_output=True,
        text=True
    )
    commit_message = result.stdout.strip() if result.returncode == 0 else ''

    return {
        'tag': tag,
        'skill_count': skill_count,
        'commit_message': commit_message,
        'repository': os.environ.get('GITHUB_REPOSITORY', 'cerebratechai/claude-skills'),
    }


def send_discord_notification(release_info: dict):
    """Send notification to Discord webhook if configured."""
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("Discord webhook not configured, skipping...")
        return

    payload = {
        "embeds": [{
            "title": f"New Release: {release_info['tag']}",
            "description": f"Claude Skills collection has been updated!",
            "color": 5814783,
            "fields": [
                {"name": "Total Skills", "value": str(release_info['skill_count']), "inline": True},
                {"name": "Repository", "value": release_info['repository'], "inline": True},
            ],
            "footer": {"text": "Claude Skills Collection"}
        }]
    }

    import urllib.request
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        urllib.request.urlopen(req)
        print("Discord notification sent successfully")
    except Exception as e:
        print(f"Failed to send Discord notification: {e}")


def send_slack_notification(release_info: dict):
    """Send notification to Slack webhook if configured."""
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    if not webhook_url:
        print("Slack webhook not configured, skipping...")
        return

    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"New Release: {release_info['tag']}"}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Total Skills:*\n{release_info['skill_count']}"},
                    {"type": "mrkdwn", "text": f"*Repository:*\n{release_info['repository']}"},
                ]
            }
        ]
    }

    import urllib.request
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        urllib.request.urlopen(req)
        print("Slack notification sent successfully")
    except Exception as e:
        print(f"Failed to send Slack notification: {e}")


def main():
    """Main function to send release notifications."""
    release_info = get_release_info()

    print(f"Release Info:")
    print(f"  Tag: {release_info['tag']}")
    print(f"  Skills: {release_info['skill_count']}")
    print(f"  Repository: {release_info['repository']}")

    send_discord_notification(release_info)
    send_slack_notification(release_info)

    print("\n✅ Release notification process completed")


if __name__ == "__main__":
    main()
