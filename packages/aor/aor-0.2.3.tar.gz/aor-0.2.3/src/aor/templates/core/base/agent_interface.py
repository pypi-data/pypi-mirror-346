"""
Abstract base class for all AI-on-Rails agents.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar, Generic, Union, List
from datetime import datetime


class AgentMetadata:
    """Metadata about the agent."""
    def __init__(self, 
                 name: str,
                 description: str,
                 version: str = "1.0.0",
                 author: Optional[str] = None,
                 tags: Optional[List[str]] = None):
        self.name = name
        self.description = description
        self.version = version
        self.author = author
        self.tags = tags or []
        self.created_at = datetime.now()


# Generic type for input/output
TInput = TypeVar('TInput')
TOutput = TypeVar('TOutput')
TState = TypeVar('TState')


class BaseAgent(ABC, Generic[TInput, TOutput, TState]):
    """
    Abstract base class for all AI-on-Rails agents.
    
    This class defines the standard interface that all agents must implement.
    It supports generic types for input, output, and state to allow flexibility
    in agent implementations.
    """
    
    def __init__(self, metadata: Optional[AgentMetadata] = None):
        """
        Initialize the agent.
        
        Args:
            metadata: Optional metadata about the agent
        """
        self.metadata = metadata or AgentMetadata(
            name=self.__class__.__name__,
            description=self.__class__.__doc__ or ""
        )
        self._initialized = False
    
    async def initialize(self) -> None:
        """
        Initialize agent resources.
        This method is called once before the agent starts processing.
        """
        if not self._initialized:
            await self._initialize()
            self._initialized = True
    
    @abstractmethod
    async def _initialize(self) -> None:
        """
        Internal initialization method to be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    async def process(self, input_data: TInput) -> TOutput:
        """
        Process input and return output.
        
        Args:
            input_data: Input data to process
            
        Returns:
            Processed output
        """
        pass
    
    @abstractmethod
    async def validate_input(self, input_data: TInput) -> bool:
        """
        Validate input data before processing.
        
        Args:
            input_data: Input to validate
            
        Returns:
            True if input is valid, False otherwise
        """
        pass
    
    @abstractmethod
    async def validate_output(self, output_data: TOutput) -> bool:
        """
        Validate output data after processing.
        
        Args:
            output_data: Output to validate
            
        Returns:
            True if output is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def get_state(self) -> TState:
        """
        Get the current state of the agent.
        
        Returns:
            Current agent state
        """
        pass
    
    @abstractmethod
    def set_state(self, state: TState) -> None:
        """
        Set the state of the agent.
        
        Args:
            state: New state to set
        """
        pass
    
    async def cleanup(self) -> None:
        """
        Clean up agent resources.
        This method is called when the agent is no longer needed.
        """
        if self._initialized:
            await self._cleanup()
            self._initialized = False
    
    @abstractmethod
    async def _cleanup(self) -> None:
        """
        Internal cleanup method to be implemented by subclasses.
        """
        pass
    
    def get_metadata(self) -> AgentMetadata:
        """
        Get agent metadata.
        
        Returns:
            Agent metadata
        """
        return self.metadata
    
    @property
    def name(self) -> str:
        """Get agent name."""
        return self.metadata.name
    
    @property
    def description(self) -> str:
        """Get agent description."""
        return self.metadata.description
    
    @property
    def version(self) -> str:
        """Get agent version."""
        return self.metadata.version
    
    @property
    def is_initialized(self) -> bool:
        """Check if agent is initialized."""
        return self._initialized


class SyncBaseAgent(BaseAgent[TInput, TOutput, TState]):
    """
    Synchronous version of BaseAgent for convenience.
    Provides synchronous wrappers for all async methods.
    """
    
    def process_sync(self, input_data: TInput) -> TOutput:
        """Synchronous version of process."""
        import asyncio
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.process(input_data))
    
    def initialize_sync(self) -> None:
        """Synchronous version of initialize."""
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.initialize())
    
    def cleanup_sync(self) -> None:
        """Synchronous version of cleanup."""
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.cleanup())