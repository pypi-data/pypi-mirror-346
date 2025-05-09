from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.criteria_string import CriteriaString
    from ..models.table_info_selector import TableInfoSelector


T = TypeVar("T", bound="ReportParameters")


@_attrs_define
class ReportParameters:
    """
    Attributes:
        table_info_selectors (list['TableInfoSelector']):
        type_ (str):
        criterias (Union[None, Unset, list['CriteriaString']]):
        equ_ids (Union[None, Unset, list[int]]):
        columns_to_remove (Union[None, Unset, list[str]]):
        custom_query (Union[None, Unset, str]):
        culture_abbreviation (Union[None, Unset, str]):
    """

    table_info_selectors: list["TableInfoSelector"]
    type_: str
    criterias: Union[None, Unset, list["CriteriaString"]] = UNSET
    equ_ids: Union[None, Unset, list[int]] = UNSET
    columns_to_remove: Union[None, Unset, list[str]] = UNSET
    custom_query: Union[None, Unset, str] = UNSET
    culture_abbreviation: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        table_info_selectors = []
        for table_info_selectors_item_data in self.table_info_selectors:
            table_info_selectors_item = table_info_selectors_item_data.to_dict()
            table_info_selectors.append(table_info_selectors_item)

        type_ = self.type_

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

        columns_to_remove: Union[None, Unset, list[str]]
        if isinstance(self.columns_to_remove, Unset):
            columns_to_remove = UNSET
        elif isinstance(self.columns_to_remove, list):
            columns_to_remove = self.columns_to_remove

        else:
            columns_to_remove = self.columns_to_remove

        custom_query: Union[None, Unset, str]
        if isinstance(self.custom_query, Unset):
            custom_query = UNSET
        else:
            custom_query = self.custom_query

        culture_abbreviation: Union[None, Unset, str]
        if isinstance(self.culture_abbreviation, Unset):
            culture_abbreviation = UNSET
        else:
            culture_abbreviation = self.culture_abbreviation

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "tableInfoSelectors": table_info_selectors,
                "type": type_,
            }
        )
        if criterias is not UNSET:
            field_dict["criterias"] = criterias
        if equ_ids is not UNSET:
            field_dict["equIds"] = equ_ids
        if columns_to_remove is not UNSET:
            field_dict["columnsToRemove"] = columns_to_remove
        if custom_query is not UNSET:
            field_dict["customQuery"] = custom_query
        if culture_abbreviation is not UNSET:
            field_dict["cultureAbbreviation"] = culture_abbreviation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.criteria_string import CriteriaString
        from ..models.table_info_selector import TableInfoSelector

        d = dict(src_dict)
        table_info_selectors = []
        _table_info_selectors = d.pop("tableInfoSelectors")
        for table_info_selectors_item_data in _table_info_selectors:
            table_info_selectors_item = TableInfoSelector.from_dict(table_info_selectors_item_data)

            table_info_selectors.append(table_info_selectors_item)

        type_ = d.pop("type")

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

        def _parse_columns_to_remove(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                columns_to_remove_type_0 = cast(list[str], data)

                return columns_to_remove_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        columns_to_remove = _parse_columns_to_remove(d.pop("columnsToRemove", UNSET))

        def _parse_custom_query(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        custom_query = _parse_custom_query(d.pop("customQuery", UNSET))

        def _parse_culture_abbreviation(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        culture_abbreviation = _parse_culture_abbreviation(d.pop("cultureAbbreviation", UNSET))

        report_parameters = cls(
            table_info_selectors=table_info_selectors,
            type_=type_,
            criterias=criterias,
            equ_ids=equ_ids,
            columns_to_remove=columns_to_remove,
            custom_query=custom_query,
            culture_abbreviation=culture_abbreviation,
        )

        return report_parameters
