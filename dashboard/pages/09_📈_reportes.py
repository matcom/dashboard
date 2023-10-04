from page_router import PageRouter, Route
from pages.reportes_pages.home import reportes_page

router = PageRouter(
    "reportes",
    Route(
        url="home",
        builder=reportes_page,
    ),
)

router.start()