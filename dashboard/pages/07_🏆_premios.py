from page_router import PageRouter, Route
from pages.premios_pages.home import premios_page

router = PageRouter(
    "premios",
    Route(
        url="home",
        builder=premios_page,
    ),
)

router.start()