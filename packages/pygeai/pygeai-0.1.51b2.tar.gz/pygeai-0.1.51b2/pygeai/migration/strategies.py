import sys
from abc import ABC, abstractmethod

from pygeai.core.models import Project
from pygeai.core.base.responses import ErrorListResponse
from pygeai.lab.managers import AILabManager
from pygeai.lab.models import Agent, Tool, AgenticProcess, Task
from pygeai.organization.managers import OrganizationManager


class MigrationStrategy(ABC):

    def __init__(
            self,
            from_api_key: str = None,
            from_instance: str = None,
            to_api_key: str = None,
            to_instance: str = None
    ):
        self.from_api_key = from_api_key
        self.from_instance = from_instance
        self.to_api_key = to_api_key if to_api_key else from_api_key
        self.to_instance = to_instance if to_instance else from_instance

    @abstractmethod
    def migrate(self):
        pass


class ProjectMigrationStrategy(MigrationStrategy):
    """
    Migrate a project from a GEAI instance.
    The target project can be in another organization or the same one; in the same instance or another.
    """

    def __init__(
            self,
            from_api_key: str = None,
            from_instance: str = None,
            to_api_key: str = None,
            to_instance: str = None,
            from_project_id: str = None,
            to_project_name: str = None,
            admin_email: str = None
    ):
        super().__init__(from_api_key, from_instance, to_api_key, to_instance)
        self.from_project_id = from_project_id
        self.to_project_name = to_project_name
        self.admin_email = admin_email
        self.source_manager = OrganizationManager(
            api_key=self.from_api_key,
            base_url=self.from_instance
        )
        self.destination_manager = OrganizationManager(
            api_key=self.to_api_key,
            base_url=self.to_instance
        )

    def migrate(self):
        response = self.__migrate_project()
        if isinstance(response, ErrorListResponse):
            return response.to_dict()
        else:
            new_project = response.project

        self.__migrate_assistants(new_project)

        sys.stdout.write(f"Migrated project: \n{response}\n")

    def __migrate_project(self):
        project_data = self.source_manager.get_project_data(project_id=self.from_project_id)

        new_project = project_data.project
        new_project.name = self.to_project_name
        new_project.email = self.admin_email
        response = self.destination_manager.create_project(new_project)

        return response

    def __migrate_assistants(self, new_project: Project):
        pass


class AgentMigrationStrategy(MigrationStrategy):
    """
    Migrate an agent from a GEAI instance.
    The target project can be in another organization or the same one; in the same instance or another.
    """

    def __init__(
            self,
            from_api_key: str = None,
            from_instance: str = None,
            to_api_key: str = None,
            to_instance: str = None,
            from_project_id: str = None,
            to_project_id: str = None,
            agent_id: str = None
    ):
        super().__init__(from_api_key, from_instance, to_api_key, to_instance)
        self.from_project_id = from_project_id
        self.to_project_id = to_project_id
        self.agent_id = agent_id
        self.source_manager = AILabManager(
            api_key=self.from_api_key,
            base_url=self.from_instance
        )
        self.destination_manager = AILabManager(
            api_key=self.to_api_key,
            base_url=self.to_instance
        )

    def migrate(self):
        new_agent = self.__migrate_agent()
        if isinstance(new_agent, ErrorListResponse):
            sys.stderr.write(f"{new_agent.to_dict()}\n")

        sys.stdout.write(f"New agent detail: \n{new_agent}\n")

    def __migrate_agent(self):
        new_agent = None
        try:
            source_agent = self.source_manager.get_agent(project_id=self.from_project_id, agent_id=self.agent_id)
            if not isinstance(source_agent, Agent):
                raise ValueError("Unable to retrieve requested agent.")

            new_agent = self.destination_manager.create_agent(project_id=self.to_project_id, agent=source_agent)
        except Exception as e:
            sys.stderr.write(f"Agent migration failed: {e} \n")

        return new_agent


