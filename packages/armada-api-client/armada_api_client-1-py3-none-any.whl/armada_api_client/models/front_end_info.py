from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.modules_options import ModulesOptions


T = TypeVar("T", bound="FrontEndInfo")


@_attrs_define
class FrontEndInfo:
    """
    Attributes:
        is_alive (Union[Unset, bool]):
        tenant (Union[None, Unset, str]):
        theme (Union[None, Unset, str]):
        supplier_website (Union[None, Unset, str]):
        default_page (Union[None, Unset, str]):
        application_name (Union[None, Unset, str]):
        welcome_message (Union[None, Unset, str]):
        specific_message (Union[None, Unset, str]):
        map_tiles_url_template (Union[None, Unset, str]):
        modules (Union['ModulesOptions', None, Unset]):
    """

    is_alive: Union[Unset, bool] = UNSET
    tenant: Union[None, Unset, str] = UNSET
    theme: Union[None, Unset, str] = UNSET
    supplier_website: Union[None, Unset, str] = UNSET
    default_page: Union[None, Unset, str] = UNSET
    application_name: Union[None, Unset, str] = UNSET
    welcome_message: Union[None, Unset, str] = UNSET
    specific_message: Union[None, Unset, str] = UNSET
    map_tiles_url_template: Union[None, Unset, str] = UNSET
    modules: Union["ModulesOptions", None, Unset] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.modules_options import ModulesOptions

        is_alive = self.is_alive

        tenant: Union[None, Unset, str]
        if isinstance(self.tenant, Unset):
            tenant = UNSET
        else:
            tenant = self.tenant

        theme: Union[None, Unset, str]
        if isinstance(self.theme, Unset):
            theme = UNSET
        else:
            theme = self.theme

        supplier_website: Union[None, Unset, str]
        if isinstance(self.supplier_website, Unset):
            supplier_website = UNSET
        else:
            supplier_website = self.supplier_website

        default_page: Union[None, Unset, str]
        if isinstance(self.default_page, Unset):
            default_page = UNSET
        else:
            default_page = self.default_page

        application_name: Union[None, Unset, str]
        if isinstance(self.application_name, Unset):
            application_name = UNSET
        else:
            application_name = self.application_name

        welcome_message: Union[None, Unset, str]
        if isinstance(self.welcome_message, Unset):
            welcome_message = UNSET
        else:
            welcome_message = self.welcome_message

        specific_message: Union[None, Unset, str]
        if isinstance(self.specific_message, Unset):
            specific_message = UNSET
        else:
            specific_message = self.specific_message

        map_tiles_url_template: Union[None, Unset, str]
        if isinstance(self.map_tiles_url_template, Unset):
            map_tiles_url_template = UNSET
        else:
            map_tiles_url_template = self.map_tiles_url_template

        modules: Union[None, Unset, dict[str, Any]]
        if isinstance(self.modules, Unset):
            modules = UNSET
        elif isinstance(self.modules, ModulesOptions):
            modules = self.modules.to_dict()
        else:
            modules = self.modules

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if is_alive is not UNSET:
            field_dict["isAlive"] = is_alive
        if tenant is not UNSET:
            field_dict["tenant"] = tenant
        if theme is not UNSET:
            field_dict["theme"] = theme
        if supplier_website is not UNSET:
            field_dict["supplierWebsite"] = supplier_website
        if default_page is not UNSET:
            field_dict["defaultPage"] = default_page
        if application_name is not UNSET:
            field_dict["applicationName"] = application_name
        if welcome_message is not UNSET:
            field_dict["welcomeMessage"] = welcome_message
        if specific_message is not UNSET:
            field_dict["specificMessage"] = specific_message
        if map_tiles_url_template is not UNSET:
            field_dict["mapTilesUrlTemplate"] = map_tiles_url_template
        if modules is not UNSET:
            field_dict["modules"] = modules

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.modules_options import ModulesOptions

        d = dict(src_dict)
        is_alive = d.pop("isAlive", UNSET)

        def _parse_tenant(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tenant = _parse_tenant(d.pop("tenant", UNSET))

        def _parse_theme(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        theme = _parse_theme(d.pop("theme", UNSET))

        def _parse_supplier_website(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        supplier_website = _parse_supplier_website(d.pop("supplierWebsite", UNSET))

        def _parse_default_page(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_page = _parse_default_page(d.pop("defaultPage", UNSET))

        def _parse_application_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        application_name = _parse_application_name(d.pop("applicationName", UNSET))

        def _parse_welcome_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        welcome_message = _parse_welcome_message(d.pop("welcomeMessage", UNSET))

        def _parse_specific_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        specific_message = _parse_specific_message(d.pop("specificMessage", UNSET))

        def _parse_map_tiles_url_template(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        map_tiles_url_template = _parse_map_tiles_url_template(d.pop("mapTilesUrlTemplate", UNSET))

        def _parse_modules(data: object) -> Union["ModulesOptions", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                modules_type_1 = ModulesOptions.from_dict(data)

                return modules_type_1
            except:  # noqa: E722
                pass
            return cast(Union["ModulesOptions", None, Unset], data)

        modules = _parse_modules(d.pop("modules", UNSET))

        front_end_info = cls(
            is_alive=is_alive,
            tenant=tenant,
            theme=theme,
            supplier_website=supplier_website,
            default_page=default_page,
            application_name=application_name,
            welcome_message=welcome_message,
            specific_message=specific_message,
            map_tiles_url_template=map_tiles_url_template,
            modules=modules,
        )

        return front_end_info
