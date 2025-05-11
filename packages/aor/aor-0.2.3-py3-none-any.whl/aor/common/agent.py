#
# AI-on-Rails: All rights reserved.
#

PYTHON_AGENT_TYPES = ["langchain", "langgraph", "pydantic"]
CLOUD_AGENT_TYPES = ["a2a"]


class Agent:
    """
    Represents an AI Agent agent in the application.
    """

    def __init__(
        self,
        name: str,
        type: str,
        desc: str = None,
        path: str = None,
        show_graph: bool = False,
    ):
        self.name = name
        self.desc = desc
        self.type = type
        self.show_graph = show_graph
        self.deployment = None
        self.url = None
        self.inputs = []
        self.outputs = []
        self.manual_mode = (
            False  # Flag to indicate if this agent was created in manual mode
        )
        self.protocol = "a2a"  # Default protocol
        self.framework = None  # Default framework
        
        # Generate a stable internal ID for this agent
        # This must be done before path generation since we use it for file paths
        from aor.agent_management.validation_utils import generate_stable_internal_id
        self.internal_id = generate_stable_internal_id(name)

        if path:
            # If path is provided, use it
            self.path = path
            # Validate the path exists (but don't modify it here)
            from pathlib import Path

            agent_path = Path(path)
            if not agent_path.exists():
                if agent_path.suffix == ".py":
                    # Check if there's a directory with the same name (without .py)
                    dir_path = Path(str(agent_path).replace(".py", ""))
                    if dir_path.exists() and dir_path.is_dir():
                        self.path = str(dir_path)
                else:
                    # Check if there's a file with the same name + .py
                    file_path = Path(f"{agent_path}.py")
                    if file_path.exists() and file_path.is_file():
                        self.path = str(file_path)
        elif self.is_python_agent():
            # By default, assume the Python agent is in the src directory
            # For Python agents, we'll check both file and directory options
            # Use internal_id instead of name for stable file paths
            from pathlib import Path

            file_path = Path(f"src/{self.internal_id}.py")
            dir_path = Path(f"src/{self.internal_id}")

            if file_path.exists():
                self.path = str(file_path)
            elif dir_path.exists() and dir_path.is_dir():
                self.path = str(dir_path)
            else:
                # Default to file path even if it doesn't exist yet
                self.path = f"src/{self.internal_id}.py"
        elif self.is_cloud_agent():
            # No file needed for cloud agents
            pass
        else:
            raise ValueError(f"Invalid agent type: {self.type}")

    def to_dict(self) -> dict:
        # Start with the name field
        agent = {
            "name": self.name,
        }
        
        # Add internal_id right after name
        if hasattr(self, "internal_id"):
            agent["internal_id"] = self.internal_id
            
        # Add the rest of the basic fields
        agent.update({
            "type": self.type,
            "protocol": self.protocol,  # Protocol right after type and internal_id
        })

        # Add framework if it exists (before desc/path/deployment)
        if self.framework:
            agent["framework"] = self.framework

        # Add desc, path, and deployment before inputs/outputs
        # These will appear right after protocol in the YAML
        if self.desc:
            agent["desc"] = self.desc
        if self.path:
            agent["path"] = self.path
        if self.deployment:
            agent["deployment"] = self.deployment

        # Add show_graph if needed
        if self.show_graph:
            agent["show_graph"] = self.show_graph

        # Add inputs and outputs last
        # Instructions will be inserted before these in the YAML
        if self.inputs:
            agent["inputs"] = self.inputs
        if self.outputs:
            agent["outputs"] = self.outputs

        # Add manual_mode flag if it's set
        if hasattr(self, "manual_mode") and self.manual_mode:
            agent["manual_mode"] = True

        return agent

    def is_python_agent(self) -> bool:
        return self.type in PYTHON_AGENT_TYPES

    def is_cloud_agent(self) -> bool:
        return self.type in CLOUD_AGENT_TYPES

    def __getitem__(self, key):
        """Allow dictionary-like access to agent attributes."""
        return getattr(self, key)

    @classmethod
    def from_dict(cls, agent_dict: dict) -> "Agent":
        """
        Create an Agent instance from a dictionary.

        Args:
            agent_dict: Dictionary containing agent properties

        Returns:
            Agent instance
        """
        agent = cls(
            name=agent_dict["name"],
            type=agent_dict["type"],
            desc=agent_dict.get("desc"),
            path=agent_dict.get("path"),
            show_graph=agent_dict.get("show_graph", False),
        )

        # Set additional properties
        # First check for URL at the endpoint level (preferred location)
        if "url" in agent_dict:
            agent.url = agent_dict["url"]
        
        if "deployment" in agent_dict:
            agent.deployment = agent_dict["deployment"]
            # For backward compatibility, check URL in deployment if not found at endpoint level
            if not hasattr(agent, 'url') and isinstance(agent.deployment, dict) and "url" in agent.deployment:
                agent.url = agent.deployment["url"]
        if "inputs" in agent_dict:
            agent.inputs = agent_dict["inputs"]
        if "outputs" in agent_dict:
            agent.outputs = agent_dict["outputs"]
        if "protocol" in agent_dict:
            agent.protocol = agent_dict["protocol"]
        if "framework" in agent_dict:
            agent.framework = agent_dict["framework"]
        if "manual_mode" in agent_dict:
            agent.manual_mode = agent_dict["manual_mode"]
            
        # Set internal_id if it exists in the dictionary, otherwise generate a new one
        if "internal_id" in agent_dict:
            agent.internal_id = agent_dict["internal_id"]
        else:
            # Generate a new internal ID if not present
            from aor.agent_management.validation_utils import generate_stable_internal_id
            agent.internal_id = generate_stable_internal_id(agent.name)

        return agent
