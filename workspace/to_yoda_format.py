import csv
import os

from PIL import Image, ImageDraw
import pandas as pd

from dds_utils import read_results_dict

VIDEOS = ["motorway", 'highway', 'jp', 'highway_normal_traffic', 'russia',
          'russia1', 'drift', 'traffic']
# VIDEOS = ["crossroad3_23", "crossroad4_21", "crossroad4_29", "crossroad4_30",
#           "driving1_24", "driving2_0", "driving2_1", "driving2_24",
#           "driving2_33", "lane_split_5", "nyc_3", "park_0", "park_36"]

for video in VIDEOS:
    dds_results_path = 'results/{}_dds_1.0_1.0_11_1_0.0_twosides_batch_15_0.5_0.3_0.01'.format(
        video)
    if not os.path.exists(dds_results_path):
        print(dds_results_path, "does not exist!")
        continue
    dds_results = read_results_dict(dds_results_path)

    frame = Image.open('/data/zxxia/videos/traffic/720p/%06d.jpg' % 0)
    width, height = frame.size
    data = []

    # for fid in range(len(dds_results)):
    with open('acc_compute/{}.csv'.format(video), 'w', 1) as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['frame id', 'xmin', 'ymin', 'xmax', 'ymax', 'class', 'score'])
        for fid in range(len(dds_results)):
            for region in dds_results[fid]:
                x, y, w, h, label, conf = region.x, region.y, region.w, region.h, region.label, region.conf
                x, w = x*width, w*width
                y, h = y*height, h*height
                # data.append({
                #     'frame id': fid+1,
                #     'xmin': int(x),
                #     'ymin': int(y),
                #     'xmax': int(x+w),
                #     'ymax': int(y+h),
                #     'class': int(label),
                #     'score': conf
                # })
                csv_writer.writerow(
                    [fid+1,
                     int(x),
                     int(y),
                     int(x+w),
                     int(y+h),
                     int(label),
                     conf])
            if len(dds_results[fid]) == 0:
                csv_writer.writerow([fid+1, '', '', '', '', '', ''])

    # dataframe = pd.DataFrame(data)
    # dataframe.to_csv(, index=False)
