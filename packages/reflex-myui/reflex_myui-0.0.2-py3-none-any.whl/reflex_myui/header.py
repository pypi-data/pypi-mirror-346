import reflex as rx
from .state import DrawerState


def _logo_icon(logo_src: str) -> rx.Component:
    return rx.image(
        src=logo_src,
        width="22px",
        height="22px",
        border_radius="100%",
        object_fit="fit",
        border=f"1px solid {rx.color('slate', 12)}",
        display=["none", "none", "none", "none", "flex", "flex"],
    )

def _logo_type(logo_type: str) -> rx.Component:
    return rx.link(
        rx.heading(
            logo_type.upper(),
            font_size="0.9em",
            font_weight="800",
            cursor="pointer",
        ),
        href="/",
        text_decoration="none",
        # on_click=SiteRoutingState.toggle_page_change(data)
    )

def identity(logo_src: str, logo_type: str) -> rx.Component:
    return rx.hstack(
        _logo_icon(logo_src),
        _logo_type(logo_type),
        align="center",
    )

def _link_item(link_item) -> rx.Component:
    return rx.link(
        link_item['name'],
        href=link_item['href'],
        text_decoration="none",
        underline="none",
    )

def _menu_item(menu_item: dict) -> rx.Component:
    return  rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.text(
                    menu_item['name'],
                ),
                rx.icon("chevron-down"),
                weight="medium",
                variant="ghost",
            ),
        ),
        rx.menu.content(
            *[rx.menu.item(_link_item(item)) for item in menu_item['href']],
        ),
    )

def nav_item(nav_item: dict) -> rx.Component:
    if isinstance(nav_item['href'], str):
        return _link_item(nav_item)
    elif isinstance(nav_item['href'], list):
        return _menu_item(nav_item)
    else:
        raise ValueError("Invalid href type")

def navbar(nav_list: list) -> rx.Component:
    return rx.hstack(
        *[nav_item(item) for item in nav_list],
        align="center",
        display=["none", "none", "none", "none", "flex", "flex"],
        spacing="5",
    )

def __header_icon(component: rx.Component) -> rx.Component:
    return rx.badge(
        component,
        # color_scheme="gray",
        variant="soft",
        width="21px",
        height="21px",
        display="flex",
        align_items="center",
        justify_content="center",
        background="none",
    )

def _header_color_mode() -> rx.Component:
    return __header_icon(
        rx.el.button(
            rx.color_mode_cond(
                light=rx.icon(
                    "moon",
                    size=14,
                    # color=rx.color("slate", 12),
                ),
                dark=rx.icon(
                    "sun",
                    size=14,
                    # color=rx.color("slate", 12),
                ),
            ),
            on_click=rx.toggle_color_mode,
        ),
    )

def _header_drawer_button() -> rx.Component:
    return __header_icon(
        rx.el.button(
            rx.icon(
                tag="align-right", 
                size=15
            ),
            on_click=DrawerState.toggle_drawer,
            size="1",
            variant="ghost",
            # color_scheme="gray",
            cursor="pointer",
            display=["flex", "flex", "flex", "flex", "none", "none"],
        )
    )

def _link_sidebar(nav_item: dict) -> rx.Component:
    return rx.link(
        rx.hstack(
            # rx.icon(icon),
            rx.text(nav_item['name'], size="4"),
            width="100%",
            padding_x="1rem",
            padding_y="0.75rem",
            align="center",
            # style={
            #     "_hover": {
            #         "bg": rx.color("accent", 4),
            #         "color": rx.color("accent", 11),
            #     },
            #     "border-radius": "0.5em",
            # },
        ),
        href=nav_item['href'],
        underline="none",
        weight="medium",
        width="100%",
    )

def _menu_sidebar(menu_item: dict) -> rx.Component:
    return rx.accordion.root(
        rx.accordion.item(
            header=rx.text(menu_item['name'], size="4", weight="medium"),
            content=rx.vstack(
                *[_link_sidebar(item) for item in menu_item['href']],
                spacing="1",
                width="100%",

            ),
            # weight="medium",
        ),
        collapsible=True,
        variant="ghost",
    )

