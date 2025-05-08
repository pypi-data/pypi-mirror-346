from typing import Type, Optional, Callable, Awaitable, Dict, Any, Union
from dataclasses import dataclass, field
from retrosys.core.dependency_injection.project_types import (
    Lifecycle,
    ResolutionStrategy,
    FactoryCallable,
    AsyncFactoryCallable,
)


@dataclass
class ServiceDescriptor:
    """Describes a registered service."""

    service_type: Type  # The type to register
    implementation_type: Optional[Type] = (
        None  # The concrete implementation (if different)
    )
    lifecycle: Lifecycle = Lifecycle.SINGLETON
    factory: Optional[Union[FactoryCallable, AsyncFactoryCallable]] = None
    instance: Any = None  # For singletons
    context_key: str = ""  # For contextual binding
    is_async: bool = False  # Whether this is an async service
    resolution_strategy: ResolutionStrategy = ResolutionStrategy.EAGER
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Lifecycle hooks
    on_init: Optional[Callable[[Any], Optional[Awaitable[None]]]] = None
    on_destroy: Optional[Callable[[Any], Optional[Awaitable[None]]]] = None

    # Dependencies to inject via properties or methods
    property_injections: Dict[str, Type] = field(
        default_factory=dict
    )  # field to ensure a dict for each instance
    method_injections: Dict[str, Dict[str, Type]] = field(default_factory=dict)

    def is_resolved(self) -> bool:
        """Determines if the service instance has been resolved/initialized.

        This method checks whether a service has been instantiated based on its lifecycle.
        For singleton services, it verifies if the instance attribute is populated.
        For non-singleton services, it always returns False since they are created
        on-demand and not cached.

        Returns:
            bool: True if the service is a singleton and has been instantiated,
                False otherwise.
        """

        return (
            self.instance is not None
            if self.lifecycle == Lifecycle.SINGLETON
            else False
        )
