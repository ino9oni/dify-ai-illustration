from typing import Any
from tools.mystablediffusion import MystablediffusionTool
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

class MystablediffusionProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            instance = MystablediffusionTool.from_credentials(credentials)
            assert isinstance(instance, MystablediffusionTool)
            instance.validate_models()

        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))

