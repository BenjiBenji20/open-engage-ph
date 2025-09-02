from enum import Enum

class OrdinanceCategory(str, Enum):
  PUBLIC_SAFETY = "public_safety"
  ENVIRONMENT = "environment"
  BUSINESS_REGULATION = "business_regulation"
  TAXATION = "taxation"
  

class OrdinanceVote(str, Enum):
  SUPPORT = "support"
  NEED_ENHANCEMENT = "need_enhancement"
  NEUTRAL = "neutral"
  NEEDS_REVISION = "needs_revision"
  OPPOSE = "oppose"
  