# 🗺️ Google Maps Tile Downloader & Mosaic Stitcher (GUI)

This Python application allows you to download static tiles from Google Maps within a specified bounding box, and stitch them together into a high-resolution mosaic. The GUI is built using **PyQt6**, and image processing is handled with **Pillow (PIL)**.

## 🚀 Features

- GUI-based interface using PyQt6
- Define a bounding box (north/south/east/west) for tile coverage
- Set Google Maps zoom level (1–21)
- Use your own **Google Maps Static API Key**
- Choose output folder and mosaic filename prefix (Area ID)
- Optional: Toggle Google Map labels (e.g. road names, place names)
- Live **progress bar** during tile download and stitching
- Final stitched mosaic saved as `mosaic.png`

---

## 🖥️ GUI Overview

| UI Element           | Purpose |
|----------------------|---------|
| **North/South Latitude** | Define vertical bounds |
| **East/West Longitude** | Define horizontal bounds |
| **Zoom Level**       | Controls tile resolution |
| **API Key**          | Required for downloading tiles |
| **Area ID**          | Prefix used in filenames |
| **Output Folder**    | Save location for tiles and mosaic |
| **Hide Labels**      | Option to hide map labels in tiles |
| **Download Tiles**   | Starts tile download process |
| **Stitch Mosaic**    | Assembles downloaded tiles into a single image |

---

## 📦 Requirements

Install required packages with:

```bash
pip install PyQt6 Pillow requests
```

---

## 🔧 Google Maps API Setup

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the **Maps Static API**
3. Generate an **API Key**
4. Copy and paste your API key into the application

---

## 🛠️ Running the App

```bash
python map_tile_gui.py
```

Replace `map_tile_gui.py` with the filename you saved this script as.

---

## 🧩 Output

- Individual tiles are saved as: `AreaID_col,row.png` (e.g. `Mumbai_0,0.png`)
- Final mosaic is saved as: `mosaic.png` in the selected folder
- Tile metadata is logged in `tiles_log.csv`

---

## 📸 Screenshots

> *(Optional: Add screenshots of the GUI and stitched output here)*

---

## 📄 License

MIT License

---

## 🤝 Acknowledgements

- [Google Maps Static API](https://developers.google.com/maps/documentation/maps-static/overview)
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/intro)
- [Pillow](https://python-pillow.org/)

---

## 🧠 TODOs / Enhancements

- [ ] Add cancel button for long operations
- [ ] Add mosaic preview within GUI
- [ ] Allow world file generation (`.pgw`)
- [ ] Multi-threading for UI responsiveness
