# 项目创意说明

# Project Creative Statement
The theme of the project is smog. Short lines extending in all directions simulate the shape of fireworks bursting, metaphorically representing the scene of excessive emission of pollutants such as fireworks. The light blue circles in the background not only resemble the hazy light and shadow after being shrouded in smog, but also can represent the pollution circle formed by the pervading smog, intuitively showing the impact of smog on the environment and making the connection between the image elements and the theme of smog more pictorial and narrative.

# PM2.5 Visualization Animation Project

## Project Overview
This project uses Python and Pygame to dynamically visualize PM2.5 data. The animation presents PM2.5 concentrations from various locations in a spiral with multi-stage color gradients. The background features a radial gradient from light purple at the center to white at the edges, with 30 slowly floating light blue semi-transparent circles, creating a soft and technological atmosphere.

## Main Features
- Reads PM2.5 data from `data.csv`, with automatic normalization and interpolation.
- Dynamic spiral animation with multi-stage color gradients to highlight data layers.
- Radial gradient background (light purple center, white edges), no extra shapes.
- 30 light blue semi-transparent circles float slowly, with random size, brightness, and transparency.
- Real-time display of current country/region and its PM2.5 value.

## Environment
- Python 3.8 or above
- Dependencies: pygame, pandas

## Quick Start
1. Install dependencies:
	```bash
	pip install pygame pandas
	```
2. Prepare the data file:
	- Save PM2.5 data as `data.csv`, which should contain the columns `Location` and `FactValueNumericLow`.
3. Run the main program:
	```bash
	python Concentrations-of-fine-particulate-matter/extract_pdf_pm25.py
	```

## File Structure
```
数据pdf.pdf
data.csv
Concentrations-of-fine-particulate-matter/
	 extract_pdf_pm25.py   # Main animation script
	 README.md             # Project documentation
	 ...
```

## Visualization Effect
- Animation window 900x900, spiral data center, soft gradient background.
- Circles float slowly, enhancing spatial and technological feel.
- Colors and animation parameters can be customized in `extract_pdf_pm25.py`.

## Contact & Feedback
For suggestions or questions, please leave a message in GitHub Issues.

---
Project Author: tong02160216
# Concentrations-of-fine-particulate-matter