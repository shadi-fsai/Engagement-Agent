from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from Engagement_Agent.tools.message_tool import MessageTool

@CrewBase
class EngagementAgentCrew():
	"""Engagement Agent Crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	discordName = None

	def __init__(self, discordName):
		self.discordName = discordName

	@agent
	def tech_lead(self) -> Agent:
		return Agent(
			config=self.agents_config['tech_lead'],
			tools=[MessageTool(self.discordName)],
			verbose=False,  ##todo
			memory=False
		) 
	
	@task
	def project_checkin_task(self) -> Task:
		return Task(
			config=self.tasks_config['project_checkin_task'],
			agent=self.tech_lead()
		)
		
	@crew
	def crew(self) -> Crew:
		"""Creates the engagement crew"""
		
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks= self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			#planning=True,
			verbose=False, ## TODO
			output_log_file='output.log',
			log_file='crewai_logs.txt'
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)