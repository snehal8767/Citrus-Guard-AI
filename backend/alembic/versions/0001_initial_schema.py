"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-10-04

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False, server_default="farmer"),
        sa.Column("full_name", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_users_username", "users", ["username"])

    op.create_table(
        "orchards",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("area", sa.Float(), nullable=False),
        sa.Column("crop", sa.String(length=64), nullable=False, server_default="Orange (Nagpur Santra)"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "orchard_zones",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("orchard_id", sa.Integer(), nullable=False),
        sa.Column("zone_name", sa.String(length=64), nullable=False),
        sa.Column("area", sa.Float(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("health_status", sa.String(length=32), nullable=False, server_default="Healthy"),
        sa.Column("risk_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.CheckConstraint("risk_score >= 0 AND risk_score <= 100", name="ck_zone_risk_score"),
        sa.ForeignKeyConstraint(["orchard_id"], ["orchards.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_orchard_zones_orchard_id", "orchard_zones", ["orchard_id"])

    op.create_table(
        "scans",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("orchard_id", sa.Integer(), nullable=False),
        sa.Column("scan_type", sa.String(length=64), nullable=False, server_default="drone_simulation"),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=True),
        sa.Column("coverage", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="Completed"),
        sa.ForeignKeyConstraint(["orchard_id"], ["orchards.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_scans_orchard_id", "scans", ["orchard_id"])
    op.create_index("ix_scans_timestamp", "scans", ["timestamp"])

    op.create_table(
        "ai_detections",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("scan_id", sa.Integer(), nullable=False),
        sa.Column("zone_id", sa.Integer(), nullable=False),
        sa.Column("condition", sa.String(length=64), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("confidence >= 0 AND confidence <= 100", name="ck_detection_confidence"),
        sa.CheckConstraint(
            "severity IN ('Low','Medium','High','Critical')", name="ck_detection_severity"
        ),
        sa.ForeignKeyConstraint(["scan_id"], ["scans.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["zone_id"], ["orchard_zones.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_ai_detections_scan_id", "ai_detections", ["scan_id"])
    op.create_index("ix_ai_detections_zone_id", "ai_detections", ["zone_id"])

    op.create_table(
        "sensor_readings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("zone_id", sa.Integer(), nullable=False),
        sa.Column("soil_moisture", sa.Float(), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False),
        sa.Column("humidity", sa.Float(), nullable=False),
        sa.Column("leaf_wetness", sa.Float(), nullable=False),
        sa.Column("irrigation_status", sa.String(length=32), nullable=False, server_default="Off"),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["zone_id"], ["orchard_zones.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_sensor_readings_zone_id", "sensor_readings", ["zone_id"])
    op.create_index("ix_sensor_readings_timestamp", "sensor_readings", ["timestamp"])

    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("zone_id", sa.Integer(), nullable=False),
        sa.Column("alert_type", sa.String(length=64), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="New"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("risk_score >= 0 AND risk_score <= 100", name="ck_alert_risk_score"),
        sa.ForeignKeyConstraint(["zone_id"], ["orchard_zones.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_alerts_zone_id", "alerts", ["zone_id"])
    op.create_index("ix_alerts_created_at", "alerts", ["created_at"])

    op.create_table(
        "farmer_verifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("alert_id", sa.Integer(), nullable=False),
        sa.Column("decision", sa.String(length=32), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["alert_id"], ["alerts.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_farmer_verifications_alert_id", "farmer_verifications", ["alert_id"])

    op.create_table(
        "interventions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("zone_id", sa.Integer(), nullable=False),
        sa.Column("intervention_type", sa.String(length=64), nullable=False),
        sa.Column("target_area", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="Planned"),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["zone_id"], ["orchard_zones.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_interventions_zone_id", "interventions", ["zone_id"])

    op.create_table(
        "historical_monitoring",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("orchard_id", sa.Integer(), nullable=False),
        sa.Column("zone_id", sa.Integer(), nullable=False),
        sa.Column("scan_id", sa.Integer(), nullable=True),
        sa.Column("health_score", sa.Float(), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("affected_area", sa.Float(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["orchard_id"], ["orchards.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["zone_id"], ["orchard_zones.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["scan_id"], ["scans.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_historical_monitoring_orchard_id", "historical_monitoring", ["orchard_id"])
    op.create_index("ix_historical_monitoring_zone_id", "historical_monitoring", ["zone_id"])
    op.create_index("ix_historical_monitoring_recorded_at", "historical_monitoring", ["recorded_at"])


def downgrade() -> None:
    op.drop_table("historical_monitoring")
    op.drop_table("interventions")
    op.drop_table("farmer_verifications")
    op.drop_table("alerts")
    op.drop_table("sensor_readings")
    op.drop_table("ai_detections")
    op.drop_table("scans")
    op.drop_table("orchard_zones")
    op.drop_table("orchards")
    op.drop_table("users")
