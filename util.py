# lightRigGenerator/util/light_utils.py
import maya.cmds as cmds
import math

# helper: clear old rig
def clear_old_rig(name):
    grp = f"LR_{name}_grp"
    if cmds.objExists(grp):
        cmds.delete(grp)

# helper: color mood map
def mood_color(mood):
    table = {
        "Neutral": (1.0, 1.0, 1.0),
        "Cinematic": (1.0, 0.9, 0.8),
        "Soft": (0.9, 0.95, 1.0)
    }
    return table.get(mood, (1, 1, 1))

# === PRESET FUNCTIONS ===================================================

def create_three_point(intensity=1.0, mood="Neutral", exposure=0.0):
    clear_old_rig("3Point")
    grp = cmds.group(em=True, n="LR_3Point_grp")
    color = mood_color(mood)

    key = cmds.directionalLight(n="LR_key")
    fill = cmds.areaLight(n="LR_fill")
    rim = cmds.directionalLight(n="LR_rim")

    cmds.setAttr(key+".intensity", intensity*1.2)
    cmds.setAttr(fill+".intensity", intensity*0.8)
    cmds.setAttr(rim+".intensity", intensity*1.0)

    for l in [key, fill, rim]:
        cmds.setAttr(l+".color", *color, type="double3")

    cmds.xform(key, t=(5,5,5), ro=(-30,45,0))
    cmds.xform(fill, t=(-6,3,6), ro=(-20,-45,0))
    cmds.xform(rim, t=(-3,5,-5), ro=(-10,150,0))
    cmds.parent(key, fill, rim, grp)
    return grp


def create_studio_rig(intensity=1.0, mood="Neutral", exposure=0.0):
    clear_old_rig("Studio")
    grp = cmds.group(em=True, n="LR_Studio_grp")
    color = mood_color(mood)

    key = cmds.areaLight(n="LR_key")
    fill = cmds.areaLight(n="LR_fill")
    backdrop = cmds.areaLight(n="LR_backdrop")

    for l in [key, fill, backdrop]:
        cmds.setAttr(l+".color", *color, type="double3")

    cmds.setAttr(key+".intensity", intensity*1.1)
    cmds.setAttr(fill+".intensity", intensity*0.8)
    cmds.setAttr(backdrop+".intensity", intensity*0.5)

    cmds.xform(key, t=(5,6,6), ro=(-20,40,0))
    cmds.xform(fill, t=(-5,4,6), ro=(-20,-40,0))
    cmds.xform(backdrop, t=(0,2,-8), ro=(0,0,0))
    cmds.parent(key, fill, backdrop, grp)
    return grp


def create_dramatic(intensity=1.0, mood="Cinematic", exposure=0.0):
    clear_old_rig("Dramatic")
    grp = cmds.group(em=True, n="LR_Dramatic_grp")
    color = mood_color(mood)

    key = cmds.spotLight(n="LR_key")
    fill = cmds.areaLight(n="LR_fill")

    cmds.setAttr(key+".intensity", intensity*2.0)
    cmds.setAttr(fill+".intensity", intensity*0.5)
    cmds.setAttr(key+".color", *color, type="double3")
    cmds.setAttr(fill+".color", *color, type="double3")

    cmds.xform(key, t=(4,6,4), ro=(-45,45,0))
    cmds.xform(fill, t=(-3,3,6), ro=(-15,-40,0))
    cmds.parent(key, fill, grp)
    return grp


def create_hdr_dome(intensity=1.0, mood="Neutral", exposure=0.0):
    clear_old_rig("HDRDome")
    grp = cmds.group(em=True, n="LR_HDRDome_grp")
    dome = cmds.createNode("aiSkyDomeLight", n="LR_dome")
    cmds.setAttr(dome+".intensity", intensity)
    cmds.parent(dome, grp)
    return grp


def create_sunset(intensity=1.0, mood="Cinematic", exposure=0.0):
    clear_old_rig("Sunset")
    grp = cmds.group(em=True, n="LR_Sunset_grp")

    key = cmds.directionalLight(n="LR_key")
    fill = cmds.areaLight(n="LR_fill")
    color = (1.0, 0.75, 0.5)

    for l in [key, fill]:
        cmds.setAttr(l+".color", *color, type="double3")
    cmds.setAttr(key+".intensity", intensity*1.3)
    cmds.setAttr(fill+".intensity", intensity*0.6)
    cmds.xform(key, t=(10,8,5), ro=(-25,45,0))
    cmds.xform(fill, t=(-4,3,6), ro=(-15,-45,0))
    cmds.parent(key, fill, grp)
    return grp


