"""TrainLoop Evaluations CLI entry point."""

import click
from cli.commands.init import init_command as init_cmd
from cli.commands.eval import eval_command as eval_cmd
from cli.commands.studio import studio_command as studio_cmd


@click.group(invoke_without_command=True)
@click.version_option()
@click.pass_context
def cli(ctx):
    """TrainLoop Evaluations - A lightweight test harness for validating LLM behaviour.

    Run without a command to launch the local viewer (studio).
    """
    if ctx.invoked_subcommand is None:
        # Default command launches the studio viewer
        studio_cmd()


@cli.command('init')
def init():
    """Scaffold data/ and eval/ directories, create sample metrics and suites."""
    init_cmd()


@cli.command('eval')
def run_eval():
    """Discover suites, apply metrics to new events, append verdicts to data/results/."""
    eval_cmd()


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()
