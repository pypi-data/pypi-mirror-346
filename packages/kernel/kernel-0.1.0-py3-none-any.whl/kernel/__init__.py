from typing import Callable, Dict, Any, TypeVar, Optional, List
import functools

class Request:
    def __init__(self, query: Optional[Dict[str, str]] = None, body: Any = None):
        self.query = query or {}
        self.body = body

T = TypeVar('T')
BrowserFunc = Callable[..., T]

# Registry for storing Kernel functions
class KernelRegistryItem:
    def __init__(self, name: str, type: str, handler: Callable, uses_browser: bool = False, **kwargs):
        self.name = name
        self.type = type
        self.handler = handler
        for key, value in kwargs.items():
            setattr(self, key, value)

class KernelRegistry:
    def __init__(self):
        self.registry: Dict[str, KernelRegistryItem] = {}
    
    def register(self, item: KernelRegistryItem) -> None:
        self.registry[item.name] = item
    
    def get_all(self) -> List[KernelRegistryItem]:
        return list(self.registry.values())
    
    def get_by_name(self, name: str) -> Optional[KernelRegistryItem]:
        return self.registry.get(name)
    
    def get_by_type(self, type: str) -> List[KernelRegistryItem]:
        return [item for item in self.get_all() if item.type == type]

# Create a singleton registry
registry = KernelRegistry()

def func(f: Callable) -> Callable:
    """Decorator to mark a function as deployable"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    registry.register(KernelRegistryItem(
        name=f.__name__,
        type='function',
        handler=f,
    ))
    
    return wrapper

def endpoint(method: str, path: str) -> Callable[[Callable], Callable]:
    """Decorator to mark a function as an HTTP endpoint"""
    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        registry.register(KernelRegistryItem(
            name=f.__name__,
            type='http',
            handler=f,
            path=path,
            method=method
        ))
        
        return wrapper
    return decorator

def schedule(cron_expression: str) -> Callable[[Callable], Callable]:
    """Decorator to mark a function as a scheduled task"""
    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        registry.register(KernelRegistryItem(
            name=f.__name__,
            type='schedule',
            handler=f,
            cron=cron_expression
        ))
        
        return wrapper
    return decorator

class Browser:
    def __init__(self):
        self.cdp_ws_url = "ws://localhost:9222"

def use_browser(browser_fn: BrowserFunc) -> Any:
    """Run a function with a browser instance
    
    The returned browser object contains cdp_ws_url which should be used with playwright:
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(browser.cdp_ws_url)
    """
    browser = Browser()
    return browser_fn(browser)
