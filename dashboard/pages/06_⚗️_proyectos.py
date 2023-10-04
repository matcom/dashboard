from page_router import PageRouter, Route
from pages.proyectos_pages.home import proyectos_page

router = PageRouter(
    "proyectos",
    Route(
        url="home",
        builder=proyectos_page,
    ),
)

router.start()