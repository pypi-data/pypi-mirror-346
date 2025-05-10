from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.post_v1_desktop_id_bash_action_response_400_status import PostV1DesktopIdBashActionResponse400Status

T = TypeVar("T", bound="PostV1DesktopIdBashActionResponse400")


@_attrs_define
class PostV1DesktopIdBashActionResponse400:
    """
    Attributes:
        status (PostV1DesktopIdBashActionResponse400Status):  Example: error.
        error (str): Error message detailing what went wrong Example: Instance not found or unauthorized.
    """

    status: PostV1DesktopIdBashActionResponse400Status
    error: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = PostV1DesktopIdBashActionResponse400Status(d.pop("status"))

        error = d.pop("error")

        post_v1_desktop_id_bash_action_response_400 = cls(
            status=status,
            error=error,
        )

        post_v1_desktop_id_bash_action_response_400.additional_properties = d
        return post_v1_desktop_id_bash_action_response_400

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
