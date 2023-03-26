from app.permissions.model import UserAssignedAccess
from sqlalchemy.orm import Session
from app.settings.model import UserRelationSettings


def get_notifying_list(user_id: int, db: Session):
    user_granted_notify_to = (
        db.query(UserAssignedAccess)
        .filter(UserAssignedAccess.owner_id == user_id)
        .filter(UserAssignedAccess.allow_notify)
        .all()
    )

    return [row.granted_to for row in user_granted_notify_to]


def filter_muted_users(user_id: int, granted_list: list, db: Session):
    users_muted = (
        db.query(UserRelationSettings)
        .filter(UserRelationSettings.regarding_user_id == user_id)
        .filter(UserRelationSettings.muted is True)
        .all()
    )

    muted_list = [row.user_id for row in users_muted]
    updated_list = []

    for id in granted_list:
        if id not in muted_list:
            updated_list.append(id)

    return updated_list
