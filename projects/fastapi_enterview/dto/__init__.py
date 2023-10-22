from pydantic import BaseModel


class UserDto(BaseModel):
    id: int
    name: str
    email: str


class ItemDto(BaseModel):
    id: int
    name: str
    price: float


class OrderDto(BaseModel):
    id: int
    user_id: int
    item_id: int
    quantity: int


class UserItemDto(BaseModel):
    user_id: int
    item_id: int