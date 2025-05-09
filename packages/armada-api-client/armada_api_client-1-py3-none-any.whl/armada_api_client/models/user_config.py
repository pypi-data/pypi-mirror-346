from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.criteria_string import CriteriaString
    from ..models.ent_prop import EntProp


T = TypeVar("T", bound="UserConfig")


@_attrs_define
class UserConfig:
    """
    Attributes:
        user_id (int):
        tree_view_1 (list['EntProp']):
        tree_view_2 (list['EntProp']):
        tree_view_3 (list['EntProp']):
        tree_view_4 (list['EntProp']):
        load_tree_view_1_from_user (Union[None, Unset, str]):
        restriction_criterias (Union[None, Unset, list['CriteriaString']]):
        personnal_criterias (Union[None, Unset, list['CriteriaString']]):
        grid_view_settings (Union[None, Unset, str]):
        default_details_tab (Union[None, Unset, str]):
        default_connection_web_page (Union[None, Unset, str]):
    """

    user_id: int
    tree_view_1: list["EntProp"]
    tree_view_2: list["EntProp"]
    tree_view_3: list["EntProp"]
    tree_view_4: list["EntProp"]
    load_tree_view_1_from_user: Union[None, Unset, str] = UNSET
    restriction_criterias: Union[None, Unset, list["CriteriaString"]] = UNSET
    personnal_criterias: Union[None, Unset, list["CriteriaString"]] = UNSET
    grid_view_settings: Union[None, Unset, str] = UNSET
    default_details_tab: Union[None, Unset, str] = UNSET
    default_connection_web_page: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        user_id = self.user_id

        tree_view_1 = []
        for tree_view_1_item_data in self.tree_view_1:
            tree_view_1_item = tree_view_1_item_data.to_dict()
            tree_view_1.append(tree_view_1_item)

        tree_view_2 = []
        for tree_view_2_item_data in self.tree_view_2:
            tree_view_2_item = tree_view_2_item_data.to_dict()
            tree_view_2.append(tree_view_2_item)

        tree_view_3 = []
        for tree_view_3_item_data in self.tree_view_3:
            tree_view_3_item = tree_view_3_item_data.to_dict()
            tree_view_3.append(tree_view_3_item)

        tree_view_4 = []
        for tree_view_4_item_data in self.tree_view_4:
            tree_view_4_item = tree_view_4_item_data.to_dict()
            tree_view_4.append(tree_view_4_item)

        load_tree_view_1_from_user: Union[None, Unset, str]
        if isinstance(self.load_tree_view_1_from_user, Unset):
            load_tree_view_1_from_user = UNSET
        else:
            load_tree_view_1_from_user = self.load_tree_view_1_from_user

        restriction_criterias: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.restriction_criterias, Unset):
            restriction_criterias = UNSET
        elif isinstance(self.restriction_criterias, list):
            restriction_criterias = []
            for restriction_criterias_type_0_item_data in self.restriction_criterias:
                restriction_criterias_type_0_item = restriction_criterias_type_0_item_data.to_dict()
                restriction_criterias.append(restriction_criterias_type_0_item)

        else:
            restriction_criterias = self.restriction_criterias

        personnal_criterias: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.personnal_criterias, Unset):
            personnal_criterias = UNSET
        elif isinstance(self.personnal_criterias, list):
            personnal_criterias = []
            for personnal_criterias_type_0_item_data in self.personnal_criterias:
                personnal_criterias_type_0_item = personnal_criterias_type_0_item_data.to_dict()
                personnal_criterias.append(personnal_criterias_type_0_item)

        else:
            personnal_criterias = self.personnal_criterias

        grid_view_settings: Union[None, Unset, str]
        if isinstance(self.grid_view_settings, Unset):
            grid_view_settings = UNSET
        else:
            grid_view_settings = self.grid_view_settings

        default_details_tab: Union[None, Unset, str]
        if isinstance(self.default_details_tab, Unset):
            default_details_tab = UNSET
        else:
            default_details_tab = self.default_details_tab

        default_connection_web_page: Union[None, Unset, str]
        if isinstance(self.default_connection_web_page, Unset):
            default_connection_web_page = UNSET
        else:
            default_connection_web_page = self.default_connection_web_page

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "userId": user_id,
                "treeView1": tree_view_1,
                "treeView2": tree_view_2,
                "treeView3": tree_view_3,
                "treeView4": tree_view_4,
            }
        )
        if load_tree_view_1_from_user is not UNSET:
            field_dict["loadTreeView1FromUser"] = load_tree_view_1_from_user
        if restriction_criterias is not UNSET:
            field_dict["restrictionCriterias"] = restriction_criterias
        if personnal_criterias is not UNSET:
            field_dict["personnalCriterias"] = personnal_criterias
        if grid_view_settings is not UNSET:
            field_dict["gridViewSettings"] = grid_view_settings
        if default_details_tab is not UNSET:
            field_dict["defaultDetailsTab"] = default_details_tab
        if default_connection_web_page is not UNSET:
            field_dict["defaultConnectionWebPage"] = default_connection_web_page

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.criteria_string import CriteriaString
        from ..models.ent_prop import EntProp

        d = dict(src_dict)
        user_id = d.pop("userId")

        tree_view_1 = []
        _tree_view_1 = d.pop("treeView1")
        for tree_view_1_item_data in _tree_view_1:
            tree_view_1_item = EntProp.from_dict(tree_view_1_item_data)

            tree_view_1.append(tree_view_1_item)

        tree_view_2 = []
        _tree_view_2 = d.pop("treeView2")
        for tree_view_2_item_data in _tree_view_2:
            tree_view_2_item = EntProp.from_dict(tree_view_2_item_data)

            tree_view_2.append(tree_view_2_item)

        tree_view_3 = []
        _tree_view_3 = d.pop("treeView3")
        for tree_view_3_item_data in _tree_view_3:
            tree_view_3_item = EntProp.from_dict(tree_view_3_item_data)

            tree_view_3.append(tree_view_3_item)

        tree_view_4 = []
        _tree_view_4 = d.pop("treeView4")
        for tree_view_4_item_data in _tree_view_4:
            tree_view_4_item = EntProp.from_dict(tree_view_4_item_data)

            tree_view_4.append(tree_view_4_item)

        def _parse_load_tree_view_1_from_user(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        load_tree_view_1_from_user = _parse_load_tree_view_1_from_user(d.pop("loadTreeView1FromUser", UNSET))

        def _parse_restriction_criterias(data: object) -> Union[None, Unset, list["CriteriaString"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                restriction_criterias_type_0 = []
                _restriction_criterias_type_0 = data
                for restriction_criterias_type_0_item_data in _restriction_criterias_type_0:
                    restriction_criterias_type_0_item = CriteriaString.from_dict(restriction_criterias_type_0_item_data)

                    restriction_criterias_type_0.append(restriction_criterias_type_0_item)

                return restriction_criterias_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CriteriaString"]], data)

        restriction_criterias = _parse_restriction_criterias(d.pop("restrictionCriterias", UNSET))

        def _parse_personnal_criterias(data: object) -> Union[None, Unset, list["CriteriaString"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                personnal_criterias_type_0 = []
                _personnal_criterias_type_0 = data
                for personnal_criterias_type_0_item_data in _personnal_criterias_type_0:
                    personnal_criterias_type_0_item = CriteriaString.from_dict(personnal_criterias_type_0_item_data)

                    personnal_criterias_type_0.append(personnal_criterias_type_0_item)

                return personnal_criterias_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CriteriaString"]], data)

        personnal_criterias = _parse_personnal_criterias(d.pop("personnalCriterias", UNSET))

        def _parse_grid_view_settings(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        grid_view_settings = _parse_grid_view_settings(d.pop("gridViewSettings", UNSET))

        def _parse_default_details_tab(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_details_tab = _parse_default_details_tab(d.pop("defaultDetailsTab", UNSET))

        def _parse_default_connection_web_page(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_connection_web_page = _parse_default_connection_web_page(d.pop("defaultConnectionWebPage", UNSET))

        user_config = cls(
            user_id=user_id,
            tree_view_1=tree_view_1,
            tree_view_2=tree_view_2,
            tree_view_3=tree_view_3,
            tree_view_4=tree_view_4,
            load_tree_view_1_from_user=load_tree_view_1_from_user,
            restriction_criterias=restriction_criterias,
            personnal_criterias=personnal_criterias,
            grid_view_settings=grid_view_settings,
            default_details_tab=default_details_tab,
            default_connection_web_page=default_connection_web_page,
        )

        return user_config
