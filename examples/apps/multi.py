from panel_splitjs import MultiSplit
from panel_material_ui import Paper

paper_opts = dict(elevation=3, margin=10, sizing_mode="stretch_both")

MultiSplit(
    objects=[
        Paper("Foo", **paper_opts),
        Paper("Bar", **paper_opts),
        Paper("Baz", **paper_opts),
        Paper("Qux", **paper_opts),
        Paper("Quux", **paper_opts),
    ],
    sizes=(20, 30, 20, 10, 20),
    min_size=100,
    sizing_mode="stretch_width",
    height=400
).servable()
