import logging

from rasa import version

# define the version before the other imports since these need it
__version__ = version.__version__

from litellm.integrations.langfuse.langfuse import LangFuseLogger

from rasa.monkey_patches import litellm_langfuse_logger_init_fixed

# Monkey-patch the init method as early as possible before the class is used
LangFuseLogger.__init__ = litellm_langfuse_logger_init_fixed  # type: ignore

logging.getLogger(__name__).addHandler(logging.NullHandler())
