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

print("%d files are marked for deletion. If this sounds correct, please input the following:" % count)
print("\t\'DELETE%d\'" % count)
code = input()
if code == "DELETE%d" % count:
	for f in to_rm:
		os.remove(fpath)
	print("%d files deleted." % count)
else:
	print("No files were deleted.")



