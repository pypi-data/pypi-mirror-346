from typing import *
from fasthtml.common import *
from .datagrid import DataGrid, CompareButton
from .right_panel import RightPanel, reset_scalar_session


# Choose a row in the datagrid
def click_row_handler(session, run_id: int):
    reset_scalar_session(session)
    if "datagrid" not in session:
        session["datagrid"] = dict()
    session["datagrid"]["selected-rows"] = [run_id]
    # Return the image
    return DataGrid(session), CompareButton(session, swap=True), RightPanel(session)