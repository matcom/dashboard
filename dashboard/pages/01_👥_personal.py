from page_router import PageRouter, Route
from pages.personal_pages.home import personal_page

router = PageRouter(
    "personal",
    Route(
        url="home",
        builder=personal_page,
    ),
)

router.start()
