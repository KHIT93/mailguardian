import json
from typing import Any
from fastapi import Request
from sqlmodel import Session

from mailguardian.app.models.audit_log import AuditLog
from mailguardian.app.schemas.audit_log import AuditAction


def audit_interaction(db: Session, action: AuditAction, model: str, res_id: int, actor_id: int, request: Request = None, message: str = '', allowed: bool = True, old: dict[str, Any] = None, new: dict[str, Any] = None) -> None:
    changes: dict[str, dict[str, Any]] = {}
    if old and new:
        for change in new.keys():
            changes[change] = {
                'from': old[change] or None,
                'to': new[change] or None
            }
    db.add(AuditLog(
            action=action,
            model=model,
            res_id=res_id,
            actor_id=actor_id,
            acted_from=request.client.host if request else '::1',
            changes=json.dumps(changes),
            message=message,
            allowed=allowed
        )
    )
    db.commit()