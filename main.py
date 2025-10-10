try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance
except:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import os

#allStyleSheet
QSS = """
QDialog {
    background: qlineargradient(x1:0 y1:0, x2:0 y2:1, stop:0 #ffffff, stop:1 #f6f7f8);
    border-radius: 8px;
    padding: 10px;
    font-family: "Segoe UI", "Helvetica Neue", Arial;
    color: #2b2b2b;
}
QGroupBox {
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 6px;
    margin-top: 8px;
    padding: 10px;
    background: rgba(255,255,255,0.6);
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: #555;
    font-weight: 600;
}
QLabel#titleLabel {
    font-size: 14pt;
    font-weight: 700;
    color: #1f2933;
}
QPushButton {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #ffffff, stop:1 #f2f5f7);
    border: 1px solid rgba(0,0,0,0.08);
    padding: 8px 14px;
    border-radius: 8px;
    min-height: 32px;
    font-weight: 600;
}
QPushButton#generateBtn {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #f7fbff, stop:1 #e6f0ff);
    border: 1px solid #bcd7ff;
    color: #0a4f9f;
}
QPushButton#resetBtn {
    background: transparent;
    border: 1px solid rgba(0,0,0,0.06);
    color: #4a5568;
}
QLabel#preview {
    border: 1px dashed rgba(0,0,0,0.06);
    min-width: 180px;
    min-height: 120px;
    border-radius: 6px;
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #ffffff, stop:1 #fcfdff);
}
.small {
    color: #6b7280;
    font-size: 9pt;
}
"""

#Main
class LightRigUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Light Rig Generator")
        self.setMinimumWidth(500)
        self.setMaximumWidth(760)
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
        self.titleLabel = QtWidgets.QLabel("✦⊹ ࣪ ˖Light Rig Generator⊹ ࣪ ˖✦")
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
        presetLayout.addRow("Preset:", self.preset_cb)
        presetLayout.addRow("Color Mood:", self.mood_cb)
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
        self.resetBtn = QtWidgets.QPushButton("Reset")
        self.resetBtn.setObjectName("resetBtn")
        self.generateBtn = QtWidgets.QPushButton("Generate Rig")
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
            pix = QtGui.QPixmap(180, 120)
            pix.fill(QtGui.QColor("#ffffff"))

        img = pix.toImage().convertToFormat(QtGui.QImage.Format_ARGB32)
        for y in range(img.height()):
            for x in range(img.width()):
                c = QtGui.QColor(img.pixel(x, y))
                r = min(int(c.red() * intensity + exposure*5), 255)
                g = min(int(c.green() * intensity + exposure*5), 255)
                b = min(int(c.blue() * intensity + exposure*5), 255)
                img.setPixel(x, y, QtGui.QColor(r, g, b).rgba())
        pix = QtGui.QPixmap.fromImage(img).scaled(180, 120, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
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
        print(f"Generating Rig: {preset}, Mood: {mood}, Intensity: {intensity}, Exposure: {exposure}")

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

