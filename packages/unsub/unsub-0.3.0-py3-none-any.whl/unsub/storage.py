import sqlalchemy
from sqlalchemy.orm import sessionmaker
from unsub.models import Base, Email
from unsub.email import MessageFacade


class DataStore:
    def __init__(self, db_path: str = "emails.db") -> None:
        self.engine = sqlalchemy.create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def write(self, msg: MessageFacade) -> None:
        """Write the email to the database."""
        session = self.Session()
        try:
            email = Email(
                received_at=msg.received_at(),
                sender=msg.from_(),
                subject=msg.subject(),
                body=msg.body(),
                reviewed=False,
                analyzed=False,
                email_id=msg.email_id.decode(),  # Store the email ID
            )
            session.add(email)
            session.commit()
        finally:
            session.close()

    def clear_database(self) -> None:
        """Clear all data from the database."""
        session = self.Session()
        try:
            session.query(Email).delete()
            session.commit()
        finally:
            session.close()

    def get_unanalyzed_emails(self) -> list[Email]:
        """Get all unanalyzed emails."""
        session = self.Session()
        try:
            return (
                session.query(Email)
                .filter_by(analyzed=False)
                .order_by(Email.received_at.desc())
                .all()
            )
        finally:
            session.close()

    def mark_as_reviewed(self, email_id: int) -> None:
        """Mark an email as reviewed."""
        session = self.Session()
        try:
            email = session.query(Email).get(email_id)
            if email:
                email.reviewed = True
                session.commit()
        finally:
            session.close()

    def update_analysis(self, email_id: int, analysis: dict) -> None:
        """Update email with analysis results."""
        session = self.Session()
        try:
            email = session.query(Email).get(email_id)
            if email:
                email.summary = analysis.get("summary")
                email.unsubscribe_link = analysis.get("unsubscribe_link")
                email.unsubscribe_score = analysis.get(
                    "unsubscribe_score_from_0_to_100_higher_supports_unsubscribing"
                )
                email.is_marketing = analysis.get(
                    "this_email_is_likely_unsolicited_marketing_material"
                )
                email.is_mass_marketing = analysis.get(
                    "this_email_seems_part_of_a_mass_marketing_effort"
                )
                email.is_ai_generated = analysis.get(
                    "this_email_does_not_appear_to_be_written_by_a_human"
                )
                email.is_safe_to_delete = analysis.get(
                    "this_email_appears_safe_to_delete"
                )
                email.is_important = not analysis.get(
                    "this_email_does_not_appear_to_contain_important_information"
                )
                session.commit()
        finally:
            session.close()
