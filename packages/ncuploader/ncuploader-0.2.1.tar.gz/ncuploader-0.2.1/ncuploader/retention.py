# ncuploader/retention.py
"""
Retention policy implementation for NCUploader.
"""

import re
from datetime import datetime, timedelta, UTC
from typing import Dict, Any, Optional

from pydantic import BaseModel, Field, field_validator


class RetentionPolicy(BaseModel):
    """Retention policy configuration for uploaded files."""

    delete_after_upload: Optional[str] = Field(
        None,
        description="Time to retain files after upload. Format: '30d' (days), '24h' (hours), "
                    "'60min' (minutes), '3600s' (seconds), '4w' (weeks), '1y' (years). None means never delete."
    )

    @field_validator('delete_after_upload')
    @classmethod
    def validate_retention_format(cls, v):
        """Validate the retention time format."""
        if v is None:
            return v

        pattern = r'^(\d+)(d|h|min|s|w|y)$'
        match = re.match(pattern, v)

        if not match:
            valid_units = "d (days), h (hours), min (minutes), s (seconds), w (weeks), y (years)"
            raise ValueError(
                f"Invalid retention format. Use a number followed by one of: {valid_units}. "
                f"Examples: '30d', '24h', '60min', '3600s', '4w', '1y'"
            )

        return v

    def get_expiry_date(self, upload_time: datetime) -> Optional[datetime]:
        """
        Calculate the expiry date based on the retention policy.

        Args:
            upload_time: The time when the file was uploaded

        Returns:
            Expiry datetime or None if no expiry
        """
        if not self.delete_after_upload:
            return None

        pattern = r'^(\d+)(d|h|min|s|w|y)$'
        match = re.match(pattern, self.delete_after_upload)

        if not match:
            return None

        value, unit = match.groups()
        value = int(value)

        # Calculate timedelta based on the unit
        if unit == 'd':
            delta = timedelta(days=value)
        elif unit == 'h':
            delta = timedelta(hours=value)
        elif unit == 'min':
            delta = timedelta(minutes=value)
        elif unit == 's':
            delta = timedelta(seconds=value)
        elif unit == 'w':
            delta = timedelta(weeks=value)
        elif unit == 'y':
            # Approximate - using 365.25 days per year
            delta = timedelta(days=value * 365.25)
        else:
            return None

        return upload_time + delta

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RetentionPolicy':
        """Create from dictionary storage format."""
        return cls.model_validate(data)