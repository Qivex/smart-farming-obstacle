How the bone config was created:
1) Extracted transform configs from recording using:
	"devutils/extract_transforms.py rosbag2_2025_05_12-14_18_46_0.mcap"
	=> 3 files: transforms_Root.json, transforms_os_sensor.json, transforms_zed_camera_link.json
2) Copied everything (except wheels) from "transform_Root.json" into config["bones"]
3) Copied everything from "transform_os_sensor.json" into "os_sensor" bone's "children" array
4) Created "zed_left" bone as child of "os_lidar":
	=> Offset from Lorenz' mail:
	<origin xyz="-0.0340776 -0.061614 0.132995" rpy="-1.20172 -0.0212631 1.58427"/>
	=> Rotation from Quaternion.inverted() of the logged quaternion to cancel the current rotation:
	{"x": 0.29323244094848633, "y": 0.24763408303260803, "z": 0.6623271107673645, "w": 0.6434399485588074}
5) Created "zed_right" bone by moving 12cm (= lens distance) into positive X direction