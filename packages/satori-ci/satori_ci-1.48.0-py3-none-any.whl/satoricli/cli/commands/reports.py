from argparse import ArgumentParser
from math import ceil
from typing import Optional

from satoricli.api import client
from satoricli.cli.utils import (
    autoformat,
    autotable,
    console,
    date_formatter,
    execution_time,
    get_command_params,
)

from .base import BaseCommand


class ReportsCommand(BaseCommand):
    name = "reports"

    def register_args(self, parser: ArgumentParser):
        parser.add_argument("-p", "--page", type=int, default=1)
        parser.add_argument("-l", "--limit", type=int, default=20)
        parser.add_argument("-f", "--filter")
        parser.add_argument(
            "--public", action="store_true", help="Fetch public reports"
        )

    def __call__(
        self, page: int, limit: int, filter: Optional[str], public: bool, **kwargs
    ):
        url = "/reports/public" if public else "/reports"
        res = client.get(
            url, params={"page": page, "limit": limit, "filters": filter}
        ).json()

        if not kwargs["json"]:
            if not res["total"]:
                console.print("No reports found")
                return 1

            self.print_table(res["rows"])
            console.print(
                f"Page {page} of {ceil(res['total'] / limit)} | Total: {res['total']}"
            )
        else:
            autoformat(res["rows"], jsonfmt=kwargs["json"])

    @staticmethod
    def print_table(reports: list) -> None:
        autotable(
            [
                {
                    "id": report["id"],
                    # "team": report.get("team"),
                    "params": get_command_params(report.get("run_params")),
                    "playbook_path": report.get("playbook_path"),
                    "playbook_name": report.get("playbook_name"),
                    "execution": report.get("execution"),
                    "status": report.get("status"),
                    "result": report.get("result"),
                    # "visibility": report.get("visibility"),
                    "runtime": execution_time(report.get("execution_time")),
                    # "user": report.get("user"),
                    "date": date_formatter(report.get("date")),
                }
                for report in reports
            ],
            widths=(16,),
        )
