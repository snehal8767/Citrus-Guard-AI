"""Command Console route."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.engine import get_db
from app.models import User
from app.schemas.command import CommandRequest, CommandResponse
from app.services import command_parser

router = APIRouter(prefix="/commands", tags=["commands"])


@router.post("", response_model=CommandResponse)
def run_command(
    payload: CommandRequest,
    orchard_id: int = 1,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Execute a text command via the deterministic rule-based parser (NOT an LLM)."""
    return command_parser.parse_and_execute(db, payload.command, orchard_id)
