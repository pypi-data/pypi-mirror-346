import asyncio
import logging

import dotenv
import typer
from gwproactor.command_line_utils import run_async_main
from gwproactor_test.certs import generate_dummy_certs

from gwupload.stubs.ingester.ingester import StubIngesterApp

app = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_enable=False,
    rich_markup_mode="rich",
    help="GridWorks Dummy Ingester",
)


@app.command()
def run(
    *,
    env_file: str = ".env",
    dry_run: bool = False,
    verbose: bool = False,
    message_summary: bool = False,
    log_events: bool = False,
) -> None:
    """Run the stub ingester"""

    env_file = dotenv.find_dotenv(filename=env_file, usecwd=True)
    app_settings = StubIngesterApp.get_settings(
        env_file=env_file,
    )
    if log_events:
        app_settings.event_logger_level = logging.INFO
    asyncio.run(
        run_async_main(
            app_settings=app_settings,
            app_type=StubIngesterApp,
            env_file=env_file,
            dry_run=dry_run,
            verbose=verbose,
            message_summary=message_summary,
        )
    )


@app.command()
def gen_test_certs(*, dry_run: bool = False, env_file: str = ".env") -> None:
    """Generate test certs for the stub ingester."""
    generate_dummy_certs(
        StubIngesterApp(env_file=dotenv.find_dotenv(env_file, usecwd=True)).settings,
        dry_run=dry_run,
    )


@app.command()
def config(
    env_file: str = ".env",
) -> None:
    """Show stub ingester configuration"""
    StubIngesterApp.print_settings(env_file=env_file)


@app.callback()
def _main() -> None: ...


if __name__ == "__main__":
    app()
