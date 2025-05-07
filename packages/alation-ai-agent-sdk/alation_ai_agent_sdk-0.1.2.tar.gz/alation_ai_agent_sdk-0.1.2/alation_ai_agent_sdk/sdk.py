from typing import Dict, Any, Optional

from .api import AlationAPI, AlationAPIError
from .tools import AlationContextTool


class AlationAIAgentSDK:
    def __init__(self, base_url: str, user_id: int, refresh_token: str):
        self.api = AlationAPI(base_url, user_id, refresh_token)
        self.context_tool = AlationContextTool(self.api)

    def get_context(
        self, question: str, signature: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Fetch context from Alation's catalog for a given question and signature.

        Returns either:
        - JSON context result (dict)
        - Error object with keys: message, reason, resolution_hint, response_body
        """
        try:
            return self.api.get_context_from_catalog(question, signature)
        except AlationAPIError as e:
            return {"error": e.to_dict()}

    def get_tools(self):
        return [self.context_tool]
