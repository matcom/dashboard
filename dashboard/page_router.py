from __future__ import annotations

from typing import Callable, Dict, Iterator, List, Optional

import auth
import streamlit as st
from models.data_models.person_model import Person
from models.permission import (
    ALL_PERMISSIONS,
    PERMISSIONS,
    PERMISSIONS_BY_NAME,
    READ,
    Permission,
)


def admin_subpage(router: PageRouter, **params):
    st.set_page_config(page_title="MatCom Dashboard - Permisos", layout="wide")
    router.page_header("Permisos")
    section = f"{router.root_name}/{router.current_page.parent.url}"
    st.write(f"#### Página:")
    st.write(section)
    st.write("#### Permisos por defecto")
    default_perm = router.current_page.parent.default_perms
    st.write(
        ", ".join([PERMISSIONS[perm] for perm in Permission.from_number(default_perm)])
    )

    permissions = Permission.find(section=section)
    if permissions:
        st.write("#### Permisos adicionales")
        for i, perm in enumerate(permissions):
            with st.expander(f"{perm.person.name}"):
                selected = st.multiselect(
                    "Permisos",
                    list(PERMISSIONS.values()),
                    [PERMISSIONS[p] for p in Permission.from_number(perm.permission)],
                    key=f"mult_{i}",
                )
                new_perm = Permission.from_list(
                    [PERMISSIONS_BY_NAME[p] for p in selected]
                )

                if st.button(
                    "Guardar cambios",
                    disabled=new_perm == perm.permission,
                    key=f"save_{i}",
                ):
                    perm.permission = new_perm
                    perm.save()
                    st.experimental_rerun()

                if st.button("Eliminar", key=f"delete_{i}"):
                    perm.delete()
                    st.experimental_rerun()

    st.write("---")
    st.write("#### Añadir permiso adicional")

    person = st.selectbox("Persona", Person.all())
    selected = st.multiselect(
        "Permisos",
        list(PERMISSIONS.values()),
        default=[PERMISSIONS[p] for p in Permission.from_number(default_perm)],
    )
    if selected:
        permission = Permission.from_list([PERMISSIONS_BY_NAME[p] for p in selected])

    if st.button("Añadir", disabled=not selected):
        new_perm = Permission(person=person, section=section, permission=permission)
        new_perm.save()
        st.experimental_rerun()


class Route:
    def __init__(
        self,
        url: str,
        builder: Callable,
        name: Optional[str] = None,
        default_perms: int = READ,
        redirect: Optional[Callable] = None,
        subroutes: Optional[List[Route]] = None,
        _has_admin: bool = True,
    ):
        self.url = url
        self.root = url
        self.builder = builder
        self.redirect = redirect
        self.parent: Optional[Route] = None
        self.page_name = url if name is None else name
        self.default_perms = default_perms

        subroutes = subroutes or []
        if _has_admin:
            subroutes.append(
                Route(
                    url="admin",
                    builder=admin_subpage,
                    default_perms=ALL_PERMISSIONS,
                    _has_admin=False,
                )
            )
        for subroute in subroutes:
            subroute.parent = self
        self.subroutes = subroutes

    def _build_url(self, root: str, current_url: str = "") -> str:
        self.root = root
        sep = "/" if current_url else ""
        self.url = f"{current_url}{sep}{self.url}"
        for sub in self.subroutes:
            sub._build_url(root, self.url)

    def all_routes(self) -> Iterator[Route]:
        yield self
        for subroute in self.subroutes:
            for route in subroute.all_routes():
                yield route

    def is_subroute(self, other: Route):
        if self == other:
            return True
        return False if self.parent is None else self.parent.is_subroute(other)

    def user_permission(self, user: Person) -> int:
        if auth.in_admin_session():
            return ALL_PERMISSIONS

        permissions = Permission.find(
            person=str(user.uuid),
            section=f"{self.root}/{self.url}",
        )
        if not permissions:
            return self.default_perms
        return permissions[0].permission


class PageRouter:
    def __init__(self, name: str, main_route: Route):
        self.root_name = name
        self.main_route = main_route
        self.main_route._build_url(self.root_name)

        self.current_page = main_route
        self.routes: Dict[str, Route] = {}
        self.routes_by_name: Dict[str, Route] = {}
        for route in main_route.all_routes():
            self.routes[route.url] = route
            if route.page_name:
                self.routes_by_name[route.page_name] = route

    def go(self, url, **params):
        route = self.routes.get(url, None)
        if not route:
            raise Exception(f"Invalid route '{url}'")

        st.experimental_set_query_params(page=url, **params)
        st.experimental_rerun()

    def go_named(self, page: str, **params):
        route = self.routes_by_name.get(page, None)
        if not route:
            raise Exception(f"There is no page named: '{page}'")
        self.go(route.url, **params)

    def go_back(self, **params):
        self.go(self.current_page.parent.url, **params)

    def page_header(self, title: str = None, show_back_button: bool = True):
        st.title(title or self.current_page.page_name)

        if (
            self.user_is_subadmin
            and not self.current_page.url.endswith("/admin")
            and st.button("Administrar permisos")
        ):
            self.go(self.current_page.url + "/admin")

        if (
            show_back_button
            and self.current_page.parent != None
            and st.button("⬅️ Atrás")
        ):
            self.go_back()

    def _not_found_page(self, url):
        st.title("Esta página no existe")

    def _access_error_page(self, url):
        st.title("No tienes permiso para acceder a esta página")

    @property
    def user_can_write(self) -> bool:
        if auth.is_user_logged():
            permission = self.current_page.user_permission(auth.current_user_model())
            if Permission.has_write_perm(permission):
                return True
        return False

    @property
    def user_is_subadmin(self) -> bool:
        if auth.is_user_logged():
            permission = self.current_page.user_permission(auth.current_user_model())
            if Permission.has_admin_perm(permission):
                return True
        return False

    def start(self):
        # To detect change of base page
        current_root = st.session_state.get("root_page", None)
        if current_root is not None:
            if current_root != self.root_name:
                st.session_state["root_page"] = self.root_name
                st.experimental_set_query_params()
        else:
            st.session_state["root_page"] = self.root_name

        query = st.experimental_get_query_params()
        if "page" not in query:
            query.clear()
            query["page"] = [self.current_page.url]

        if query["page"][0] not in self.routes.keys():
            query.clear()
            query["page"] = [self.main_route.url]

        st.experimental_set_query_params(**query)
        url = st.experimental_get_query_params()["page"][0]

        route = self.routes[url]

        # Check permission
        if auth.is_user_logged():
            permission = route.user_permission(auth.current_user_model())
            if not Permission.has_read_perm(permission):
                self._access_error_page(url)
                return
        elif not Permission.has_read_perm(route.default_perms):
            self._access_error_page(url)
            return

        if route.redirect is not None:
            new_url = route.redirect(**query)
            if new_url is not None:
                del query["page"]
                self.go(new_url, **query)
                return

        self.current_page = route
        query = {k: (v[0] if v and len(v) == 1 else v) for k, v in query.items()}
        self.current_page.builder(self, **query)
