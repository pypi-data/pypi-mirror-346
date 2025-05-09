import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="ArmadaLicenseInfo")


@_attrs_define
class ArmadaLicenseInfo:
    """
    Attributes:
        company (str):
        monitoring_limit (int):
        site_location_limit (int):
        expiration_date (datetime.datetime):
        modules (list[str]):
    """

    company: str
    monitoring_limit: int
    site_location_limit: int
    expiration_date: datetime.datetime
    modules: list[str]

    def to_dict(self) -> dict[str, Any]:
        company = self.company

        monitoring_limit = self.monitoring_limit

        site_location_limit = self.site_location_limit

        expiration_date = self.expiration_date.isoformat()

        modules = self.modules

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "company": company,
                "monitoringLimit": monitoring_limit,
                "siteLocationLimit": site_location_limit,
                "expirationDate": expiration_date,
                "modules": modules,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        company = d.pop("company")

        monitoring_limit = d.pop("monitoringLimit")

        site_location_limit = d.pop("siteLocationLimit")

        expiration_date = isoparse(d.pop("expirationDate"))

        modules = cast(list[str], d.pop("modules"))

        armada_license_info = cls(
            company=company,
            monitoring_limit=monitoring_limit,
            site_location_limit=site_location_limit,
            expiration_date=expiration_date,
            modules=modules,
        )

        return armada_license_info
