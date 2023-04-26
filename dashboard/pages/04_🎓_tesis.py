from page_router import PageRouter, Route
from pages.tesis_pages.home import tesis_page

router = PageRouter(
    "tesis",
    Route(
        url="home",
        builder=tesis_page,
    ),
)

router.start()