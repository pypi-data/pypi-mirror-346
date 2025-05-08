import os
import traceback
from typing import Any, Optional

from litellm.secret_managers.main import str_to_bool
from packaging.version import Version


def litellm_langfuse_logger_init_fixed(
    self: Any,  # we should not import LangfuseLogger class before we patch it
    langfuse_public_key: Optional[str] = None,
    langfuse_secret: Optional[str] = None,
    langfuse_host: str = "https://cloud.langfuse.com",
    flush_interval: int = 1,
) -> None:
    """Monkeypatched version of LangfuseLogger.__init__ from the LiteLLM library.

    This patched version removes a call that fetched the `project_id` from
    Langfuse Cloud even when it was already set via environment variables.
    In the original implementation, this call was made *before* initializing
    the LangfuseClient, which caused the application to freeze for up to 60 seconds.

    By removing this premature call, the monkeypatch avoids the unnecessary network
    request and prevents the timeout/freeze issue.

    This workaround can be removed once the underlying bug is resolved in LiteLLM:
    https://github.com/BerriAI/litellm/issues/7732
    """
    try:
        import langfuse
        from langfuse import Langfuse
    except Exception as e:
        raise Exception(
            f"\033[91mLangfuse not installed, try running 'pip install langfuse' "
            f"to fix this error: {e}\n{traceback.format_exc()}\033[0m"
        )
    # Instance variables
    self.secret_key = langfuse_secret or os.getenv("LANGFUSE_SECRET_KEY", "")
    self.public_key = langfuse_public_key or os.getenv("LANGFUSE_PUBLIC_KEY", "")

    self.langfuse_host = langfuse_host or os.getenv(
        "LANGFUSE_HOST", "https://cloud.langfuse.com"
    )
    self.langfuse_host.replace("http://", "https://")
    if not self.langfuse_host.startswith("https://"):
        self.langfuse_host = "https://" + self.langfuse_host

    self.langfuse_release = os.getenv("LANGFUSE_RELEASE")
    self.langfuse_debug = os.getenv("LANGFUSE_DEBUG")
    self.langfuse_flush_interval = (
        os.getenv("LANGFUSE_FLUSH_INTERVAL") or flush_interval
    )

    parameters = {
        "public_key": self.public_key,
        "secret_key": self.secret_key,
        "host": self.langfuse_host,
        "release": self.langfuse_release,
        "debug": self.langfuse_debug,
        "flush_interval": self.langfuse_flush_interval,  # flush interval in seconds
    }

    if Version(langfuse.version.__version__) >= Version("2.6.0"):
        parameters["sdk_integration"] = "litellm"

    self.Langfuse = Langfuse(**parameters)

    if os.getenv("UPSTREAM_LANGFUSE_SECRET_KEY") is not None:
        upstream_langfuse_debug = (
            str_to_bool(self.upstream_langfuse_debug)
            if self.upstream_langfuse_debug is not None
            else None
        )
        self.upstream_langfuse_secret_key = os.getenv("UPSTREAM_LANGFUSE_SECRET_KEY")
        self.upstream_langfuse_public_key = os.getenv("UPSTREAM_LANGFUSE_PUBLIC_KEY")
        self.upstream_langfuse_host = os.getenv("UPSTREAM_LANGFUSE_HOST")
        self.upstream_langfuse_release = os.getenv("UPSTREAM_LANGFUSE_RELEASE")
        self.upstream_langfuse_debug = os.getenv("UPSTREAM_LANGFUSE_DEBUG")
        self.upstream_langfuse = Langfuse(
            public_key=self.upstream_langfuse_public_key,
            secret_key=self.upstream_langfuse_secret_key,
            host=self.upstream_langfuse_host,
            release=self.upstream_langfuse_release,
            debug=(
                upstream_langfuse_debug
                if upstream_langfuse_debug is not None
                else False
            ),
        )
    else:
        self.upstream_langfuse = None
