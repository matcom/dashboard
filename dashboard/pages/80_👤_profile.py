from page_router import PageRouter, Route
from pages.profile_pages.home import profile_page

router = PageRouter(
    "publications",
    Route(
        url="home",
        builder=profile_page,
    ),
)

router.start()
