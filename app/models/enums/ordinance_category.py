from enum import Enum

class OrdinanceCategory(str, Enum):
  PUBLIC_SAFETY = "public_safety"
  ENVIRONMENT = "environment"
  BUSINESS_REGULATION = "business_regulation"
  TAXATION = "taxation"
  