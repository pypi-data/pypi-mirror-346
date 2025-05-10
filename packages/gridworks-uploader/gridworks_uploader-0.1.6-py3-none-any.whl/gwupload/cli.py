import asyncio

import dotenv
import typer
from gwproactor.command_line_utils import run_async_main
from gwproactor.logging_setup import enable_aiohttp_logging
from gwproactor_test.certs import generate_dummy_certs

from gwupload import UploaderApp
from gwupload.stubs import stubs_cli

cli_app = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_enable=False,
    rich_markup_mode="rich",
    help="GridWorks Uploader",
)

cli_app.add_typer(stubs_cli.app, name="stubs", help="Use stub applications for testing")


@cli_app.command()
def run(
    env_file: str = ".env",
    *,
    dry_run: bool = False,
    verbose: bool = False,
    message_summary: bool = False,
    aiohttp_verbose: bool = False,
) -> None:
    """Run the uploader."""
    if aiohttp_verbose:
        enable_aiohttp_logging()
    asyncio.run(
        run_async_main(
            app_type=UploaderApp,
            env_file=env_file,
            dry_run=dry_run,
            verbose=verbose,
            message_summary=message_summary,
        )
    )


@cli_app.command()
def config(
    env_file: str = ".env",
) -> None:
    """Show uploader configuration"""
    UploaderApp.print_settings(env_file=env_file)


@cli_app.command()
def gen_test_certs(*, dry_run: bool = False, env_file: str = ".env") -> None:
    """Generate test certs for the uploader."""
    generate_dummy_certs(
        UploaderApp(env_file=dotenv.find_dotenv(env_file, usecwd=True)).settings,
        dry_run=dry_run,
    )


@cli_app.callback()
def _main() -> None: ...


if __name__ == "__main__":
    cli_app()
