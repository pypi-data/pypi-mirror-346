from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="ParamModifyElementByNameForEquIds")


@_attrs_define
class ParamModifyElementByNameForEquIds:
    """
    Attributes:
        table_name (str):
        attribute_name (str):
        element_group (str):
        element_subgroup (str):
        element_name (str):
        new_value (str):
        equ_ids (Union[None, list[int]]):
    """

    table_name: str
    attribute_name: str
    element_group: str
    element_subgroup: str
    element_name: str
    new_value: str
    equ_ids: Union[None, list[int]]

    def to_dict(self) -> dict[str, Any]:
        table_name = self.table_name

        attribute_name = self.attribute_name

        element_group = self.element_group

        element_subgroup = self.element_subgroup

        element_name = self.element_name

        new_value = self.new_value

        equ_ids: Union[None, list[int]]
        if isinstance(self.equ_ids, list):
            equ_ids = self.equ_ids

        else:
            equ_ids = self.equ_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "tableName": table_name,
                "attributeName": attribute_name,
                "elementGroup": element_group,
                "elementSubgroup": element_subgroup,
                "elementName": element_name,
                "newValue": new_value,
                "equIds": equ_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        table_name = d.pop("tableName")

        attribute_name = d.pop("attributeName")

        element_group = d.pop("elementGroup")

        element_subgroup = d.pop("elementSubgroup")

        element_name = d.pop("elementName")

        new_value = d.pop("newValue")

        def _parse_equ_ids(data: object) -> Union[None, list[int]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                equ_ids_type_0 = cast(list[int], data)

                return equ_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[int]], data)

        equ_ids = _parse_equ_ids(d.pop("equIds"))

        param_modify_element_by_name_for_equ_ids = cls(
            table_name=table_name,
            attribute_name=attribute_name,
            element_group=element_group,
            element_subgroup=element_subgroup,
            element_name=element_name,
            new_value=new_value,
            equ_ids=equ_ids,
        )

        return param_modify_element_by_name_for_equ_ids
