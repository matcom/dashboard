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
