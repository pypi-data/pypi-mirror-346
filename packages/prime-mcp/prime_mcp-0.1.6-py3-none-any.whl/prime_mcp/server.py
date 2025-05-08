from functools import lru_cache
import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from pydantic import ValidationError

from prime_mcp.operations import CaseModel, IssueID, IssueSummaryAttributesModel
from pydantic_ai import format_as_xml

RESOURCES = Path(__file__).parent / "data"
RECOMMENDATIONS = RESOURCES / "recommendation.json"
SUMMARY = RESOURCES / "summary.json"


@lru_cache(maxsize=1)
def load_recommendations() -> str:
    with open(RECOMMENDATIONS) as f:
        try:
            data = json.load(f)
            model = CaseModel.model_validate(data)
            return format_as_xml(model, include_root_tag=False, indent=None, item_tag="item", root_tag="data")
        except ValidationError as e:
            raise ValueError(f"Invalid JSON: {e}") from e


@lru_cache(maxsize=1)
def load_summary() -> str:
    with open(SUMMARY) as f:
        data = json.load(f)
        model = IssueSummaryAttributesModel.model_validate(data)
        return format_as_xml(model, include_root_tag=False, indent=None, item_tag="item", root_tag="data")


async def main():
    mcp = FastMCP("Prime-MCP")

    @mcp.tool()
    def issue_summary(issue_id: IssueID) -> str:
        """Summarize an issue or ticket.
        Use this tool to summarize an issue when you need to provide a high-level overview of the issue.
        """
        print(f"Loading issue summary for {issue_id}")
        return load_summary()

    @mcp.tool()
    def recommendations(issue_id: IssueID) -> str:
        """Security Concerns and Recommendations for an issue or ticket.
        Use this tool when you need to:
        - Identify concerns and recommendations for an issue
        - Provide a detailed description of the issue and the recommendations to address it
        - verify implementation are aligned with the recommendations
        - when you generate code and you need to consider security
        """
        print(f"Loading recommendations for {issue_id}")
        return load_recommendations()

    await mcp.run_stdio_async()
