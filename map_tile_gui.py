import os
import math
import requests
from PIL import Image
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QHBoxLayout, QCheckBox, QSpinBox,
    QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt
import sys


def latLngToPoint(mapWidth, mapHeight, lat, lng):
    x = (lng + 180) * (mapWidth / 360)
    y = ((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2) * mapHeight
    return x, y


def pointToLatLng(mapWidth, mapHeight, x, y):
    lng = x / mapWidth * 360 - 180
    n = math.pi - 2 * math.pi * y / mapHeight
    lat = math.degrees(math.atan(0.5 * (math.exp(n) - math.exp(-n))))
    return lat, lng


def getLatStep(mapWidth, mapHeight, yScale, lat, lng):
    pointX, pointY = latLngToPoint(mapWidth, mapHeight, lat, lng)
    steppedPointY = pointY - (mapHeight / yScale)
    newLat, _ = pointToLatLng(mapWidth, mapHeight, pointX, steppedPointY)
    return newLat - lat


def getLngStep(mapWidth, mapHeight, xScale, lat, lng):
    pointX, pointY = latLngToPoint(mapWidth, mapHeight, lat, lng)
    steppedPointX = pointX + (mapWidth / xScale)
    _, newLng = pointToLatLng(mapWidth, mapHeight, steppedPointX, pointY)
    return newLng - lng


class TileDownloaderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Google Maps Tile Downloader & Stitcher")
        self.setMinimumWidth(600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.north_input = self.create_labeled_input("North Latitude:", layout)
        self.south_input = self.create_labeled_input("South Latitude:", layout)
        self.east_input = self.create_labeled_input("East Longitude:", layout)
        self.west_input = self.create_labeled_input("West Longitude:", layout)
        self.api_key_input = self.create_labeled_input("Google API Key:", layout)
        self.area_id_input = self.create_labeled_input("Area ID (used in filenames):", layout)

        zoom_layout = QHBoxLayout()
        zoom_layout.addWidget(QLabel("Zoom Level:"))
        self.zoom_input = QSpinBox()
        self.zoom_input.setRange(1, 21)
        self.zoom_input.setValue(19)
        zoom_layout.addWidget(self.zoom_input)
        layout.addLayout(zoom_layout)

        out_layout = QHBoxLayout()
        self.output_folder_input = QLineEdit()
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.select_output_folder)
        out_layout.addWidget(QLabel("Output Folder:"))
        out_layout.addWidget(self.output_folder_input)
        out_layout.addWidget(browse_btn)
        layout.addLayout(out_layout)

        # New Checkbox: Toggle label visibility
        self.hide_labels_checkbox = QCheckBox("Hide Labels (for cleaner maps)")
        self.hide_labels_checkbox.setChecked(True)
        layout.addWidget(self.hide_labels_checkbox)

        self.download_button = QPushButton("Download Tiles")
        self.download_button.clicked.connect(self.download_tiles)
        layout.addWidget(self.download_button)

        self.stitch_button = QPushButton("Stitch Mosaic")
        self.stitch_button.clicked.connect(self.stitch_mosaic)
        layout.addWidget(self.stitch_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def create_labeled_input(self, label, parent_layout):
        row = QHBoxLayout()
        lbl = QLabel(label)
        input_field = QLineEdit()
        row.addWidget(lbl)
        row.addWidget(input_field)
        parent_layout.addLayout(row)
        return input_field

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder_input.setText(folder)

    def download_tiles(self):
        try:
            north = float(self.north_input.text())
            south = float(self.south_input.text())
            east = float(self.east_input.text())
            west = float(self.west_input.text())

            if north > 85 or south < -85:
                raise ValueError("Latitude range must be within -85 to 85 for Mercator projection.")
            if east < west:
                QMessageBox.warning(self, "Antimeridian Warning",
                                    "East longitude is less than west longitude. Your region may cross the antimeridian.")

            zoom = self.zoom_input.value()
            api_key = self.api_key_input.text().strip()
            output_dir = self.output_folder_input.text().strip()
            area_id = self.area_id_input.text().strip()
            hide_labels = self.hide_labels_checkbox.isChecked()

            os.makedirs(output_dir, exist_ok=True)

            mapHeight = mapWidth = 256
            picHeight = picWidth = 640
            scale = 2
            maptype = "roadmap"
            xScale = math.pow(2, zoom) / (picWidth / mapWidth)
            yScale = math.pow(2, zoom) / (picHeight / mapWidth)

            lngStep = getLngStep(mapWidth, mapHeight, xScale, north, west)

            total_tiles = 0
            lat = north
            while lat >= south:
                lng = west
                while lng <= east:
                    total_tiles += 1
                    lng += lngStep
                lat -= getLatStep(mapWidth, mapHeight, yScale, lat, west)

            downloaded = 0
            self.progress_bar.setValue(0)

            log_file_path = os.path.join(output_dir, "tiles_log.csv")
            with open(log_file_path, 'w') as log_file:
                log_file.write("tilename,lat,lon\n")

                lat = north
                col = 0
                while lat >= south:
                    lng = west
                    row = 0
                    while lng <= east:
                        center = f"{lat},{lng}"
                        style_param = "&style=feature:all|element:labels|visibility:off" if hide_labels else ""
                        url = (f"https://maps.googleapis.com/maps/api/staticmap?center={center}&zoom={zoom}"
                               f"&size={picWidth}x{picHeight}&maptype={maptype}&scale={scale}"
                               f"{style_param}&key={api_key}")
                        filename = os.path.join(output_dir, f"{area_id}_{col},{row}.png")
                        try:
                            r = requests.get(url, timeout=10)
                            r.raise_for_status()
                            with open(filename, 'wb') as f:
                                f.write(r.content)
                            log_file.write(f"{area_id}_{col},{row}.png,{lat},{lng}\n")
                        except Exception as e:
                            print(f"Failed to download {filename}: {e}")

                        downloaded += 1
                        self.progress_bar.setValue(int((downloaded / total_tiles) * 100))

                        lng += lngStep
                        row += 1
                    lat -= getLatStep(mapWidth, mapHeight, yScale, lat, west)
                    col += 1

            QMessageBox.information(self, "Done", "Tile download complete.")
        except Exception as ex:
            QMessageBox.critical(self, "Download Error", str(ex))

    def stitch_mosaic(self):
        try:
            folder = self.output_folder_input.text().strip()

            def get_tile_coordinates(filename):
                match = re.search(r'_(\d+),(\d+)\.png$', filename)
                if match:
                    return int(match.group(1)), int(match.group(2))
                return None

            images = {}
            tile_width, tile_height = None, None

            for filename in os.listdir(folder):
                if filename.endswith(".png"):
                    coords = get_tile_coordinates(filename)
                    if coords:
                        row, col = coords
                        img = Image.open(os.path.join(folder, filename))
                        images[(row, col)] = img
                        if tile_width is None or tile_height is None:
                            tile_width, tile_height = img.size

            if not images:
                raise RuntimeError("No tile images found in folder.")

            max_row = max(row for row, col in images.keys())
            max_col = max(col for row, col in images.keys())

            mosaic_width = (max_col + 1) * tile_width
            mosaic_height = (max_row + 1) * tile_height
            mosaic = Image.new("RGB", (mosaic_width, mosaic_height))

            self.progress_bar.setValue(0)
            total = len(images)
            count = 0

            for (row, col), img in images.items():
                x_offset = col * tile_width
                y_offset = row * tile_height
                mosaic.paste(img, (x_offset, y_offset))
                count += 1
                self.progress_bar.setValue(int((count / total) * 100))

            output_path = os.path.join(folder, "mosaic.png")
            mosaic.save(output_path)
            QMessageBox.information(self, "Done", f"Mosaic saved as {output_path}")
        except Exception as ex:
            QMessageBox.critical(self, "Mosaic Error", str(ex))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = TileDownloaderGUI()
    gui.show()
    sys.exit(app.exec())
