#!/usr/bin/env python3

import os, sys

count = 0
to_rm = []
for root, dirs, files in os.walk(os.getcwd()):
	for f in files:
		if f.startswith("arrayJob_") and f.endswith(".err"):
			fpath = os.path.join(root, f)
			if os.stat(fpath).st_size == 0:
				to_rm.append(fpath)
				count += 1

if count > 0:
	print("%d files are marked for deletion. If this sounds correct, please input the following: DELETE%d" % (count, count))
	code = input()
	if code == "DELETE%d" % count:
		for f in to_rm:
			os.remove(f)
		print("%d files deleted." % count)
	else:
		print("No files were deleted.")
else:
	print("0 files were marked for deletion. Exiting program.")


