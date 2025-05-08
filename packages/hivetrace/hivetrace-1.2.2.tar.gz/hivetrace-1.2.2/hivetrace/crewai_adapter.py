import functools
import uuid
from typing import Any, Callable, Dict, Optional

from crewai import Agent, Crew, Task


class CrewAIAdapter:
    """
    Integration adapter for monitoring CrewAI agents with Hivetrace.
    """

    def __init__(
        self,
        hivetrace,
        application_id: Optional[str] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ):
        """
        Initialize the CrewAI adapter.
        """

        self.trace = hivetrace
        self.application_id = application_id or str(uuid.uuid4())
        self.user_id = user_id or str(uuid.uuid4())
        self.session_id = session_id or str(uuid.uuid4())
        self.async_mode = self.trace.async_mode
        self.original_kickoff = None
        self.original_kickoff_async = None

    async def input_async(
        self, message: str, additional_params: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Asynchronously logs user input to Hivetrace.
        """
        if not self.async_mode:
            raise RuntimeError("Cannot use async methods when SDK is in sync mode")

        params = additional_params or {}
        params.update(
            {
                "user_id": self.user_id,
                "session_id": self.session_id,
            }
        )

        try:
            await self.trace.input_async(
                application_id=self.application_id,
                message=message,
                additional_parameters=params,
            )
        except Exception as e:
            print(f"Error logging input to Hivetrace: {e}")

    def input(
        self, message: str, additional_params: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Synchronously logs user input to Hivetrace.
        """
        if self.async_mode:
            raise RuntimeError("Cannot use sync methods when SDK is in async mode")

        params = additional_params or {}
        params.update(
            {
                "user_id": self.user_id,
                "session_id": self.session_id,
            }
        )

        try:
            self.trace.input(
                application_id=self.application_id,
                message=message,
                additional_parameters=params,
            )
        except Exception as e:
            print(f"Error logging input to Hivetrace: {e}")

    async def output_async(
        self,
        message: str,
        agent_name: Optional[str] = None,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Asynchronously logs agent output to Hivetrace.
        """
        if not self.async_mode:
            raise RuntimeError("Cannot use async methods when SDK is in sync mode")

        params = additional_params or {}
        params.update(
            {
                "user_id": self.user_id,
                "session_id": self.session_id,
            }
        )

        if agent_name:
            params["agent_name"] = agent_name

        try:
            await self.trace.output_async(
                application_id=self.application_id,
                message=message,
                additional_parameters=params,
            )
        except Exception as e:
            print(f"Error logging output to Hivetrace: {e}")

    def output(
        self,
        message: str,
        agent_name: Optional[str] = None,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Synchronously logs agent output to Hivetrace.
        """
        if self.async_mode:
            raise RuntimeError("Cannot use sync methods when SDK is in async mode")

        params = additional_params or {}
        params.update(
            {
                "user_id": self.user_id,
                "session_id": self.session_id,
            }
        )

        if agent_name:
            params["agent_name"] = agent_name

        try:
            self.trace.output(
                application_id=self.application_id,
                message=message,
                additional_parameters=params,
            )
        except Exception as e:
            print(f"Error logging output to Hivetrace: {e}")

    def agent_callback(self, message: Any) -> None:
        """
        Handler for agent messages.
        Formats and logs agent messages to Hivetrace.
        """
        try:
            agent_name = None
            if hasattr(message, "agent") and hasattr(message.agent, "role"):
                agent_name = message.agent.role

            message_text = ""
            if hasattr(message, "__dict__"):
                message_type = message.__class__.__name__
                details = []
                for key, value in message.__dict__.items():
                    if key not in ["__dict__", "__weakref__"]:
                        details.append(f"{key}: {value}")
                message_text = f"[Agent {message_type}] {' | '.join(details)}"
            else:
                message_text = f"[Agent] {str(message)}"

            if self.async_mode:
                import asyncio

                asyncio.create_task(
                    self.output_async(message_text, agent_name=agent_name)
                )
            else:
                self.output(message_text, agent_name=agent_name)
        except Exception as e:
            error_text = f"[Agent] Error logging: {str(e)} | Object: {message}"
            if self.async_mode:
                import asyncio

                asyncio.create_task(self.output_async(error_text))
            else:
                self.output(error_text)

    def task_callback(self, message: Any) -> None:
        """
        Handler for task messages.
        Formats and logs task messages to Hivetrace.
        """
        try:
            message_text = ""
            if hasattr(message, "__dict__"):
                details = []
                for key, value in message.__dict__.items():
                    if key not in ["__dict__", "__weakref__"]:
                        details.append(f"{key}: {value}")
                message_text = f"[Task] {' | '.join(details)}"
            else:
                message_text = f"[Task] {str(message)}"

            if self.async_mode:
                import asyncio

                asyncio.create_task(self.log_output_async(message_text))
            else:
                self.log_output(message_text)
        except Exception as e:
            error_text = f"[Task] Error logging: {str(e)} | Object: {message}"
            if self.async_mode:
                import asyncio

                asyncio.create_task(self.log_output_async(error_text))
            else:
                self.log_output(error_text)

    def _wrap_agent(self, agent: Agent) -> Agent:
        """
        Adds monitoring to the agent.
        Wraps existing agent callbacks to add logging.
        """
        original_callback = agent.callback

        def combined_callback(message):
            self.agent_callback(message)
            if original_callback:
                original_callback(message)

        agent.callback = combined_callback

        original_step_callback = agent.step_callback

        def combined_step_callback(message):
            self.agent_callback(message)
            if original_step_callback:
                original_step_callback(message)

        agent.step_callback = combined_step_callback
        return agent

    def _wrap_task(self, task: Task) -> Task:
        """
        Adds monitoring to the task.
        Wraps existing task callbacks to add logging.
        """
        original_callback = task.callback

        def combined_callback(message):
            self.task_callback(message)
            if original_callback:
                original_callback(message)

        task.callback = combined_callback
        return task

    def wrap_crew(self, crew: Crew) -> Crew:
        """
        Adds monitoring to the existing CrewAI crew.
        Wraps all agents and tasks in the crew, as well as the kickoff methods.
        """
        crew.agents = [self._wrap_agent(agent) for agent in crew.agents]
        crew.tasks = [self._wrap_task(task) for task in crew.tasks]

        if not self.original_kickoff:
            self.original_kickoff = crew.kickoff

            @functools.wraps(crew.kickoff)
            def wrapped_kickoff(*args, **kwargs):
                if "inputs" in kwargs and "request" in kwargs["inputs"]:
                    if self.async_mode:
                        import asyncio

                        asyncio.create_task(
                            self.log_input_async(kwargs["inputs"]["request"])
                        )
                    else:
                        self.log_input(kwargs["inputs"]["request"])

                result = self.original_kickoff(*args, **kwargs)

                if result:
                    final_message = f"[Final Result] {str(result)}"
                    if self.async_mode:
                        import asyncio

                        asyncio.create_task(self.log_output_async(final_message))
                    else:
                        self.log_output(final_message)

                return result

            crew.kickoff = wrapped_kickoff

        if hasattr(crew, "kickoff_async") and not self.original_kickoff_async:
            self.original_kickoff_async = crew.kickoff_async

            @functools.wraps(crew.kickoff_async)
            async def wrapped_kickoff_async(*args, **kwargs):
                if "inputs" in kwargs and "request" in kwargs["inputs"]:
                    if self.async_mode:
                        await self.log_input_async(kwargs["inputs"]["request"])
                    else:
                        self.log_input(kwargs["inputs"]["request"])

                result = await self.original_kickoff_async(*args, **kwargs)

                if result:
                    final_message = f"[Final Result] {str(result)}"
                    if self.async_mode:
                        await self.log_output_async(final_message)
                    else:
                        self.log_output(final_message)

                return result

            crew.kickoff_async = wrapped_kickoff_async

        return crew

    def track_crew(self, crew_setup_func: Callable) -> Callable:
        """
        Decorator for tracking the crew.
        Wraps the crew setup function to add monitoring.
        """

        @functools.wraps(crew_setup_func)
        def wrapper(*args, **kwargs):
            crew = crew_setup_func(*args, **kwargs)
            return self.wrap_crew(crew)

        return wrapper


def track_crew(
    hivetrace,
    application_id: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
):
    """
    Decorator for tracking the CrewAI crew.
    Creates an adapter and applies it to the crew setup function.
    """
    if callable(hivetrace):
        raise ValueError(
            "track_crew requires at least the hivetrace parameter. "
            "Use @track_crew(hivetrace=your_hivetrace_instance)"
        )

    adapter = CrewAIAdapter(
        hivetrace=hivetrace,
        application_id=application_id,
        user_id=user_id,
        session_id=session_id,
    )

    def decorator(crew_setup_func):
        return adapter.track_crew(crew_setup_func)

    return decorator
