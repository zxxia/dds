#!/bin/bash

# for VIDEO in traffic highway_normal_traffic drift highway jp russia russia1 motorway; do
#     python entrance.py ${VIDEO}
# done


# for VIDEO in motorway russia russia1; do
#     CUDA_VISIBLE_DEVICES=1  python entrance.py ${VIDEO}
# done





# for VIDEO in crossroad3_23 crossroad4_21 crossroad4_29 crossroad4_30 driving1_24 driving2_0 driving2_1 driving2_24 driving2_33 lane_split_5 nyc_3 park_0 park_36; do
for VIDEO in driving1_24  park_0 ; do
    CUDA_VISIBLE_DEVICES=1  python entrance.py ${VIDEO}
done

"crossroad3_11",  "crossroad_2",
"crossroad3_24", "crossroad3_18",
"crossroad_1",
"crossroad_17",
"crossroad_56",
"park_14", "park_31",
