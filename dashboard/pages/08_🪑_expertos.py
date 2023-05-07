from page_router import PageRouter, Route
from pages.expertos_pages.home import expertos_page

router = PageRouter(
    "expertos",
    Route(
        url="home",
        builder=expertos_page,
    ),
)

router.start()
