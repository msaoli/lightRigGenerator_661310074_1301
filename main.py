try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance
except:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import os

from lightRigGenerator import util
import maya.cmds as cmds


#allStyleSheet
QSS = """
QDialog {
    background: qlineargradient(x1:0 y1:0, x2:0 y2:1, stop:0 #EDECEB, stop:1 #EDEDDD);
    border-radius: 19px;
    padding: 12px;
    font-family: HYWenHei-85W;
    color: #F5F3EB;
}
QGroupBox {
    border: 3px solid rgba(0,0,0,0.06);
    border-radius: 15px;
    margin-top: 17px;
    padding: 20px;
    font-family: HYWenHei-85W;
    background: rgba(255,255,255,0.6);
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 19px;
    font-family: HYWenHei-85W;
    color: #786536;
    font-weight: 700;
}
QLabel#titleLabel {
    font-size: 16pt;
    font-weight: 700;
    padding: 5px;
    font-family: HYWenHei-85W;
    color: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #B8B195, stop:1 #B8B195);
}
QPushButton {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #B8B49C, stop:1 #898CC9);
    border: 1px solid rgba(0,0,0,0.08);
    
    padding: 10px 15px;
    border-radius: 10px;
    font-family: HYWenHei-85W;
    min-height: 32px;
    font-weight: 600;
}
QPushButton#generateBtn {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #898ACC, stop:1 #A7C4C0);
    border: 1px solid #8F886D;
    padding: 8px 14px;
    color: #0a4f9fv;
}
QPushButton#generateBtn:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #706950, stop:1 #C9BC77);
}
QpushButton#generateBtn:pressed {
    background-color: #44589C;
}
QPushButton#resetBtn {
    background: transparent;
    border: 1px solid #8F886D;
    padding: 8px 14px;
    color: #4a5568;
}
QPushButton#resetBtn:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #706950, stop:1 #C9BC77);
}
QpushButton#resetBtn:pressed {
    background-color: #44589C;
}
QLabel#preview {
    border: 2px dashed rgba(0,0,0,0.06);
    min-width: 180px;
    min-height: 180px;
    border-radius: 8px;
    font-family: HYWenHei-85W;
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #0F0C40, stop:1 #59548F);
}
.small {
    color: #6b7280;
    font-size: 4pt;
    font-family: HYWenHei-85W;
}
"""

