from typing import *
from fasthtml.common import *
from .datagrid import DataGrid, CompareButton
from .right_panel import RightPanel

def MainPage(session, swap: bool = False):
    return Div(
        Div(
            DataGrid(session, wrapincontainer=True),
            CompareButton(session),
            cls="table-container"
        ),
        RightPanel(session),
        cls='container',
        id="container",
        hx_swap_oob="true" if swap else None
    )