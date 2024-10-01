#!/usr/bin/env python
import os
import sys
from textwrap import dedent
import json
import requests
from Engagement_Agent.crew import EngagementAgentCrew
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def post_to_discord(webhook_url, message):
  """Posts a message to a Discord webhook."""

  data = {"content": message}
  headers = {"Content-Type": "application/json"}

  response = requests.post(webhook_url, json=data, headers=headers)

  if response.status_code == 204:
    print("Message sent successfully!")
  else:
    print(f"Failed to send message. Status code: {response.status_code}")


# Example usage
webhook_url = os.getenv("DISCORD_WEBHOOK")
discordName = 'minorioshadi'
def run():
    inputs = {
        'name': 'Shadi',
        'discordName': 'minorioshadi',
        'project_description': 'Building a new example for crewAI (https://github.com/crewAIInc/crewAI) gamebuilder usin the new format, the task is to use yaml instead of hard coded values and to update documentation. Shadi started working on this last week.',
        'previous_checkin_summary': '---',
        'daysago': 'first checkin'
    }
    result = EngagementAgentCrew(discordName).crew().kickoff(inputs=inputs)
    result_json = json.dumps(result, default=str)
    post_to_discord(webhook_url, result_json)
    print(result)
