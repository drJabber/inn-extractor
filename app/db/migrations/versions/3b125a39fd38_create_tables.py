"""create tables

Revision ID: 3b125a39fd38
Revises: 
Create Date: 2021-01-22 17:38:11.017835

"""
from typing import Tuple
from alembic import op
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.sql.schema import ForeignKey


# revision identifiers, used by Alembic.
revision = '3b125a39fd38'
down_revision = None
branch_labels = None
depends_on = None

def create_updated_at_trigger() -> None:
    op.execute(
        """
    CREATE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS
    $$
    BEGIN
        NEW.updated_at = now();
        RETURN NEW;
    END;
    $$ language 'mysql';
    """
    )

def timestamps() -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
    )

def create_people_table() -> None:
    op.create_table(
        "people",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("family", sa.String(200), unique=False, nullable=False, index=False),
        sa.Column("name", sa.String(200), unique=False, nullable=False, index=False),
        sa.Column("patronimic_name", sa.String(200), unique=False, nullable=True, index=False),
        sa.Column("bdate", sa.String(20)),
        sa.Column("docser", sa.String(20)),
        sa.Column("docno", sa.String(20)),
        sa.Column("docdt", sa.String(20)),
        sa.Column("snils", sa.String(20)),
        sa.Column("inn", sa.String(20), server_default="0"),
        sa.Column("status", sa.String(200), server_default=""),
        sa.Column(name="task_id", type_=sa.Integer, unique=False, nullable=False ),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id']),

    )

def create_tasks_table() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("dt", sa.String(20), unique=False, nullable=False, index=False),
        sa.Column("file", sa.LargeBinary(2**32-1), unique=False, nullable=True, index=False),
        sa.Column("state", sa.String(100), server_default="new"),
        *timestamps(),
    )

def upgrade():
    create_tasks_table()
    create_people_table()
    pass


def downgrade():
    op.drop_table('people')
    op.drop_table('tasks')
    pass
