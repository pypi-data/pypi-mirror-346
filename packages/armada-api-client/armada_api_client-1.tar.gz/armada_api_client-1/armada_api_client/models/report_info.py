from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_date_and_user import AuditDateAndUser
    from ..models.criteria_string import CriteriaString
    from ..models.table_info_selector import TableInfoSelector


T = TypeVar("T", bound="ReportInfo")


@_attrs_define
class ReportInfo:
    """
    Attributes:
        table_info_selectors (list['TableInfoSelector']):
        type_ (str):
        id (str):
        report_id (int):
        name (str):
        criterias (Union[None, Unset, list['CriteriaString']]):
        equ_ids (Union[None, Unset, list[int]]):
        columns_to_remove (Union[None, Unset, list[str]]):
        custom_query (Union[None, Unset, str]):
        culture_abbreviation (Union[None, Unset, str]):
        audit (Union['AuditDateAndUser', None, Unset]):
    """

    table_info_selectors: list["TableInfoSelector"]
    type_: str
    id: str
    report_id: int
    name: str
    criterias: Union[None, Unset, list["CriteriaString"]] = UNSET
    equ_ids: Union[None, Unset, list[int]] = UNSET
    columns_to_remove: Union[None, Unset, list[str]] = UNSET
    custom_query: Union[None, Unset, str] = UNSET
    culture_abbreviation: Union[None, Unset, str] = UNSET
    audit: Union["AuditDateAndUser", None, Unset] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.audit_date_and_user import AuditDateAndUser

        table_info_selectors = []
        for table_info_selectors_item_data in self.table_info_selectors:
            table_info_selectors_item = table_info_selectors_item_data.to_dict()
            table_info_selectors.append(table_info_selectors_item)

        type_ = self.type_

        id = self.id

        report_id = self.report_id

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

        audit: Union[None, Unset, dict[str, Any]]
        if isinstance(self.audit, Unset):
            audit = UNSET
        elif isinstance(self.audit, AuditDateAndUser):
            audit = self.audit.to_dict()
        else:
            audit = self.audit

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "tableInfoSelectors": table_info_selectors,
                "type": type_,
                "id": id,
                "reportId": report_id,
                "name": name,
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
        if audit is not UNSET:
            field_dict["audit"] = audit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.audit_date_and_user import AuditDateAndUser
        from ..models.criteria_string import CriteriaString
        from ..models.table_info_selector import TableInfoSelector

        d = dict(src_dict)
        table_info_selectors = []
        _table_info_selectors = d.pop("tableInfoSelectors")
        for table_info_selectors_item_data in _table_info_selectors:
            table_info_selectors_item = TableInfoSelector.from_dict(table_info_selectors_item_data)

            table_info_selectors.append(table_info_selectors_item)

        type_ = d.pop("type")

        id = d.pop("id")

        report_id = d.pop("reportId")

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

        def _parse_audit(data: object) -> Union["AuditDateAndUser", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                audit_type_1 = AuditDateAndUser.from_dict(data)

                return audit_type_1
            except:  # noqa: E722
                pass
            return cast(Union["AuditDateAndUser", None, Unset], data)

        audit = _parse_audit(d.pop("audit", UNSET))

        report_info = cls(
            table_info_selectors=table_info_selectors,
            type_=type_,
            id=id,
            report_id=report_id,
            name=name,
            criterias=criterias,
            equ_ids=equ_ids,
            columns_to_remove=columns_to_remove,
            custom_query=custom_query,
            culture_abbreviation=culture_abbreviation,
            audit=audit,
        )

        return report_info
