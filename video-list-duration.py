#!/usr/bin/env python3

import os, sys
import glob
import subprocess
import functools
import math

os.chdir(os.path.dirname(sys.argv[0]))

def get_video_duration(filename):
	result = subprocess.run(
	["ffprobe", "-v", "error", "-show_entries",
	 "format=duration", "-of",
	 "default=noprint_wrappers=1:nokey=1", filename],
	stdout = subprocess.PIPE,
	stderr = subprocess.STDOUT)
	return float(result.stdout)

def seconds_to_hms(s, round_seconds=False):
	if round_seconds: s = round(s)
	h = math.floor(s / 3600)
	s -= h * 3600
	m = math.floor(s / 60)
	s -= m * 60
	return '{}:{}:{}'.format(h, m, s)

# Get videos

videos = []

for video_type in ['*.mp4', '*.avi', '*.mov', '*.mkv']:
	videos.extend(glob.glob(video_type))

videos.sort()

# Get durations

total_duration = 0
output = ''

for video in videos:
	video_duration = get_video_duration(video)
	total_duration += video_duration
	output += '{} - {}\n'.format(seconds_to_hms(video_duration, True), video)

total_duration = round(total_duration)

# Output

output += '---------------------------------------------\n'
output += '{} ({}s)\n'.format(seconds_to_hms(total_duration), total_duration)

print(output)

with open('duration.txt', 'w') as f:
	f.write(output)


