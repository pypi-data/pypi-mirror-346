from typing import List, Optional  # Import typing hints for lists and optional values
from pydantic import BaseModel, model_validator  # Import Pydantic for data validation


# Certificate model
class Certificate(BaseModel):
    name: str = "certificate"  # Certificate identifier with default value
    url: Optional[str] = None  # URL where certificate can be downloaded 
    file: Optional[str] = None  # Local file path to certificate 
    threshold: Optional[int] = 30  # Days threshold for expiry warning (default 30)

    @model_validator(mode="after")
    def url_xor_file(self):
        # Ensure that either url OR file is set, but NOT both
        if self.url and self.file:
            raise ValueError("❌ Either url OR file must be set")
        return self


# Model  that holds the certificates to check
class Config(BaseModel):
    certificates: List[Certificate]  # List of certificate configurations


# Model for individual certificate check results
class Check(BaseModel):
    name: str = "certificate"  # Name of the checked certificate
    days_to_expiry: int  # Number of days until certificate expires
    threshold_reached: bool  # Flag indicating if expiry threshold is reached


# Model for the complete check report
class Report(BaseModel):
    checks: List[Check]  # List of all certificate check results
