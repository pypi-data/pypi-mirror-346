from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_date_and_user import AuditDateAndUser


T = TypeVar("T", bound="JobHttpGetConfig")


@_attrs_define
class JobHttpGetConfig:
    """
    Attributes:
        config_id (int):
        path_and_query (str):
        refresh_period_in_minutes (int):
        enabled (int):
        processor (Union[None, str]):
        audit (Union['AuditDateAndUser', None, Unset]):
    """

    config_id: int
    path_and_query: str
    refresh_period_in_minutes: int
    enabled: int
    processor: Union[None, str]
    audit: Union["AuditDateAndUser", None, Unset] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.audit_date_and_user import AuditDateAndUser

        config_id = self.config_id

        path_and_query = self.path_and_query

        refresh_period_in_minutes = self.refresh_period_in_minutes

        enabled = self.enabled

        processor: Union[None, str]
        processor = self.processor

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
                "configId": config_id,
                "pathAndQuery": path_and_query,
                "refreshPeriodInMinutes": refresh_period_in_minutes,
                "enabled": enabled,
                "processor": processor,
            }
        )
        if audit is not UNSET:
            field_dict["audit"] = audit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.audit_date_and_user import AuditDateAndUser

        d = dict(src_dict)
        config_id = d.pop("configId")

        path_and_query = d.pop("pathAndQuery")

        refresh_period_in_minutes = d.pop("refreshPeriodInMinutes")

        enabled = d.pop("enabled")

        def _parse_processor(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        processor = _parse_processor(d.pop("processor"))

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

        job_http_get_config = cls(
            config_id=config_id,
            path_and_query=path_and_query,
            refresh_period_in_minutes=refresh_period_in_minutes,
            enabled=enabled,
            processor=processor,
            audit=audit,
        )

        return job_http_get_config
