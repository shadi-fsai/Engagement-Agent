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
    }
    print(EngagementAgentCrew().crew().kickoff(inputs=inputs))
