from panel_splitjs import MultiSplit
from panel_material_ui import Button, Column, Paper, Row

paper_opts = dict(elevation=3, margin=10, sizing_mode="stretch_both")

add = Button(label="Add item", on_click=lambda _: ms.append(Paper("Added", **paper_opts)))
insert = Button(label="Insert item", on_click=lambda _: ms.insert(2, Paper("Inserted", **paper_opts)))

ms = MultiSplit(
    Paper("Foo", **paper_opts),
    Paper("Bar", **paper_opts),
    Paper("Baz", **paper_opts),
    Paper("Qux", **paper_opts),
    Paper("Quux", **paper_opts),
    sizes=(20, 30, 20, 10, 20),
    min_size=100,
    sizing_mode="stretch_width",
    height=400
)

Column(Row(add, insert), ms).servable()
