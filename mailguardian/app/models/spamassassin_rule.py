from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.spamassassin_rule import (
    SpamAssassinRule as SpamAssassinRuleSchema,
)


class SpamAssassinRule(SpamAssassinRuleSchema, BaseModel, table=True):
    __tablename__ = 'spamassassin_rules'
