from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.data_record_consolidation_info import DataRecordConsolidationInfo
    from ..models.data_records_selection_info import DataRecordsSelectionInfo


T = TypeVar("T", bound="DataRecordsConsolidationParameters")


@_attrs_define
class DataRecordsConsolidationParameters:
    """
    Attributes:
        selection_info (DataRecordsSelectionInfo):
        consolidation_info (DataRecordConsolidationInfo):
    """

    selection_info: "DataRecordsSelectionInfo"
    consolidation_info: "DataRecordConsolidationInfo"

    def to_dict(self) -> dict[str, Any]:
        selection_info = self.selection_info.to_dict()

        consolidation_info = self.consolidation_info.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "selectionInfo": selection_info,
                "consolidationInfo": consolidation_info,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data_record_consolidation_info import DataRecordConsolidationInfo
        from ..models.data_records_selection_info import DataRecordsSelectionInfo

        d = dict(src_dict)
        selection_info = DataRecordsSelectionInfo.from_dict(d.pop("selectionInfo"))

        consolidation_info = DataRecordConsolidationInfo.from_dict(d.pop("consolidationInfo"))

        data_records_consolidation_parameters = cls(
            selection_info=selection_info,
            consolidation_info=consolidation_info,
        )

        return data_records_consolidation_parameters
