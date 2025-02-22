import os


def mkdirs(filepath):
	dirs = os.path.dirname(filepath)
	if not os.path.exists(dirs):
		os.makedirs(dirs, mode=755, exist_ok=True)
