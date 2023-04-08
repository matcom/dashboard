from __future__ import annotations

from typing import Callable, Dict, Iterator, List, Optional

import streamlit as st


class Route:
    def __init__(
        self,
        url: str,
        builder: Callable,
        name: Optional[str] = None,
        subroutes: Optional[List[Route]] = None,
    ):
        self.url = url
        self.builder = builder
        self.parent: Optional[Route] = None
        self.page_name = url if name is None else name

        subroutes = subroutes or []
        for route in subroutes:
            route.parent = self
            route.url = f"{url}/{route.url}"
        self.subroutes = subroutes

    def all_routes(self) -> Iterator[Route]:
        yield self
        for subroute in self.subroutes:
            for route in subroute.all_routes():
                yield route

    def is_subroute(self, other: Route):
        if self == other:
            return True
        return False if self.parent is None else self.parent.is_subroute(other)


class PageRouter:
    def __init__(self, name: str, main_route: Route):
        self.root_name = name
        self.main_route = main_route
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

    def go_named(self, page_name: str, **params):
        route = self.routes_by_name.get(page_name, None)
        if not route:
            raise Exception(f"There is no page named: '{page_name}'")
        self.go(route.url, **params)

    def go_back(self, **params):
        self.go(self.current_page.parent.url, **params)

    def page_header(self, title: str = None, show_back_button: bool = True):
        st.title(title or self.current_page.page_name)
        if show_back_button and st.button("⬅️ Atrás"):
            self.go_back()

    def start(self):
        if st.session_state.get("root_page", None) != self.root_name:
            st.session_state["root_page"] = self.root_name
            st.experimental_set_query_params()

        query = st.experimental_get_query_params()
        if "page" not in query:
            query.clear()
            query["page"] = [self.current_page.url]

        if query["page"][0] not in self.routes.keys():
            query.clear()
            query["page"] = [self.main_route.url]

        st.experimental_set_query_params(**query)
        url = st.experimental_get_query_params()["page"][0]

        route = self.routes.get(url, None)
        if not route:
            raise Exception(f"Invalid route '{url}'")
        self.current_page = route
        query = {k: (v[0] if v and len(v) == 1 else v) for k, v in query.items()}

        self.current_page.builder(self, **query)
