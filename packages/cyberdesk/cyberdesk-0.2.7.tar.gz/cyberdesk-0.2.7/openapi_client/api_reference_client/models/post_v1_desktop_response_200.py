from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.post_v1_desktop_response_200_status import PostV1DesktopResponse200Status

T = TypeVar("T", bound="PostV1DesktopResponse200")


@_attrs_define
class PostV1DesktopResponse200:
    """
    Attributes:
        id (str): Unique identifier for the desktop instance Example: desktop_12345.
        status (PostV1DesktopResponse200Status): Initial status of the desktop instance after creation request Example:
            pending.
    """

    id: str
    status: PostV1DesktopResponse200Status
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        status = PostV1DesktopResponse200Status(d.pop("status"))

        post_v1_desktop_response_200 = cls(
            id=id,
            status=status,
        )

        post_v1_desktop_response_200.additional_properties = d
        return post_v1_desktop_response_200

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
