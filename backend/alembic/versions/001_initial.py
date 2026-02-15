"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('admin', 'tax_inspector', 'analyst', 'business_owner', name='userrole'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Locations table
    op.create_table(
        'locations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('address', sa.String(length=500), nullable=False),
        sa.Column('location_type', sa.Enum('cafe', 'restaurant', 'tea_house', 'hair_salon', 'car_wash', 'service_center', 'household_service', 'other', name='locationtype'), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('tax_id', sa.String(length=50), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_locations_tax_id'), 'locations', ['tax_id'], unique=True)

    # Cameras table
    op.create_table(
        'cameras',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('ip_address', sa.String(length=50), nullable=False),
        sa.Column('port', sa.Integer(), nullable=True),
        sa.Column('username', sa.String(length=100), nullable=True),
        sa.Column('password', sa.String(length=255), nullable=True),
        sa.Column('onvif_url', sa.String(length=500), nullable=True),
        sa.Column('camera_type', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('stream_url', sa.String(length=500), nullable=True),
        sa.Column('resolution', sa.String(length=50), nullable=True),
        sa.Column('fps', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Employees table
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('position', sa.String(length=100), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('passport_number', sa.String(length=50), nullable=True),
        sa.Column('is_registered', sa.Boolean(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('hire_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Employee faces table
    op.create_table(
        'employee_faces',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('face_encoding', sa.Text(), nullable=False),
        sa.Column('image_path', sa.String(length=500), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Work logs table
    op.create_table(
        'work_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('check_in', sa.DateTime(), nullable=False),
        sa.Column('check_out', sa.DateTime(), nullable=True),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Customer flows table
    op.create_table(
        'customer_flows',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('total_entered', sa.Integer(), nullable=True),
        sa.Column('total_exited', sa.Integer(), nullable=True),
        sa.Column('peak_hour', sa.Integer(), nullable=True),
        sa.Column('average_stay_time', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_flows_date'), 'customer_flows', ['date'], unique=False)

    # Customer visits table
    op.create_table(
        'customer_visits',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('flow_id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('entered_at', sa.DateTime(), nullable=False),
        sa.Column('exited_at', sa.DateTime(), nullable=True),
        sa.Column('stay_duration', sa.Float(), nullable=True),
        sa.Column('track_id', sa.String(length=100), nullable=True),
        sa.Column('is_employee', sa.Boolean(), nullable=True),
        sa.Column('employee_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['flow_id'], ['customer_flows.id'], ),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_visits_entered_at'), 'customer_visits', ['entered_at'], unique=False)

    # Analytics table
    op.create_table(
        'analytics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('real_customers', sa.Integer(), nullable=True),
        sa.Column('reported_revenue', sa.Float(), nullable=True),
        sa.Column('estimated_revenue', sa.Float(), nullable=True),
        sa.Column('average_check', sa.Float(), nullable=True),
        sa.Column('discrepancy', sa.Float(), nullable=True),
        sa.Column('discrepancy_percentage', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analytics_date'), 'analytics', ['date'], unique=False)

    # Risk scores table
    op.create_table(
        'risk_scores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('risk_score', sa.Float(), nullable=True),
        sa.Column('risk_level', sa.String(length=50), nullable=True),
        sa.Column('factors', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('unregistered_employees', sa.Integer(), nullable=True),
        sa.Column('revenue_discrepancy', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_risk_scores_date'), 'risk_scores', ['date'], unique=False)

    # Heatmaps table
    op.create_table(
        'heatmaps',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('hour', sa.Integer(), nullable=False),
        sa.Column('heatmap_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('max_intensity', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_heatmaps_date'), 'heatmaps', ['date'], unique=False)

    # Tax integrations table
    op.create_table(
        'tax_integrations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('tax_id', sa.String(length=50), nullable=False),
        sa.Column('last_sync', sa.DateTime(), nullable=True),
        sa.Column('reported_revenue', sa.Float(), nullable=True),
        sa.Column('tax_paid', sa.Float(), nullable=True),
        sa.Column('sync_status', sa.String(length=50), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # KKT integrations table
    op.create_table(
        'kkt_integrations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('kkt_serial', sa.String(length=100), nullable=False),
        sa.Column('kkt_number', sa.String(length=100), nullable=True),
        sa.Column('last_sync', sa.DateTime(), nullable=True),
        sa.Column('total_receipts', sa.Integer(), nullable=True),
        sa.Column('total_amount', sa.Float(), nullable=True),
        sa.Column('sync_status', sa.String(length=50), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('kkt_integrations')
    op.drop_table('tax_integrations')
    op.drop_table('heatmaps')
    op.drop_table('risk_scores')
    op.drop_table('analytics')
    op.drop_table('customer_visits')
    op.drop_table('customer_flows')
    op.drop_table('work_logs')
    op.drop_table('employee_faces')
    op.drop_table('employees')
    op.drop_table('cameras')
    op.drop_table('locations')
    op.drop_table('users')
