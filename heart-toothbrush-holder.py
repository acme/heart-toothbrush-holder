import cadquery as cq
import math
import numpy as np

# The thickness of the shell
thickness = 1.67

# The height of the vase
height = 100

face_x_center = (math.sqrt(30*30 + 30*30))/2
face_y_center = height/2

# Create a heart shape
heart = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(30, 30)
    .threePointArc((15, 60), (0, 45))
    .threePointArc((-15, 60), (-30, 30))
    .close()
)

# Center over the origin
centered_heart = (heart.translate(-heart.val().CenterOfBoundBox()))

# Extrude the heart
vase = (
    centered_heart
    .extrude(height)
)

# Fillet the front pointy bit
vase = (
    vase.edges(cq.NearestToPointSelector((0, 0, 50)))
    .fillet(2+thickness)
)

# Fillet the back pointy bit
vase = (
    vase.edges(cq.NearestToPointSelector((0, 60, 50)))
    .fillet(2+thickness)
)

# Chamfer the bottom
vase = (
    vase.faces("<Z")
    .chamfer(thickness)
)

# Create the shell
vase = (
    vase.faces(">Z")
    .shell(-thickness)
)

# Chamfer the top
vase = (
    vase.edges(cq.NearestToPointSelector((10, 20, 100)))
    .chamfer(thickness-0.001)
)

# Pixel heart points
points = [
    (0, -2),
    (1, -1),
    (2, 0),
    (3, 1),
    (3, 2),
    (2, 3),
    (1, 3),

    (0, 2),

    (-1, -1),
    (-2, 0),
    (-3, 1),
    (-3, 2),
    (-2, 3),
    (-1, 3),
]

# Add pixel hearts to the sides
scale_sides = 5

vase = (vase
        .faces(cq.NearestToPointSelector((-20, 20, 50)))
        .workplane()
        .center(-face_x_center-4, face_y_center)
        .pushPoints(np.multiply(points, scale_sides))
        .rect(scale_sides-thickness, scale_sides-thickness)
        .extrude("next", combine="cut")
        )

vase = (vase
        .faces(cq.NearestToPointSelector((20, 20, 50)))
        .workplane()
        .center(face_x_center+4, 0)
        .pushPoints(np.multiply(points, scale_sides))
        .rect(scale_sides-thickness, scale_sides-thickness)
        .extrude("next", combine="cut")
        )

# Add pixel hearts to the bottom
scale_bottom = 7

vase = (vase
        .faces("<Z")
        .workplane()
        .center(-17.8, -7)
        .pushPoints(np.multiply(points, (scale_bottom, -scale_bottom)))
        .rect(scale_bottom-thickness, scale_bottom-thickness)
        .extrude("next", combine="cut")
        )

# Show the object
show_object(vase, name="heart")
# debug(vase.faces(">Z").edges().first())
# debug(vase.edges(cq.NearestToPointSelector((20, 20, 100))))

# Export the object
cq.exporters.export(vase, 'heart-toothbrush-holder.3mf')
cq.exporters.export(vase, 'heart-toothbrush-holder.step')
cq.exporters.export(vase, 'heart-toothbrush-holder.stl')
