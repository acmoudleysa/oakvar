from .decorators import cli_func
from .decorators import cli_entry


@cli_entry
@cli_func
def issue(__args__):
    from .admin_util import report_issue

    return report_issue()


def get_parser_fn_issue():
    from argparse import ArgumentParser

    # opens issue report
    parser_fn_feedback = (
        ArgumentParser()
    )  # "feedback", help="opens a browser window to report issues")
    parser_fn_feedback.add_argument(
        "--quiet", action="store_true", default=None, help="Run quietly"
    )
    parser_fn_feedback.set_defaults(func=issue)
    return parser_fn_feedback
