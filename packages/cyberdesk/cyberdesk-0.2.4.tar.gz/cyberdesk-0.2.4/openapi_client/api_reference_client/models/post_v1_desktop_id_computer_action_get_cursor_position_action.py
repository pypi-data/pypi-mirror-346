from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.post_v1_desktop_id_computer_action_get_cursor_position_action_type import (
    PostV1DesktopIdComputerActionGetCursorPositionActionType,
)

T = TypeVar("T", bound="PostV1DesktopIdComputerActionGetCursorPositionAction")


@_attrs_define
class PostV1DesktopIdComputerActionGetCursorPositionAction:
    """
    Attributes:
        type_ (PostV1DesktopIdComputerActionGetCursorPositionActionType): Get the current mouse cursor position Example:
            get_cursor_position.
    """

    type_: PostV1DesktopIdComputerActionGetCursorPositionActionType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = PostV1DesktopIdComputerActionGetCursorPositionActionType(d.pop("type"))

        post_v1_desktop_id_computer_action_get_cursor_position_action = cls(
            type_=type_,
        )

        post_v1_desktop_id_computer_action_get_cursor_position_action.additional_properties = d
        return post_v1_desktop_id_computer_action_get_cursor_position_action

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
