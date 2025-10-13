import panel as pn
from panel_splitjs import Split

pn.extension()

Split(objects=['Foo', 'Bar'], height=500, width=500).servable()
Split(objects=['Foo', 'Bar'], height=500, width=500, orientation="vertical").servable()
