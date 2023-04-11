import abc
from typing import Optional

import auth
import streamlit as st
from page_router import PageRouter, Route
from pages.publications_pages.books_and_chapters import books_and_chapters_page
from pages.publications_pages.home import home_page
from pages.publications_pages.journals import journals_page
from pages.publications_pages.papers import papers_page
from pages.publications_pages.presentations import presentations_page


class ControlledSectionModel: ...


class Page(abc.ABC):
    def __init__(self, url: str, section_model: ControlledSectionModel):
        self.url = url
        self.section_model: Optional[ControlledSectionModel] = section_model

        # This is modified when the router is composed
        self.full_url = url
    
    @property
    def user_can_open(self):
        if auth.in_admin_session or self.section_model is None:
            return True

    @abc.abstractmethod
    def build(self, router: PageRouter, **params):
        pass


# TODO: Only build router if it is not stored in session
router = PageRouter(
    "publications",
    Route(
        url="home",
        builder=home_page,
        name="Publicaciones",
        subroutes=[
            Route(
                url="papers",
                name="Artículos",
                builder=papers_page,
            ),
            Route(
                url="journals",
                name="Revistas",
                builder=journals_page,
            ),
            Route(
                url="presentations",
                name="Presentaciones",
                builder=presentations_page,
            ),
            Route(
                url="books-and-chapters",
                name="Libros y artículos",
                builder=books_and_chapters_page,
            ),
        ],
    ),
)

router.start()
