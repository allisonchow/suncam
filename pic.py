"""
Take a photo from the webcam and save as a 1920x1080 JPEG file, where the
filename is derived from the timestamp (in UTC).
"""

import os
import datetime

os.system(
    "fswebcam --jpeg 100 -D 2 -F 20 -S 5 -r 1920x1080 --flip v,h '/home/suncam/fswebcampics/%s.jpg'"
    % datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
)
