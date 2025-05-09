from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, Unset

T = TypeVar("T", bound="FilesAddWithUploadBody")


@_attrs_define
class FilesAddWithUploadBody:
    """
    Attributes:
        file (File):
        comment (Union[Unset, str]):
        display_name (Union[Unset, str]):
    """

    file: File
    comment: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file = self.file.to_tuple()

        comment = self.comment

        display_name = self.display_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "File": file,
            }
        )
        if comment is not UNSET:
            field_dict["Comment"] = comment
        if display_name is not UNSET:
            field_dict["DisplayName"] = display_name

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        file = self.file.to_tuple()

        comment = self.comment if isinstance(self.comment, Unset) else (None, str(self.comment).encode(), "text/plain")

        display_name = (
            self.display_name
            if isinstance(self.display_name, Unset)
            else (None, str(self.display_name).encode(), "text/plain")
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "File": file,
            }
        )
        if comment is not UNSET:
            field_dict["Comment"] = comment
        if display_name is not UNSET:
            field_dict["DisplayName"] = display_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file = File(payload=BytesIO(d.pop("File")))

        comment = d.pop("Comment", UNSET)

        display_name = d.pop("DisplayName", UNSET)

        files_add_with_upload_body = cls(
            file=file,
            comment=comment,
            display_name=display_name,
        )

        files_add_with_upload_body.additional_properties = d
        return files_add_with_upload_body

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
