from sqlalchemy.orm import declarative_base
import sqlalchemy

Base = declarative_base()


class Email(Base):
    __tablename__ = "emails"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    received_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    sender = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    subject = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    body = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    reviewed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    analyzed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    email_id = sqlalchemy.Column(
        sqlalchemy.String(255), nullable=True
    )  # Store the IMAP email ID

    # Analysis fields
    summary = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    unsubscribe_link = sqlalchemy.Column(sqlalchemy.String(512), nullable=True)
    unsubscribe_score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    is_marketing = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    is_mass_marketing = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    is_ai_generated = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    is_safe_to_delete = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    is_important = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
