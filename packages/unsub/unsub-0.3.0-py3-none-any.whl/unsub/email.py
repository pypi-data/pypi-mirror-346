import imaplib
import email
from email.header import decode_header
import datetime
from typing import Optional, List, Union
import email.message
import re
import email
import email.message
from email.utils import parsedate_to_datetime


class MessageFacade:
    def __init__(
        self, client: "IMAPClient", msg: email.message.Message, email_id: bytes
    ) -> None:
        self.client = client
        self.msg = msg
        self.email_id = email_id

    def body_plain(self) -> str | None:
        """Extract and return the plain text body of the email, or None if not found."""
        msg = self.msg
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if (
                    content_type == "text/plain"
                    and "attachment" not in content_disposition
                ):
                    charset = part.get_content_charset() or "utf-8"
                    try:
                        return part.get_payload(decode=True).decode(
                            charset, errors="replace"
                        )
                    except Exception:
                        continue
        else:
            content_type = msg.get_content_type()
            if content_type == "text/plain":
                charset = msg.get_content_charset() or "utf-8"
                return msg.get_payload(decode=True).decode(charset, errors="replace")
        return None

    def body_html(self) -> str | None:
        """Extract and return the HTML body of the email, or None if not found."""
        msg = self.msg
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if (
                    content_type == "text/html"
                    and "attachment" not in content_disposition
                ):
                    charset = part.get_content_charset() or "utf-8"
                    try:
                        return part.get_payload(decode=True).decode(
                            charset, errors="replace"
                        )
                    except Exception:
                        continue
        else:
            content_type = msg.get_content_type()
            if content_type == "text/html":
                charset = msg.get_content_charset() or "utf-8"
                return msg.get_payload(decode=True).decode(charset, errors="replace")
        return None

    def body(self) -> str:
        """Return the plain text body if available, otherwise fallback to HTML, otherwise a default message."""
        html = self.body_html()
        if html:
            return html
        plain = self.body_plain()
        if plain:
            return plain
        return "(No body found)"

    def from_(self):
        return self.client.decode_header_field(self.msg.get("From"))

    def subject(self):
        return self.client.decode_header_field(self.msg["Subject"])

    def received_at(self) -> datetime.datetime:
        date_str = self.msg["Date"]
        return parsedate_to_datetime(date_str)


class IMAPClient:
    def __init__(self, imap_server: str, email_account: str, password: str) -> None:
        self.imap_server: str = imap_server
        self.email_account: str = email_account
        self.password: str = password
        self.mail: Optional[imaplib.IMAP4_SSL] = None

    def connect(self) -> None:
        self.mail = imaplib.IMAP4_SSL(self.imap_server)
        self.mail.login(self.email_account, self.password)
        self.select_mailbox("INBOX")  # Automatically select INBOX after connecting

    def select_mailbox(self, mailbox: str = "inbox") -> None:
        self.mail.select(mailbox)

    def count_emails_past_days(self, days: int = 30) -> dict[datetime.date, int]:
        """Count emails for each of the past N days.

        Args:
            days: Number of past days to count emails for

        Returns:
            Dictionary mapping dates to email counts
        """
        results = {}
        today = datetime.date.today()

        for days_ago in range(days):
            date = today - datetime.timedelta(days=days_ago)
            count = self.count_emails_on_date(date)
            results[date] = count

        return results

    def count_emails_on_date(self, date: datetime.date | None = None) -> int:
        """Count emails for a specific date using IMAP's COUNT modifier."""
        if date is None:
            date = datetime.date.today()
        date_str = date.strftime("%d-%b-%Y")
        next_day = date + datetime.timedelta(days=1)
        next_day_str = next_day.strftime("%d-%b-%Y")
        status, messages = self.mail.search(
            None, f"SINCE {date_str} BEFORE {next_day_str}"
        )
        if status != "OK":
            return 0
        return len(messages[0].split())

    def email_ids_on_date(self, date: datetime.date | None = None) -> List[bytes]:
        if date is None:
            date = datetime.date.today()
        date_str = date.strftime("%d-%b-%Y")
        next_day = date + datetime.timedelta(days=1)
        next_day_str = next_day.strftime("%d-%b-%Y")
        status, messages = self.mail.search(
            None, f"SINCE {date_str} BEFORE {next_day_str}"
        )
        if status != "OK":
            print("No messages found!")
            return []
        email_ids = messages[0].split()
        if not email_ids:
            print("Inbox is empty!")
            return []
        return email_ids

    def fetch_email(self, email_id: bytes) -> Union[MessageFacade, None]:
        status, msg_data = self.mail.fetch(email_id, "(RFC822)")
        if status != "OK":
            print("Failed to fetch the email!")
            return None
        msg = email.message_from_bytes(msg_data[0][1])
        return MessageFacade(self, msg, email_id)

    @staticmethod
    def decode_header_field(field: str) -> str:
        value, encoding = decode_header(field)[0]
        if isinstance(value, bytes):
            value = value.decode(encoding if encoding else "utf-8")
        return value

    def logout(self) -> None:
        if self.mail:
            self.mail.logout()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.logout()

    def list_mailboxes(self) -> list[str]:
        """Return a list of all mailbox names available on the server."""
        if not self.mail:
            raise RuntimeError("Not connected to the mail server.")
        status, mailboxes = self.mail.list()
        if status != "OK":
            print("Failed to retrieve mailboxes!")
            return []
        mailbox_names = []
        for mbox in mailboxes:
            # mbox is a bytes object like: b'(\HasNoChildren) "/" "INBOX"'
            parts = mbox.decode().split(' "')
            if len(parts) > 1:
                name = parts[-1].strip('"')
                mailbox_names.append(name)
            else:
                # fallback: try to get last quoted string
                match = re.search(r'"([^"]+)"$', mbox.decode())
                if match:
                    mailbox_names.append(match.group(1))
        return mailbox_names

    def delete_email(self, email_id: bytes) -> bool:
        """Delete an email by its ID.

        Args:
            email_id: The IMAP ID of the email to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            # Mark the email for deletion
            self.mail.store(email_id, "+FLAGS", "\\Deleted")
            return True
        except Exception as e:
            print(f"⚠️  Error deleting email: {str(e)}")
            return False