class ToolMigrationStrategy(MigrationStrategy):
    """
    Migrate a tool from a GEAI instance.
    The target project can be in another organization or the same one; in the same instance or another.
    """

    def __init__(
            self,
            from_api_key: str = None,
            from_instance: str = None,
            to_api_key: str = None,
            to_instance: str = None,
            from_project_id: str = None,
            to_project_id: str = None,
            tool_id: str = None
    ):
        super().__init__(from_api_key, from_instance, to_api_key, to_instance)
        self.from_project_id = from_project_id
        self.to_project_id = to_project_id
        self.tool_id = tool_id
        self.source_manager = AILabManager(
            api_key=self.from_api_key,
            base_url=self.from_instance
        )
        self.destination_manager = AILabManager(
            api_key=self.to_api_key,
            base_url=self.to_instance
        )

    def migrate(self):
        new_tool = self.__migrate_tool()
        if isinstance(new_tool, ErrorListResponse):
            sys.stderr.write(f"{new_tool.to_dict()}\n")

        sys.stdout.write(f"New tool detail: \n{new_tool}\n")

    def __migrate_tool(self):
        new_tool = None
        try:
            source_tool = self.source_manager.get_tool(project_id=self.from_project_id, tool_id=self.tool_id)
            if not isinstance(source_tool, Tool):
                raise ValueError("Unable to retrieve requested tool.")

            new_tool = self.destination_manager.create_tool(project_id=self.to_project_id, tool=source_tool)
        except Exception as e:
            sys.stderr.write(f"Tool migration failed: {e}\n")

        return new_tool


class AgenticProcessMigrationStrategy(MigrationStrategy):
    """
    Migrate an agentic process from a GEAI instance.
    The target project can be in another organization or the same one; in the same instance or another.
    """

    def __init__(
            self,
            from_api_key: str = None,
            from_instance: str = None,
            to_api_key: str = None,
            to_instance: str = None,
            from_project_id: str = None,
            to_project_id: str = None,
            process_id: str = None
    ):
        super().__init__(from_api_key, from_instance, to_api_key, to_instance)
        self.from_project_id = from_project_id
        self.to_project_id = to_project_id
        self.process_id = process_id
        self.source_manager = AILabManager(
            api_key=self.from_api_key,
            base_url=self.from_instance
        )
        self.destination_manager = AILabManager(
            api_key=self.to_api_key,
            base_url=self.to_instance
        )

    def migrate(self):
        new_process = self.__migrate_process()
        if isinstance(new_process, ErrorListResponse):
            sys.stdout.write(f"{new_process.to_dict()}\n")

        sys.stdout.write(f"New process detail: \n{new_process}\n")

    def __migrate_process(self):
        new_process = None
        try:
            source_process = self.source_manager.get_process(project_id=self.from_project_id, process_id=self.process_id)
            if not isinstance(source_process, AgenticProcess):
                raise ValueError("Unable to retrieve requested process.")

            new_process = self.destination_manager.create_process(project_id=self.to_project_id, process=source_process)
        except Exception as e:
            sys.stderr.write(f"Process migration failed: {e}\n")

        return new_process


class TaskMigrationStrategy(MigrationStrategy):
    """
    Migrate a task from a GEAI instance.
    The target project can be in another organization or the same one; in the same instance or another.
    """

    def __init__(
            self,
            from_api_key: str = None,
            from_instance: str = None,
            to_api_key: str = None,
            to_instance: str = None,
            from_project_id: str = None,
            to_project_id: str = None,
            task_id: str = None
    ):
        super().__init__(from_api_key, from_instance, to_api_key, to_instance)
        self.from_project_id = from_project_id
        self.to_project_id = to_project_id
        self.task_id = task_id
        self.source_manager = AILabManager(
            api_key=self.from_api_key,
            base_url=self.from_instance
        )
        self.destination_manager = AILabManager(
            api_key=self.to_api_key,
            base_url=self.to_instance
        )

    def migrate(self):
        new_task = self.__migrate_task()
        if isinstance(new_task, ErrorListResponse):
            sys.stderr.write(f"{new_task.to_dict()}\n")

        sys.stdout.write(f"New task detail: \n{new_task}\n")

    def __migrate_task(self):
        new_task = None
        try:
            source_task = self.source_manager.get_task(project_id=self.from_project_id, task_id=self.task_id)
            if not isinstance(source_task, Task):
                raise ValueError("Unable to retrieve requested task.")

            new_task = self.destination_manager.create_task(project_id=self.to_project_id, task=source_task)
        except Exception as e:
            sys.stderr.write(f"Task migration failed: {e}\n")

        return new_task
