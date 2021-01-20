import csv
import glob
import os
import subprocess


VIDEO_DIR = "/data/zxxia/videos"
SAVE_DIR = "bw_compute"

# VIDEOS = ["motorway", 'highway', 'jp', 'highway_normal_traffic', 'russia', 'russia1', 'drift']
# VIDEOS = ["crossroad3_23", "crossroad4_21", "crossroad4_29", "crossroad4_30",
#           "driving1_24", "driving2_0", "driving2_1", "driving2_24",
#           "driving2_33", "lane_split_5", "nyc_3", "park_0", "park_36"]
VIDEOS = ["driving1_24", "park_0"]
FPS_MAP = {
    'traffic': 30,
    "motorway": 24,
    "highway": 25,
    "jp": 30,
    "highway_normal_traffic": 30,
    "russia": 30,
    "russia1": 30,
    "drift": 30,
    "crossroad3_23": 30,
    "crossroad4_21": 30,
    "crossroad4_29": 30,
    "crossroad4_30": 30,
    "driving1_24": 30,
    "driving2_0": 30,
    "driving2_1": 30,
    "driving2_24": 30,
    "driving2_33": 30,
    "lane_split_5": 30,
    "nyc_3": 30,
    "park_0": 30,
    "park_36": 30,
}

PROC_IMG_ROOT = '2nd_round_imgs'


def encode(start_fid, img_dir, qp, scale, nb_frames, fps, vid_path,
           list_file=None):
    if list_file is None:
        cmd = "ffmpeg -y -loglevel error -start_number {} -r {}" \
            " -i {}/%06d.jpg -vcodec libx264 -qp {} -pix_fmt yuv420p -vf {} " \
            "-frames:v {} {} -hide_banner".format(start_fid, fps, img_dir, qp,
                                                  scale, nb_frames, vid_path)
    else:
        cmd = "ffmpeg -y -loglevel error -i {} -vcodec libx264 -qp {} " \
            "-pix_fmt yuv420p -vf {} {} -hide_banner".format(
                list_file, qp, scale, vid_path)
    print(cmd)
    size = 0
    encode_ret = subprocess.run(cmd.split(' '), check=True)
    if encode_ret.returncode != 0:
        # size = 0;
        raise RuntimeError("Encoding Failed!")
    else:
        size = os.path.getsize(vid_path)
    return size

# def encode(start_fid, img_dir, qp, scale, nb_frames, fps, vid_path):
#     cmd = "ffmpeg -y -loglevel error -start_number {} -r {}" \
#         " -i {}/%06d.jpg -vcodec libx264 -qp {} -pix_fmt yuv420p -vf {} " \
#         "-frames:v {} {} -hide_banner".format(start_fid, fps, img_dir, qp,
#                                               scale, nb_frames, vid_path)
#     print(cmd)
#     size = 0
#     encode_ret = subprocess.run(cmd.split(' '), check=True)
#     if encode_ret.returncode != 0:
#         # size = 0;
#         raise RuntimeError("Encoding Failed!")
#     else:
#         size = os.path.getsize(vid_path)
#     return size

# for video in VIDEOS:
#     img_dir = os.path.join(VIDEO_DIR, video, '720p')
#     img_paths = glob.glob(os.path.join(img_dir, "*.jpg"))
#     vid_frame_cnt = len(img_paths)
#     fps = FPS_MAP[video]
#     scale = "scale=1280:720"
#     chunk_duration = 30  # second
#     log_path = os.path.join(SAVE_DIR, "{}.csv".format(video))
#     with open(log_path, 'w', 1) as f:
#         csv_writer = csv.writer(f, lineterminator='\n')
#         csv_writer.writerow(['video', 'low_quality_bandwidth',
#                              'high_quality_bandwidth'])
#         for i in range(0, vid_frame_cnt, fps * chunk_duration):
#             chunk_id = i // (fps * chunk_duration)
#             chunk_name = '{}_{}'.format(video, chunk_id)
#             vid_path = os.path.join(SAVE_DIR, '{}.mp4'.format(chunk_name))
#             high_q_vid_size = encode(i, img_dir, 1, scale,
#                                      fps*chunk_duration, fps, vid_path)
#             low_q_vid_size = encode(i, img_dir, 11, scale,
#                                     fps*chunk_duration, fps, vid_path)
#             # print(high_q_vid_size, low_q_vid_size)
#             csv_writer.writerow([chunk_name, low_q_vid_size, high_q_vid_size])
#             if os.path.exists(vid_path):
#                 os.remove(vid_path)