#Main
class LightRigUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Light Rig Generator")
        self.setMinimumWidth(600)
        self.setMaximumWidth(800)

        self.setStyleSheet(QSS)

        self.preview_dir = "C:/Users/DELL/OneDrive/Documents/maya/2025/scripts/lightRigGenerator/resources/LightRigPreview"
        self.preview_images = {

            "3-Point Lighting": os.path.join(self.preview_dir, "3point.png"),
            "Studio Portrait": os.path.join(self.preview_dir, "studio.png"),
            "Dramatic": os.path.join(self.preview_dir, "dramatic.png"),
            "HDR Dome": os.path.join(self.preview_dir, "hdr.png"),
            "Sunset": os.path.join(self.preview_dir, "sunset.png"),
            "Moonlight": os.path.join(self.preview_dir, "moon.png"),

        }

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        headerLayout = QtWidgets.QHBoxLayout()
        self.titleLabel = QtWidgets.QLabel("✦ ⊹࣪˖ Light Rig Generator ⊹࣪˖ ✦")
        self.titleLabel.setObjectName("titleLabel")
        headerLayout.addWidget(self.titleLabel)
        headerLayout.addStretch()
        self.mainLayout.addLayout(headerLayout)

        contentLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(contentLayout)

        leftCol = QtWidgets.QVBoxLayout()

        self.grpPresets = QtWidgets.QGroupBox("Preset & Mood")
        presetLayout = QtWidgets.QFormLayout()
        self.preset_cb = QtWidgets.QComboBox()
        self.preset_cb.addItems(list(self.preview_images.keys()))
        self.mood_cb = QtWidgets.QComboBox()
        self.mood_cb.addItems(["Neutral", "Cinematic", "Soft"])
        presetLayout.addRow("𝄞⨾Preset:", self.preset_cb)
        presetLayout.addRow("𝄞⨾Color Mood:", self.mood_cb)
        self.grpPresets.setLayout(presetLayout)
        leftCol.addWidget(self.grpPresets)

        #Sliders: Intensity|Exposure
        self.grpSliders = QtWidgets.QGroupBox("Adjustments")
        sliderLayout = QtWidgets.QFormLayout()
        self.intensity_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.intensity_slider.setMinimum(1)
        self.intensity_slider.setMaximum(300)
        self.intensity_slider.setValue(100)
        self.intensity_label = QtWidgets.QLabel("Intensity: 1.0")

        self.exposure_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.exposure_slider.setMinimum(-50)
        self.exposure_slider.setMaximum(50)
        self.exposure_slider.setValue(0)
        self.exposure_label = QtWidgets.QLabel("Exposure: 0.0")

        sliderLayout.addRow(self.intensity_label, self.intensity_slider)
        sliderLayout.addRow(self.exposure_label, self.exposure_slider)
        self.grpSliders.setLayout(sliderLayout)
        leftCol.addWidget(self.grpSliders)

        #Button
        buttonLayout = QtWidgets.QHBoxLayout()
        self.resetBtn = QtWidgets.QPushButton("✧Reset✧")
        self.resetBtn.setObjectName("resetBtn")
        self.generateBtn = QtWidgets.QPushButton("✧Generate Rig✧")
        self.generateBtn.setObjectName("generateBtn")
        buttonLayout.addWidget(self.resetBtn)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.generateBtn)
        leftCol.addLayout(buttonLayout)

        contentLayout.addLayout(leftCol, stretch=3)

        #Preview
        rightCol = QtWidgets.QVBoxLayout()
        self.previewLabel = QtWidgets.QLabel()
        self.previewLabel.setObjectName("preview")
        self.previewLabel.setAlignment(QtCore.Qt.AlignCenter)
        rightCol.addWidget(self.previewLabel)

        #Status
        self.statusLabel = QtWidgets.QLabel()
        self.statusLabel.setProperty("class", "small")
        rightCol.addWidget(self.statusLabel)
        rightCol.addStretch()

        contentLayout.addLayout(rightCol, stretch=2)

        self.preset_cb.currentIndexChanged.connect(self.update_preview)
        self.mood_cb.currentIndexChanged.connect(self.update_status)
        self.intensity_slider.valueChanged.connect(self.update_preview)
        self.exposure_slider.valueChanged.connect(self.update_preview)
        self.resetBtn.clicked.connect(self.reset)
        self.generateBtn.clicked.connect(self.generate)

        self.update_preview()

    def update_status(self):
        preset = self.preset_cb.currentText()
        mood = self.mood_cb.currentText()
        self.statusLabel.setText(f"Preset: {preset} | Mood: {mood}")

    def update_preview(self):
        preset = self.preset_cb.currentText()
        mood = self.mood_cb.currentText()
        intensity = round(self.intensity_slider.value() / 100.0, 2)
        exposure = round(self.exposure_slider.value() / 10.0, 2)
        self.statusLabel.setText(f"Preset: {preset} | Mood: {mood} | Intensity: {intensity} Exposure: {exposure}")

        path = self.preview_images.get(preset)
        if path and os.path.exists(path):
            pix = QtGui.QPixmap(path)
        else:
            pix = QtGui.QPixmap(200, 200)
            pix.fill(QtGui.QColor("#EDEDDD"))

        img = pix.toImage().convertToFormat(QtGui.QImage.Format_ARGB32)
        for y in range(img.height()):
            for x in range(img.width()):
                c = QtGui.QColor(img.pixel(x, y))
                r = min(int(c.red() * intensity + exposure*5), 255)
                g = min(int(c.green() * intensity + exposure*5), 255)
                b = min(int(c.blue() * intensity + exposure*5), 255)
                img.setPixel(x, y, QtGui.QColor(r, g, b).rgba())
        pix = QtGui.QPixmap.fromImage(img).scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.previewLabel.setPixmap(pix)

    def reset(self):
        self.preset_cb.setCurrentIndex(0)
        self.mood_cb.setCurrentIndex(0)
        self.intensity_slider.setValue(100)
        self.exposure_slider.setValue(0)
        self.update_preview()

    def generate(self):
        preset = self.preset_cb.currentText()
        mood = self.mood_cb.currentText()
        intensity = round(self.intensity_slider.value() / 100.0, 2)
        exposure = round(self.exposure_slider.value() / 10.0, 2)

        preset_map = {
            "3-Point Lighting": util.create_three_point,
            "Studio Portrait": util.create_studio_rig,
            "Dramatic": util.create_dramatic,
            "HDR Dome": util.create_hdr_dome,
            "Sunset": util.create_sunset,
            "Moonlight": util.create_moonlight,
            "Product Showcase": util.create_product,
            "Horror": util.create_horror,
            "Silhouette": util.create_silhouette,
            "Stylized": util.create_stylized,
        }

        func = preset_map.get(preset)
        if func:
            func(intensity, mood, exposure)
            QtWidgets.QMessageBox.information(
                self, "Light Rig Generator",
                f"✨ Generated {preset} rig successfully! ✨"
            )
        else:
            QtWidgets.QMessageBox.warning(
                self, "Light Rig Generator",
                f"Preset '{preset}' not implemented."
            )

def run():
    global ui
    try:
        ui.close()
    except:
        pass
    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = LightRigUI(parent=ptr)
    ui.show()
    return ui

