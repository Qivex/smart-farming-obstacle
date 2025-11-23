How to use:
1) Install Python & Blender (tested with Blender 4.5)
2) Create a Python virtual environment in "src":
	python venv .
3) With the virtual environment active, install the requirements:
	pip install -r requirements.txt
4) In both "extractor.config.json" files set property "recordingPath" to absolute path of MCAP recordings (not included):
	- For 01_zed: "Pascal/zed_only2/zed_only_0.mcap" (MD5 = 86173f950e2a1ec78535e9c10c826b98)
	- For 02_gps: "rosbag2_2025_05_12-14_18_46/rosbag2_2025_05_12-14_18_46_0.mcap" (MD5 = 5c36135982bdd5691293a1919ea4aa08)
5) Start "run-extractor.bat", this will create a new folder "export@<timestamp>"
6) In both "generator.config.json" files set property "dataFolder" to the path of this new folder
7) Install Blender and adjust BLENDER_PATH in "run-generator.bat" (optional: remove "--background" flag for GUI)
8) Select the obstacle from any of the available scenes. Adjust path to .blend project in "run-generator.bat" accordingly.
9) Start "run-generator.bat", this will create a new folder "render@<timestamp>" (render might take several minutes depending on hardware)
10) In "validator.config.json" add image paths to array "images" to be analyzed using the given method.
11) Start "run-validator.bat"


Optional:
- Remove "--background" flag in "run-generator.bat to enable GUI and avoid close-on-finish
- In "generator.config.json" set property render.skip=true to skip the actual rendering (used for scene creation debugging)


Recommendation:
- View the rendered .exr files using DJV (https://github.com/grizzlypeak3d/DJV)