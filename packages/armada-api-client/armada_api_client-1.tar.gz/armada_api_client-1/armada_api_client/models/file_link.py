from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.criteria_string import CriteriaString


T = TypeVar("T", bound="FileLink")


@_attrs_define
class FileLink:
    """
    Attributes:
        id (str):
        link_id (int):
        file_id (int):
        criterias (list['CriteriaString']):
    """

    id: str
    link_id: int
    file_id: int
    criterias: list["CriteriaString"]

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        link_id = self.link_id

        file_id = self.file_id

        criterias = []
        for criterias_item_data in self.criterias:
            criterias_item = criterias_item_data.to_dict()
            criterias.append(criterias_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "linkId": link_id,
                "fileId": file_id,
                "criterias": criterias,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.criteria_string import CriteriaString

        d = dict(src_dict)
        id = d.pop("id")

        link_id = d.pop("linkId")

        file_id = d.pop("fileId")

        criterias = []
        _criterias = d.pop("criterias")
        for criterias_item_data in _criterias:
            criterias_item = CriteriaString.from_dict(criterias_item_data)

            criterias.append(criterias_item)

        file_link = cls(
            id=id,
            link_id=link_id,
            file_id=file_id,
            criterias=criterias,
        )

        return file_link
