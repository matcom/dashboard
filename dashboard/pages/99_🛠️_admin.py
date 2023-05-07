from page_router import PageRouter, Route
from pages.admin_pages.home import admin_page

router = PageRouter(
    "admin",
    Route(
        url="home",
        builder=admin_page,
    ),
)

router.start()
