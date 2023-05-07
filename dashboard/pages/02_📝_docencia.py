from page_router import PageRouter, Route
from pages.docencia_pages.home import docencia_page

router = PageRouter(
    "docencia",
    Route(
        url="home",
        builder=docencia_page,
    ),
)

router.start()
