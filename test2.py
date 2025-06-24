import pyrealsense2 as rs
import numpy as np

# 1. Start RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
pipeline.start(config)

try:
    # 2. Wait for frames
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()

    if not depth_frame:
        raise RuntimeError("No depth frame received")

    # 3. Convert depth frame to NumPy array
    depth_image = np.asanyarray(depth_frame.get_data())

    # 4. Define center pixel and 10x10 box
    center_x = 200
    center_y = 400
    half_box = 5  # Half of 10 → will extract from [y-5:y+5, x-5:x+5]

    # 5. Slice 10x10 region safely (make sure you don’t go out of bounds)
    min_y = max(center_y - half_box, 0)
    max_y = min(center_y + half_box, depth_image.shape[0])
    min_x = max(center_x - half_box, 0)
    max_x = min(center_x + half_box, depth_image.shape[1])

    region = depth_image[min_y:max_y, min_x:max_x]

    # 6. Print the region
    print(f"Depth image shape: {depth_image.shape}")
    print(f"10x10 region around pixel ({center_x}, {center_y}):")
    print(region)

finally:
    pipeline.stop()