def sidebar_item(nav_item: dict) -> rx.Component:
    if isinstance(nav_item['href'], str):
        return _link_sidebar(nav_item)
    elif isinstance(nav_item['href'], list):
        return _menu_sidebar(nav_item)
    else:
        raise ValueError("Invalid href type")

def sidebar(logo_src, logo_type, nav_links) -> rx.Component:
    return rx.box(
            rx.drawer.root(
                rx.drawer.trigger(
                    __header_icon(
                        rx.el.button(
                            rx.icon(
                                tag="align-right", 
                                size=15
                            ),
                            on_click=DrawerState.toggle_drawer,
                            size="1",
                            variant="ghost",
                            # color_scheme="gray",
                            cursor="pointer",
                            display=["flex", "flex", "flex", "flex", "none", "none"],
                        ),
                    ),
                ),
                rx.drawer.overlay(z_index="1000"),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.vstack(
                            rx.box(
                                rx.drawer.close(
                                    __header_icon(
                                        rx.el.button(
                                            rx.icon(
                                                tag="x", 
                                                size=20
                                            ),
                                            on_click=DrawerState.toggle_drawer,
                                            size="1",
                                            variant="ghost",
                                            # color_scheme="gray",
                                            cursor="pointer",
                                        ),
                                    ),
                                ),
                                align='right',
                                width="100%",
                            ),
                            rx.vstack(
                                rx.link(
                                    rx.heading(
                                        logo_type.upper(),
                                        font_size="2em",
                                        font_weight="800",
                                        cursor="pointer",
                                    ),
                                    href="/",
                                    text_decoration="none",
                                    padding="1em",
                                ),
                                *[sidebar_item(item) for item in nav_links],
                                spacing="1",
                                width="100%",
                            ),
                            spacing="5",
                            width="100%",
                        ),
                        top="auto",
                        right="auto",
                        height="100%",
                        width="20em",
                        padding="1.5em",
                        background=rx.color("sky", 3),
                    ),
                    width="100%",
                ),
                open=DrawerState.is_open,
                direction="left",
            ),
            padding="1em",
    )

def utility(logo_src: str, logo_type: str, nav_links: dict) -> rx.Component:
    return rx.hstack(
        _header_color_mode(),
        align="center",
    )

def header(
        logo_src: str,
        logo_type: str,
        navigation_list: list,
    ) -> rx.Component:
    """
    Header component for the app.

    This component includes a logo, a navigation bar, and utility items.

    Args:
        logo_src (str): The source URL for the logo image.
        logo_type (str): The type of the logo, displayed as text.
        navigation_list (list): A list of dictionaries representing the navigation items.
            Each dictionary should have a 'name' and 'href' key. The 'href' can be a string or a list of dictionaries. If it's a list, each dictionary in the list should also have 'name' and 'href' keys.
            
            Example:
                [
                    {"name": "link_1", "href": "/"},
                    {"name": "link_2", "href": "/"},
                    {"name": "menu_1", "href": [{"name": "link_1", "href": "/"}, {"name": "link_2", "href": "/"}]}
                ]

    Returns:
        rx.Component: The header component.
    """
    return rx.hstack(
        rx.hstack(
            sidebar(logo_src, logo_type, navigation_list),
            identity(logo_src, logo_type),
            rx.spacer(),
            navbar(navigation_list),
            rx.spacer(),
            utility(logo_src, logo_type, navigation_list),
            width="100%",
            max_width="80em",
            height="50px",
            align="center",
            # justify="between",
        ),
        align="center",
        background=rx.color("sky", 3),
        justify="center",
        padding="0rem 1rem 0rem 1rem",
        position="fixed",
        top="0",
        width="100%",
        z_index="1000",
    )





