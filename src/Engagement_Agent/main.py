#!/usr/bin/env python
import os
import sys
from textwrap import dedent
from Engagement_Agent.crew import EngagementAgentCrew
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def run():
    inputs = {
        'name': 'Zoro',
        'project_description': 'Building a calculator tool in CrewAI',
        'previous_checkin_summary': 'Zoro appears to be progressing with the project for CrewAIs tools library, although their brief responses make it challenging to get detailed insights into their specific accomplishments. They have indicated that they do not need any assistance and seem to be confident in their work. Zoro\'s preference for brief communication suggests that they might either be highly focused or prefer a more independent working style. \n In terms of engagement and satisfaction, Zoro has not expressed any issues or dissatisfaction with the project or with working with me, though their minimal responses might also indicate a preference for less frequent check-ins.  Progress: Zoro is working on the tools project, but specific details on accomplishments are not clear due to minimal feedback.  Issues: None reported.  Help provided: Offered support and encouragement, reassured Zoro that they can reach out for help anytime, and respected their preference for brief communication.',
        'daysago': 'two days ago'
    }
    print(EngagementAgentCrew().crew().kickoff(inputs=inputs))
