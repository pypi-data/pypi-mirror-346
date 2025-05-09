from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.element_modification_request import ElementModificationRequest


T = TypeVar("T", bound="ElementsModificationRequest")


@_attrs_define
class ElementsModificationRequest:
    """
    Attributes:
        changes (list['ElementModificationRequest']):
        request_to_save_on_site (bool):
    """

    changes: list["ElementModificationRequest"]
    request_to_save_on_site: bool

    def to_dict(self) -> dict[str, Any]:
        changes = []
        for changes_item_data in self.changes:
            changes_item = changes_item_data.to_dict()
            changes.append(changes_item)

        request_to_save_on_site = self.request_to_save_on_site

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "changes": changes,
                "requestToSaveOnSite": request_to_save_on_site,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.element_modification_request import ElementModificationRequest

        d = dict(src_dict)
        changes = []
        _changes = d.pop("changes")
        for changes_item_data in _changes:
            changes_item = ElementModificationRequest.from_dict(changes_item_data)

            changes.append(changes_item)

        request_to_save_on_site = d.pop("requestToSaveOnSite")

        elements_modification_request = cls(
            changes=changes,
            request_to_save_on_site=request_to_save_on_site,
        )

        return elements_modification_request
