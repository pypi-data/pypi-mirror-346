import datetime
from marvin import Task
import dataclasses
import webbrowser
import textwrap
import sys
import tty
import termios
import time
from unsub.models import Email
from unsub.email import IMAPClient
from unsub.storage import DataStore


class Downloader:
    def __init__(self, client: IMAPClient, db: DataStore) -> None:
        self.client = client
        self.db = db

    def download_one_day(self, date: datetime.date) -> int:
        print("\n" + "=" * 80)
        print(f"📅 Downloading emails for {date.strftime('%B %d, %Y')}")
        print("=" * 80 + "\n")

        email_ids = self.client.email_ids_on_date(date)
        print(f"📧 Found {len(email_ids)} emails to process\n")

        for idx, email_id in enumerate(email_ids, 1):
            msg = self.client.fetch_email(email_id)
            print(f"⏳ Downloading email {idx}/{len(email_ids)}")
            print(f"   Subject: {msg.subject()}")
            print(f"   From: {msg.from_()}")
            print()

            if msg is not None:
                self.db.write(msg)
                print("✅ Email downloaded successfully\n")
            else:
                print("❌ Failed to process email\n")

    def download_all_days(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> None:
        """Download emails for a range of dates.

        Args:
            start_date: The first date to process
            end_date: The last date to process
        """
        current_date = start_date
        step = (
            datetime.timedelta(days=1)
            if start_date <= end_date
            else datetime.timedelta(days=-1)
        )

        while (step.days > 0 and current_date <= end_date) or (
            step.days < 0 and current_date >= end_date
        ):
            self.download_one_day(current_date)
            current_date += step


class Analzyer:
    def __init__(self, db: DataStore) -> None:
        self.db = db

    def analyze_email(self, email: Email):
        content = f"""
Date: {email.received_at}
From: {email.sender}
Subject: {email.subject}
{'-' * 80}
{email.body}
        """

        instructions = f"""
Analyze the following email.

{content}
        """

        @dataclasses.dataclass
        class EmailAnalysis:
            summary: str
            unsubscribe_link: str | None
            this_email_is_likely_unsolicited_marketing_material: bool
            this_email_does_not_appear_to_contain_important_information: bool
            this_email_appears_safe_to_delete: bool
            this_email_does_not_appear_to_be_written_by_a_human: bool
            this_email_seems_part_of_a_mass_marketing_effort: bool
            unsubscribe_score_from_0_to_100_higher_supports_unsubscribing: int

        task = Task(instructions=instructions, result_type=EmailAnalysis)
        analysis = task.run()
        return analysis

    def analyze_all(self):
        unanalyzed_emails = self.db.get_unanalyzed_emails()

        if not unanalyzed_emails:
            print("\n📭 No emails to analyze!")
            return

        print("\n" + "=" * 80)
        print("🔍 Starting Email Analysis")
        print("=" * 80 + "\n")

        for email in unanalyzed_emails:
            print("\n" + "-" * 80)
            print(f"📨 Analyzing: {email.subject}")
            print("-" * 80)

            analysis = self.analyze_email(email)
            score = (
                analysis.unsubscribe_score_from_0_to_100_higher_supports_unsubscribing
            )

            if score < 50:
                print("\n⚠️  Analysis Result:")
                print(f"   • Unsubscribe Score: {score}/100")
                print("   • Recommendation: Keep subscription")
                print("   • Reason: Email appears to be important or personal")
            elif analysis.unsubscribe_link is None:
                print("\n⚠️  Analysis Result:")
                print(f"   • Unsubscribe Score: {score}/100")
                print("   • Recommendation: Manual review needed")
                print("   • Reason: No unsubscribe link found")
            else:
                print("\n🔍 Analysis Result:")
                print(f"   • Unsubscribe Score: {score}/100")
                print(f"   • Summary: {analysis.summary}")
                print("\n📊 Key Indicators:")
                print(
                    f"   • Marketing Material: {'Yes' if analysis.this_email_is_likely_unsolicited_marketing_material else 'No'}"
                )
                print(
                    f"   • Mass Marketing: {'Yes' if analysis.this_email_seems_part_of_a_mass_marketing_effort else 'No'}"
                )
                print(
                    f"   • AI Generated: {'Yes' if analysis.this_email_does_not_appear_to_be_written_by_a_human else 'No'}"
                )
                print(
                    f"   • Safe to Delete: {'Yes' if analysis.this_email_appears_safe_to_delete else 'No'}"
                )

            # Update the email with analysis results
            session = self.db.Session()
            try:
                email = session.query(Email).get(email.id)
                if email:
                    email.summary = analysis.summary
                    email.unsubscribe_link = analysis.unsubscribe_link
                    email.unsubscribe_score = score
                    email.is_marketing = (
                        analysis.this_email_is_likely_unsolicited_marketing_material
                    )
                    email.is_mass_marketing = (
                        analysis.this_email_seems_part_of_a_mass_marketing_effort
                    )
                    email.is_ai_generated = (
                        analysis.this_email_does_not_appear_to_be_written_by_a_human
                    )
                    email.is_safe_to_delete = analysis.this_email_appears_safe_to_delete
                    email.is_important = not analysis.this_email_does_not_appear_to_contain_important_information
                    email.analyzed = True
                    session.commit()
                    print("\n✅ Email marked as analyzed in database")
            finally:
                session.close()

        print("\n" + "=" * 80)
        print("✨ Analysis Complete")
        print("=" * 80 + "\n")


def get_single_key():
    """Get a single keypress from the user without requiring Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


class Reviewer:
    def __init__(self, db: DataStore, client: IMAPClient) -> None:
        self.db = db
        self.client = client

    def display_email_review_form(self, email: Email) -> None:
        """Display email details to the user."""
        print("\n" + "=" * 80)
        print("📧 EMAIL DETAILS")
        print("=" * 80)

        # Header section with key information
        print("\n📌 HEADER")
        print("-" * 40)
        print(f"👤 From:    {email.sender}")
        print(f"📝 Subject: {email.subject}")
        print(f"🕒 Date:    {email.received_at}")
        print("-" * 40)

        # Summary section if available
        if email.summary:
            print("\n📋 SUMMARY")
            print("-" * 40)
            print(textwrap.fill(email.summary, width=100))
            print("-" * 40)

        # Analysis results with visual indicators
        print("\n🔍 ANALYSIS RESULTS")
        print("-" * 40)

        # Score with visual indicator
        if email.unsubscribe_score is not None:
            score = email.unsubscribe_score
            score_emoji = "🟢" if score < 30 else "🟡" if score < 70 else "🔴"
            print(f"{score_emoji} Unsubscribe Score: {score}/100")

        print("-" * 40)

        # Action menu
        print("\n🎯 ACTIONS")
        print("-" * 40)
        print("u - Unsubscribe")
        print("o - Open")
        print("n - Next")
        print("e - Exit")
        print("-" * 40)
        print("\nEnter your choice: ", end="")

    def handle_unsubscribe(self, email: Email) -> None:
        """Handle unsubscribe flow."""
        if not email.unsubscribe_link:
            print("❌ No unsubscribe link found for this email")
            return

        print(f"\n🔗 Unsubscribe link: {email.unsubscribe_link}")
        webbrowser.open(email.unsubscribe_link)

        # Delete the email using its ID
        if email.email_id and self.client.delete_email(email.email_id.encode()):
            print("🗑️  Email deleted from Gmail")
        else:
            print("⚠️  Could not delete email")

    def handle_open(self, email: Email) -> None:
        """Handle opening the email in browser."""
        # URL encode the subject to handle special characters
        encoded_subject = email.subject.replace(" ", "+")
        gmail_url = f"https://mail.google.com/mail/u/0/#search/{encoded_subject}"
        webbrowser.open(gmail_url)
        print("✅ Opening email in browser...")

    def review_all(self) -> None:
        """Review all unreviewed emails."""
        session = self.db.Session()
        try:
            while True:
                # Get the next unreviewed email
                email = (
                    session.query(Email)
                    .filter_by(reviewed=False, analyzed=True)
                    .order_by(Email.received_at.desc())
                    .first()
                )

                if not email:
                    print("\n📭 No unreviewed emails found! Sleeping for 10 seconds...")
                    time.sleep(10)
                    continue

                self.display_email_review_form(email)

                while True:
                    choice = get_single_key().lower()
                    if choice in ["u", "o", "n", "e"]:
                        break
                    print("\rInvalid choice. Please press u, o, n, or e: ", end="")

                if choice == "u":
                    self.handle_unsubscribe(email)
                elif choice == "o":
                    self.handle_open(email)
                elif choice == "n":
                    print("⏭️ Skipping to next email...")
                elif choice == "e":
                    print("\n👋 Exiting email review...")
                    return

                print("Marking email as reviewed...")
                self.db.mark_as_reviewed(email.id)

        finally:
            session.close()
