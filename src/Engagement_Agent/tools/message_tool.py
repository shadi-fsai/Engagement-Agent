from crewai_tools import BaseTool


class MessageTool(BaseTool):
    name: str = "Message tool"
    description: str = (
        "This tool will allow you to reach out and interact with the team member you are managing. It accepts short messages and returns short messages"
    )

    def _run(self, argument: str) -> str:
        # Implementation goes here
        print ("[Manager]: " + argument + "\n")
        a = input("[Your response]:")
        return a
