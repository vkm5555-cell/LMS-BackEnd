from pydantic import BaseModel
from datetime import date

class UserDetailsBase(BaseModel):
    profile_image: str | None = None
    profile_image_thumb: str | None = None
    dob: date | None = None
    father_name: str | None = None
    mother_name: str | None = None
    gender: str | None = None
    marital_status: str | None = None

    permanent_address_line1: str | None = None
    permanent_address_line2: str | None = None
    permanent_city: str | None = None
    permanent_state: str | None = None
    permanent_country: str | None = None
    permanent_pincode: str | None = None

    current_address_line1: str | None = None
    current_address_line2: str | None = None
    current_city: str | None = None
    current_state: str | None = None
    current_country: str | None = None
    current_pincode: str | None = None

    bio: str | None = None
    facebook: str | None = None
    x_com: str | None = None
    linkedin: str | None = None
    instagram: str | None = None


class UserDetailsCreate(UserDetailsBase):
    pass

class UserDetailsOut(UserDetailsBase):
    id: int
    user_id: int | None

    class Config:
        from_attributes = True