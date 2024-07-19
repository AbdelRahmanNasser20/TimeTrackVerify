"""Add phone_number to Employee

Revision ID: e012fe234143
Revises: 
Create Date: 2024-07-18 08:05:08.061820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e012fe234143'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('events')
    op.drop_table('employees')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employees',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('employees_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='employees_pkey'),
    sa.UniqueConstraint('email', name='employees_email_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('events',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('employee_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('date', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('duration', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('position', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('location', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], name='events_employee_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='events_pkey')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key'),
    sa.UniqueConstraint('username', name='user_username_key')
    )
    # ### end Alembic commands ###
