from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="EquipmentSetupTemplateConfig")


@_attrs_define
class EquipmentSetupTemplateConfig:
    """
    Attributes:
        id (str):
        template_config_id (int):
        template_id (int):
        entity (str):
        property_ (str):
        group (str):
        sub_group (str):
        name (str):
        requested_value (str):
    """

    id: str
    template_config_id: int
    template_id: int
    entity: str
    property_: str
    group: str
    sub_group: str
    name: str
    requested_value: str

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        template_config_id = self.template_config_id

        template_id = self.template_id

        entity = self.entity

        property_ = self.property_

        group = self.group

        sub_group = self.sub_group

        name = self.name

        requested_value = self.requested_value

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "templateConfigId": template_config_id,
                "templateId": template_id,
                "entity": entity,
                "property": property_,
                "group": group,
                "subGroup": sub_group,
                "name": name,
                "requestedValue": requested_value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        template_config_id = d.pop("templateConfigId")

        template_id = d.pop("templateId")

        entity = d.pop("entity")

        property_ = d.pop("property")

        group = d.pop("group")

        sub_group = d.pop("subGroup")

        name = d.pop("name")

        requested_value = d.pop("requestedValue")

        equipment_setup_template_config = cls(
            id=id,
            template_config_id=template_config_id,
            template_id=template_id,
            entity=entity,
            property_=property_,
            group=group,
            sub_group=sub_group,
            name=name,
            requested_value=requested_value,
        )

        return equipment_setup_template_config
