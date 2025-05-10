"""
Abstract base class for protocol adapters.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar, Optional, Callable, Awaitable, Union
from pydantic import BaseModel

# Type variables for input and output types
TProtocolInput = TypeVar('TProtocolInput')
TProtocolOutput = TypeVar('TProtocolOutput')
TAgentInput = TypeVar('TAgentInput')
TAgentOutput = TypeVar('TAgentOutput')


class ProtocolMetadata(BaseModel):
    """Metadata about the protocol adapter."""
    name: str
    description: str
    version: str
    capabilities: Dict[str, Any] = {}
    author: Optional[str] = None
    tags: list[str] = []


class ProtocolAdapter(ABC, Generic[TProtocolInput, TProtocolOutput, TAgentInput, TAgentOutput]):
    """
    Abstract base class for protocol adapters.
    
    Protocol adapters handle conversion between protocol-specific formats
    and the agent's internal format.
    """
    
    def __init__(self, 
                 agent_function: Callable[[TAgentInput], Union[TAgentOutput, Awaitable[TAgentOutput]]],
                 metadata: Optional[ProtocolMetadata] = None):
        """
        Initialize the protocol adapter.
        
        Args:
            agent_function: The core agent function to wrap
            metadata: Optional metadata about the protocol adapter
        """
        self.agent_function = agent_function
        self.metadata = metadata or ProtocolMetadata(
            name=self.__class__.__name__,
            description=self.__class__.__doc__ or ""
        )
    
    @abstractmethod
    async def convert_to_internal(self, protocol_input: TProtocolInput) -> TAgentInput:
        """
        Convert protocol-specific input to agent's internal format.
        
        Args:
            protocol_input: Input in protocol-specific format
            
        Returns:
            Input in agent's internal format
        """
        pass
    
    @abstractmethod
    async def convert_to_protocol(self, agent_output: TAgentOutput, 
                                  session_id: Optional[str] = None) -> TProtocolOutput:
        """
        Convert agent's output to protocol-specific format.
        
        Args:
            agent_output: Output from the agent
            session_id: Optional session identifier
            
        Returns:
            Output in protocol-specific format
        """
        pass
    
    async def process_request(self, protocol_input: TProtocolInput) -> TProtocolOutput:
        """
        Process a protocol request end-to-end.
        
        Args:
            protocol_input: Input in protocol-specific format
            
        Returns:
            Output in protocol-specific format
        """
        try:
            # Convert to internal format
            internal_input = await self.convert_to_internal(protocol_input)
            
            # Process with agent
            result = self.agent_function(internal_input)
            if hasattr(result, "__await__"):
                internal_output = await result
            else:
                internal_output = result
            
            # Convert to protocol format
            protocol_output = await self.convert_to_protocol(
                internal_output, 
                getattr(protocol_input, 'session_id', None)
            )
            
            return protocol_output
            
        except Exception as e:
            # Handle errors according to protocol
            return await self.handle_error(e, protocol_input)
    
    @abstractmethod
    async def handle_error(self, error: Exception, 
                          protocol_input: TProtocolInput) -> TProtocolOutput:
        """
        Handle errors in a protocol-specific way.
        
        Args:
            error: The exception that occurred
            protocol_input: The original input that caused the error
            
        Returns:
            Error response in protocol-specific format
        """
        pass
    
    def get_metadata(self) -> ProtocolMetadata:
        """Get protocol adapter metadata."""
        return self.metadata