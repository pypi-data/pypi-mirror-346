from PyThinkDesign import Application
from PyThinkDesign import Geo3d

app = Application.GetActiveApplication()
doc=app.GetActiveDocument()

# get creators
curveCreator=doc.GetCurveCreator()
profileCreator = doc.GetProfileCreator()

# add lines
p1 = Geo3d.Point(0,0,0)
p2 = Geo3d.Point(1,0,0)
p3 = Geo3d.Point(1,1,0)
p4 = Geo3d.Point(0,1,0)
line1 = curveCreator.AddLine(p1,p2)
line2 = curveCreator.AddLine(p2,p3)
line3 = curveCreator.AddLine(p3,p4)
line4 = curveCreator.AddLine(p4,p1)

lines = [line1.ToSmartId(),line2.ToSmartId(),line3.ToSmartId(),line4.ToSmartId()]
spProfile =profileCreator.AddProfile(lines, False)


