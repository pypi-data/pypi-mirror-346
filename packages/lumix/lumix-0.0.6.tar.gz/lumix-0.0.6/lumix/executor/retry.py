from typing import Any, Callable, Optional
from lumix.utils.logger import LoggerMixin


__all__ = [
    "RetryExecutor"
]


class RetryExecutor(LoggerMixin):
    """"""
    def __init__(
            self,
            max_retries: int = 3,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = False,
    ):
        """

        Args:
            max_retries:
        """
        self.max_retries = max_retries
        self.logger = logger
        self.verbose = verbose

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """

        Args:
            func:
            *args:
            **kwargs:

        Returns:

        """
        try_times = 0
        success = False

        while try_times < self.max_retries and not success:
            try_times += 1
            try:
                return func(*args, **kwargs)
            except Exception as error:
                self.info(msg=f"[{__class__.__name__}]: Attempt {try_times} failed. Retrying...")
                self.warning(msg=f"[{__class__.__name__}]: \nError: {error}\nKwargs: {kwargs}\nArgs: {args}\n")
        self.info(msg=f"[{__class__.__name__}] Retry {self.max_retries} attempts failed.")
        return None
