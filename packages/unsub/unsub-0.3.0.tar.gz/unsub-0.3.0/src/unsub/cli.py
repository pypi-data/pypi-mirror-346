import click
import datetime
import os
from unsub.applets import Downloader, Analzyer, Reviewer
from unsub.storage import DataStore
from unsub.email import IMAPClient


class DateParamType(click.ParamType):
    name = "date"

    def convert(self, value, param, ctx):
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            self.fail(f"{value!r} is not a valid date in YYYY-MM-DD format", param, ctx)


@click.group()
@click.option(
    "--imap-server",
    default="imap.gmail.com",
    help="IMAP server address (can also use UNSUB_IMAP_SERVER env var)",
)
@click.option("--email", help="Email account (can also use UNSUB_EMAIL env var)")
@click.option("--password", help="Email password (can also use UNSUB_PASSWORD env var)")
@click.option("--db-path", default="emails.db", help="Path to SQLite database")
@click.pass_context
def cli(ctx, imap_server, email, password, db_path):
    """Unsub - Email management and unsubscribe automation tool."""
    # Check environment variables if command line options aren't provided
    imap_server = imap_server or os.environ.get("UNSUB_IMAP_SERVER", "imap.gmail.com")
    email = email or os.environ.get("UNSUB_EMAIL")
    password = password or os.environ.get("UNSUB_PASSWORD")

    if not email:
        raise click.UsageError(
            "Email must be provided either via --email or UNSUB_EMAIL environment variable"
        )
    if not password:
        raise click.UsageError(
            "Password must be provided either via --password or UNSUB_PASSWORD environment variable"
        )

    ctx.ensure_object(dict)
    ctx.obj["IMAP_SERVER"] = imap_server
    ctx.obj["EMAIL"] = email
    ctx.obj["PASSWORD"] = password
    ctx.obj["DB_PATH"] = db_path


@cli.command()
@click.option(
    "--days",
    type=int,
    default=30,
    help="Number of days to check emails for",
)
@click.pass_context
def check(ctx, days):
    """Check email count from past n days."""
    with IMAPClient(
        ctx.obj["IMAP_SERVER"], ctx.obj["EMAIL"], ctx.obj["PASSWORD"]
    ) as client:
        click.echo(f"\n📊 Email Count for Past {days} Days")
        click.echo("=" * 40)

        counts = client.count_emails_past_days(days)
        total = 0
        for date, count in counts.items():
            click.echo(f"{date.strftime('%Y-%m-%d')}: {count:4d} emails")
            total += count

        click.echo("=" * 40)
        click.echo(f"Total: {total:4d} emails")


@cli.command()
@click.argument(
    "date",
    type=DateParamType(),
    required=False,
)
@click.pass_context
def download(ctx, date):
    """Download emails from a specific day.

    DATE: Specific date to download emails from (YYYY-MM-DD format). If not provided, uses today's date.
    """
    db = DataStore(ctx.obj["DB_PATH"])
    with IMAPClient(
        ctx.obj["IMAP_SERVER"], ctx.obj["EMAIL"], ctx.obj["PASSWORD"]
    ) as client:
        db.clear_database()
        downloader = Downloader(client, db)
        target_date = date or datetime.date.today()
        downloader.download_one_day(target_date)


@cli.command()
@click.pass_context
def analyze(ctx):
    """Analyze downloaded emails."""
    db = DataStore(ctx.obj["DB_PATH"])
    analyzer = Analzyer(db)
    analyzer.analyze_all()


@cli.command()
@click.pass_context
def review(ctx):
    """Review analyzed emails."""
    db = DataStore(ctx.obj["DB_PATH"])
    with IMAPClient(
        ctx.obj["IMAP_SERVER"], ctx.obj["EMAIL"], ctx.obj["PASSWORD"]
    ) as client:
        reviewer = Reviewer(db, client)
        reviewer.review_all()


def main():
    """Entry point for the unsub command."""
    cli(obj={})


if __name__ == "__main__":
    main()
