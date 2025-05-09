from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_date_and_user import AuditDateAndUser


T = TypeVar("T", bound="FileInformation")


@_attrs_define
class FileInformation:
    """
    Attributes:
        id (str):
        file_id (int):
        storage_type (int):
        name (str):
        extension (str):
        display_name (str):
        type_ (str):
        size (int):
        version (str):
        path (str):
        content_id (int):
        revision (int):
        comment (str):
        audit (Union['AuditDateAndUser', None, Unset]):
    """

    id: str
    file_id: int
    storage_type: int
    name: str
    extension: str
    display_name: str
    type_: str
    size: int
    version: str
    path: str
    content_id: int
    revision: int
    comment: str
    audit: Union["AuditDateAndUser", None, Unset] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.audit_date_and_user import AuditDateAndUser

        id = self.id

        file_id = self.file_id

        storage_type = self.storage_type

        name = self.name

        extension = self.extension

        display_name = self.display_name

        type_ = self.type_

        size = self.size

        version = self.version

        path = self.path

        content_id = self.content_id

        revision = self.revision

        comment = self.comment

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
                "id": id,
                "fileId": file_id,
                "storageType": storage_type,
                "name": name,
                "extension": extension,
                "displayName": display_name,
                "type": type_,
                "size": size,
                "version": version,
                "path": path,
                "contentId": content_id,
                "revision": revision,
                "comment": comment,
            }
        )
        if audit is not UNSET:
            field_dict["audit"] = audit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.audit_date_and_user import AuditDateAndUser

        d = dict(src_dict)
        id = d.pop("id")

        file_id = d.pop("fileId")

        storage_type = d.pop("storageType")

        name = d.pop("name")

        extension = d.pop("extension")

        display_name = d.pop("displayName")

        type_ = d.pop("type")

        size = d.pop("size")

        version = d.pop("version")

        path = d.pop("path")

        content_id = d.pop("contentId")

        revision = d.pop("revision")

        comment = d.pop("comment")

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

        file_information = cls(
            id=id,
            file_id=file_id,
            storage_type=storage_type,
            name=name,
            extension=extension,
            display_name=display_name,
            type_=type_,
            size=size,
            version=version,
            path=path,
            content_id=content_id,
            revision=revision,
            comment=comment,
            audit=audit,
        )

        return file_information
