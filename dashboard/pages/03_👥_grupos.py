from page_router import PageRouter, Route
from pages.grupos_pages.home import grupos_page

router = PageRouter(
    "grupos",
    Route(
        url="home",
        builder=grupos_page,
    ),
)

router.start()