import numpy as np

def scale_pos(pos, scale):
	return {
		"x": pos["x"] * scale["x"],
		"y": pos["y"] * scale["y"],
		"z": pos["z"] * scale["z"]
	}

def translate_pos(pos, offset):
	return {
		"x": pos["x"] + offset["x"],
		"y": pos["y"] + offset["y"],
		"z": pos["z"] + offset["z"]
	}

def rotate_pos(pos, rotation_quaternion):
	return {}


def coord_transform(value, scale, rotation, translation):
	pass
