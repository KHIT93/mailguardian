from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.spamassassin_rule_description import (
    SpamAssassinRuleDescription as SpamAssassinRuleDescriptionSchema,
)


class SpamAssassinRuleDescription(SpamAssassinRuleDescriptionSchema, BaseModel, table=True):
    __tablename__ = 'spamassassin_rule_descriptions'
