from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.criteria_string import CriteriaString
    from ..models.equipment_setup_template_config import EquipmentSetupTemplateConfig


T = TypeVar("T", bound="EquipmentSetupTemplate")


@_attrs_define
class EquipmentSetupTemplate:
    """
    Attributes:
        id (str):
        template_id (int):
        name (str):
        criterias (Union[None, Unset, list['CriteriaString']]):
        equ_ids (Union[None, Unset, list[int]]):
        configs (Union[None, Unset, list['EquipmentSetupTemplateConfig']]):
    """

    id: str
    template_id: int
    name: str
    criterias: Union[None, Unset, list["CriteriaString"]] = UNSET
    equ_ids: Union[None, Unset, list[int]] = UNSET
    configs: Union[None, Unset, list["EquipmentSetupTemplateConfig"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        template_id = self.template_id

        name = self.name

        criterias: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.criterias, Unset):
            criterias = UNSET
        elif isinstance(self.criterias, list):
            criterias = []
            for criterias_type_0_item_data in self.criterias:
                criterias_type_0_item = criterias_type_0_item_data.to_dict()
                criterias.append(criterias_type_0_item)

        else:
            criterias = self.criterias

        equ_ids: Union[None, Unset, list[int]]
        if isinstance(self.equ_ids, Unset):
            equ_ids = UNSET
        elif isinstance(self.equ_ids, list):
            equ_ids = self.equ_ids

        else:
            equ_ids = self.equ_ids

        configs: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.configs, Unset):
            configs = UNSET
        elif isinstance(self.configs, list):
            configs = []
            for configs_type_0_item_data in self.configs:
                configs_type_0_item = configs_type_0_item_data.to_dict()
                configs.append(configs_type_0_item)

        else:
            configs = self.configs

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "templateId": template_id,
                "name": name,
            }
        )
        if criterias is not UNSET:
            field_dict["criterias"] = criterias
        if equ_ids is not UNSET:
            field_dict["equIds"] = equ_ids
        if configs is not UNSET:
            field_dict["configs"] = configs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.criteria_string import CriteriaString
        from ..models.equipment_setup_template_config import EquipmentSetupTemplateConfig

        d = dict(src_dict)
        id = d.pop("id")

        template_id = d.pop("templateId")

        name = d.pop("name")

        def _parse_criterias(data: object) -> Union[None, Unset, list["CriteriaString"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                criterias_type_0 = []
                _criterias_type_0 = data
                for criterias_type_0_item_data in _criterias_type_0:
                    criterias_type_0_item = CriteriaString.from_dict(criterias_type_0_item_data)

                    criterias_type_0.append(criterias_type_0_item)

                return criterias_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CriteriaString"]], data)

        criterias = _parse_criterias(d.pop("criterias", UNSET))

        def _parse_equ_ids(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                equ_ids_type_0 = cast(list[int], data)

                return equ_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        equ_ids = _parse_equ_ids(d.pop("equIds", UNSET))

        def _parse_configs(data: object) -> Union[None, Unset, list["EquipmentSetupTemplateConfig"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                configs_type_0 = []
                _configs_type_0 = data
                for configs_type_0_item_data in _configs_type_0:
                    configs_type_0_item = EquipmentSetupTemplateConfig.from_dict(configs_type_0_item_data)

                    configs_type_0.append(configs_type_0_item)

                return configs_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["EquipmentSetupTemplateConfig"]], data)

        configs = _parse_configs(d.pop("configs", UNSET))

        equipment_setup_template = cls(
            id=id,
            template_id=template_id,
            name=name,
            criterias=criterias,
            equ_ids=equ_ids,
            configs=configs,
        )

        return equipment_setup_template