for video in VIDEOS:
    img_dir = os.path.join(VIDEO_DIR, video, '720p')
    img_dir_2nd_round = os.path.join(PROC_IMG_ROOT, video)
    img_paths = glob.glob(os.path.join(img_dir, "*.jpg"))
    vid_frame_cnt = len(img_paths)
    fps = FPS_MAP[video]
    scale = "scale=1280:720"
    chunk_duration = 30  # second
    log_path = os.path.join(SAVE_DIR, "{}_2nd_iter.csv".format(video))
    with open(log_path, 'w', 1) as f:
        csv_writer = csv.writer(f, lineterminator='\n')
        csv_writer.writerow(['video', '2n_round_bandwidth'])
        for i in range(0, vid_frame_cnt, fps * chunk_duration):
            end_frame_idx = min(i + (fps * chunk_duration), vid_frame_cnt)
            chunk_id = i // (fps * chunk_duration)
            chunk_name = '{}_{}'.format(video, chunk_id)
            vid_path = os.path.join(SAVE_DIR, '{}.mp4'.format(chunk_name))

            # img_paths = glob.glob(os.path.join(img_dir_2nd_round, "*.jpg"))
            img_paths = [os.path.join(img_dir_2nd_round, "{:06d}.jpg".format(j))
                         for j in range(i, end_frame_idx)
                         if os.path.exists(
                             os.path.join(img_dir_2nd_round, "{:06d}.jpg".format(j)))]
            if len(img_paths) == chunk_duration * fps:
                high_q_vid_size = encode(i, img_dir_2nd_round, 1, scale,
                                         fps*chunk_duration, fps, vid_path)
            elif len(img_paths) > 0:

                tmp_list_file = video + '_list.txt'
                with open(tmp_list_file, 'w') as f_list:
                    for target_img_path in img_paths:
                        # based on sample rate, decide whether this frame is
                        # sampled
                        line = 'file \'{}\'\n'.format(target_img_path)
                        f_list.write(line)
                high_q_vid_size = encode(i, img_dir_2nd_round, 1, scale,
                                         fps*chunk_duration, fps, vid_path,
                                         tmp_list_file)
            else:
                high_q_vid_size = 0
            # print(high_q_vid_size, low_q_vid_size)
            csv_writer.writerow([chunk_name, high_q_vid_size])
            if os.path.exists(vid_path):
                os.remove(vid_path)

# for video in VIDEOS:
#     output_dir = os.path.join(PROC_IMG_ROOT, video)
#     os.makedirs(output_dir, exist_ok=True)
#     img_dir = os.path.join(VIDEO_DIR, video, '720p')
#     img_paths = glob.glob(os.path.join(img_dir, "*.jpg"))
#     vid_frame_cnt = len(img_paths)
#     print('{} = {}'.format(video, vid_frame_cnt))
#
#     for i in range(0, vid_frame_cnt, 15):
#         end_frame = min(vid_frame_cnt, i+15)
#         seg_dir = "debugging/{}_dds_1.0_1.0_11_1_0.0_twosides_batch_15_0.5_0.3_0.01-cropped-{}-{}".format(video, i, end_frame)
#         if not os.path.exists(seg_dir):
#             # print(seg_dir, "doest not exist!")
#             continue
#         os.system("cp {}/*.jpg {}".format(seg_dir, output_dir))
#     print(len(glob.glob(os.path.join(output_dir, "*.jpg")))) #== vid_frame_cnt, "{} frame cnt is not equal!".format(video)
#     # fps = FPS_MAP[video]
#     # scale = "scale=1280:720"
#     # chunk_duration = 30  # second
