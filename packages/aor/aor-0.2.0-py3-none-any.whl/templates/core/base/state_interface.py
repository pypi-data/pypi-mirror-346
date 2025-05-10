"""
Base state interface for all AI-on-Rails agents.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, TypeVar, Generic
from datetime import datetime
from pydantic import BaseModel, Field


class BaseState(BaseModel, ABC):
    """
    Abstract base state class for all agents.
    
    This class defines the minimum state requirements that all agents must support.
    Each agent can extend this with additional state fields as needed.
    """
    
    # Basic state fields that all agents should have
    agent_id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    session_id: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Processing state
    processing_status: str = Field(default="idle")  # idle, processing, completed, error
    error_message: Optional[str] = Field(default=None)
    
    # Metadata for tracking
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # History of operations
    history: List[Dict[str, Any]] = Field(default_factory=list)
    
    def update_status(self, status: str, error: Optional[str] = None) -> None:
        """
        Update the processing status.
        
        Args:
            status: New status
            error: Optional error message
        """
        self.processing_status = status
        self.error_message = error
        self.updated_at = datetime.now()
    
    def add_to_history(self, operation: str, details: Dict[str, Any]) -> None:
        """
        Add an operation to the history.
        
        Args:
            operation: Operation name
            details: Operation details
        """
        self.history.append({
            "operation": operation,
            "details": details,
            "timestamp": datetime.now()
        })
        self.updated_at = datetime.now()
    
    def set_metadata(self, key: str, value: Any) -> None:
        """
        Set a metadata value.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value
        self.updated_at = datetime.now()
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """
        Get a metadata value.
        
        Args:
            key: Metadata key
            default: Default value if key not found
        
        Returns:
            Metadata value or default
        """
        return self.metadata.get(key, default)
    
    def clear_history(self) -> None:
        """Clear the operation history."""
        self.history.clear()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary."""
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseState':
        """Create state from dictionary."""
        return cls.model_validate(data)
    
    class Config:
        arbitrary_types_allowed = True


# Generic type for extended state
TState = TypeVar('TState', bound=BaseState)


class StatefulAgent(Generic[TState]):
    """
    Mixin for agents that need to maintain state.
    """
    
    def __init__(self, state_class: type[TState]):
        """
        Initialize with state class.
        
        Args:
            state_class: Class to use for state
        """
        self._state_class = state_class
        self._state: TState = state_class()
    
    @property
    def state(self) -> TState:
        """Get current state."""
        return self._state
    
    @state.setter
    def state(self, new_state: TState) -> None:
        """Set new state."""
        if not isinstance(new_state, self._state_class):
            raise TypeError(f"State must be of type {self._state_class.__name__}")
        self._state = new_state
    
    def reset_state(self) -> None:
        """Reset state to initial values."""
        self._state = self._state_class()
    
    def save_state(self, path: str) -> None:
        """
        Save state to file.
        
        Args:
            path: File path to save state
        """
        import json
        with open(path, 'w') as f:
            json.dump(self._state.to_dict(), f, default=str)
    
    def load_state(self, path: str) -> None:
        """
        Load state from file.
        
        Args:
            path: File path to load state from
        """
        import json
        with open(path, 'r') as f:
            data = json.load(f)
            self._state = self._state_class.from_dict(data)


class SimpleState(BaseState):
    """
    Simple state implementation for basic agents.
    Can be used as-is or extended with additional fields.
    """
    
    # Additional simple fields
    input_data: Optional[Dict[str, Any]] = Field(default=None)
    output_data: Optional[Dict[str, Any]] = Field(default=None)
    intermediate_results: List[Dict[str, Any]] = Field(default_factory=list)
    
    def add_intermediate_result(self, result: Dict[str, Any]) -> None:
        """Add an intermediate result."""
        self.intermediate_results.append(result)
        self.updated_at = datetime.now()
    
    def clear_intermediate_results(self) -> None:
        """Clear intermediate results."""
        self.intermediate_results.clear()
        self.updated_at = datetime.now()