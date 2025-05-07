from .handlers import click_row_handler
from .datagrid import build_datagrid_endpoints
from .right_panel import build_right_panel_routes
from .main_page import MainPage

def build_main_page_endpoints(rt):
    rt("/click_row")(click_row_handler)
    rt("/reset")(reset)
    rt("/fullscreen")(fullscreen)
    build_datagrid_endpoints(rt)
    build_right_panel_routes(rt)

def reset(session):
    if "show_hidden" not in session:
        session["show_hidden"] = False
    session["datagrid"] = dict()
    return MainPage(session, swap=True)

def fullscreen(session, full: bool):
    return MainPage(session, swap=True, fullscreen=full)