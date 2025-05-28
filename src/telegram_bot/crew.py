from langchain_openai import ChatOpenAI
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.telegram_bot.tools.google_calendar_tool import create_event, update_event, delete_event
from src.telegram_bot.tools.gmail_tool import send_email
import logging
import sys
import os

# Pastikan path tools bisa diakses

logger = logging.getLogger(__name__)

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class TelegramBot():
	"""TelegramBot crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	schedule_tools = [create_event, update_event, delete_event]
	gmail_tool = [send_email]
	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def manager(self) -> Agent:
		return Agent(
			config=self.agents_config['manager'],
			verbose=True,
			allow_delegation=True,
		)
	
	@agent
	def schedule_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['schedule_agent'],
			verbose=True,
			tools=self.schedule_tools,
		)
	
	@agent
	def gmail_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['gmail_agent'],
			verboser=True,
			tools=self.gmail_tool,
		)
	

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task

	@task
	def handle_query(self) -> Task:
		return Task(
			config=self.tasks_config['handle_query'],
		)
	
	@task
	def gmail_task(self) -> Task:
		return Task(
			config=self.tasks_config['send_email_task'],
		)
	
	@task
	def schedule_task(self) -> Task:
		return Task(
			config=self.tasks_config['schedule_task'],
		)


	manager_llm = LLM(model="gpt-4o")
	@crew
	def crew(self) -> Crew:
		"""Creates the TelegramBot crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=[self.schedule_agent(), self.gmail_agent()], # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			manager_agent=self.manager(),
			process=Process.hierarchical,
			verbose=True,
			planning=True,
		)