def create_moonlight(intensity=1.0, mood="Soft", exposure=0.0):
    clear_old_rig("Moonlight")
    grp = cmds.group(em=True, n="LR_Moonlight_grp")

    key = cmds.directionalLight(n="LR_key")
    rim = cmds.directionalLight(n="LR_rim")
    color = (0.5, 0.6, 1.0)

    cmds.setAttr(key+".color", *color, type="double3")
    cmds.setAttr(rim+".color", *color, type="double3")
    cmds.setAttr(key+".intensity", intensity*0.8)
    cmds.setAttr(rim+".intensity", intensity*1.2)
    cmds.xform(key, t=(4,8,4), ro=(-30,45,0))
    cmds.xform(rim, t=(-5,5,-6), ro=(-20,150,0))
    cmds.parent(key, rim, grp)
    return grp


def create_product(intensity=1.0, mood="Neutral", exposure=0.0):
    clear_old_rig("Product")
    grp = cmds.group(em=True, n="LR_Product_grp")
    color = mood_color(mood)

    key = cmds.areaLight(n="LR_key")
    fill = cmds.areaLight(n="LR_fill")
    top = cmds.areaLight(n="LR_top")

    for l in [key, fill, top]:
        cmds.setAttr(l+".color", *color, type="double3")
        cmds.setAttr(l+".intensity", intensity)

    cmds.xform(key, t=(6,6,6), ro=(-30,40,0))
    cmds.xform(fill, t=(-6,3,6), ro=(-20,-40,0))
    cmds.xform(top, t=(0,10,0), ro=(-90,0,0))
    cmds.parent(key, fill, top, grp)
    return grp


def create_horror(intensity=1.0, mood="Cinematic", exposure=0.0):
    clear_old_rig("Horror")
    grp = cmds.group(em=True, n="LR_Horror_grp")

    under = cmds.spotLight(n="LR_under")
    rim = cmds.directionalLight(n="LR_rim")

    cmds.setAttr(under+".color", 0.8, 0.2, 0.2, type="double3")
    cmds.setAttr(rim+".color", 0.2, 0.2, 0.8, type="double3")
    cmds.setAttr(under+".intensity", intensity*2.0)
    cmds.setAttr(rim+".intensity", intensity*0.7)
    cmds.xform(under, t=(0,-3,3), ro=(60,0,0))
    cmds.xform(rim, t=(0,5,-5), ro=(-10,180,0))
    cmds.parent(under, rim, grp)
    return grp


def create_silhouette(intensity=1.0, mood="Neutral", exposure=0.0):
    clear_old_rig("Silhouette")
    grp = cmds.group(em=True, n="LR_Silhouette_grp")

    rim = cmds.directionalLight(n="LR_rim")
    cmds.setAttr(rim+".color", 1, 1, 1, type="double3")
    cmds.setAttr(rim+".intensity", intensity*1.5)
    cmds.xform(rim, t=(0,5,-10), ro=(0,180,0))
    cmds.parent(rim, grp)
    return grp


def create_stylized(intensity=1.0, mood="Soft", exposure=0.0):
    clear_old_rig("Stylized")
    grp = cmds.group(em=True, n="LR_Stylized_grp")

    key = cmds.directionalLight(n="LR_key")
    fill = cmds.areaLight(n="LR_fill")
    color_key = (1.0, 0.5, 0.5)
    color_fill = (0.5, 0.7, 1.0)

    cmds.setAttr(key+".color", *color_key, type="double3")
    cmds.setAttr(fill+".color", *color_fill, type="double3")
    cmds.setAttr(key+".intensity", intensity*1.2)
    cmds.setAttr(fill+".intensity", intensity)
    cmds.xform(key, t=(5,5,5), ro=(-30,40,0))
    cmds.xform(fill, t=(-5,4,5), ro=(-20,-40,0))
    cmds.parent(key, fill, grp)
    return grp
