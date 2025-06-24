import pyrealsense2 as rs
import math
import time

# Camera parameters (RealSense D435 at 640x480)
W, H = 640, 480
HFOV = 86  # Horizontal FOV in degrees
x, y = 200, 400  # Target pixel

# Create and start the RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, W, H, rs.format.z16, 30)
pipeline.start(config)

def get_depth_and_angles():
    frames = pipeline.wait_for_frames()
    depth = frames.get_depth_frame()
    if not depth:
        print("No depth frame received")
        return

    distance = depth.get_distance(x, y)
    h_angle = ((x - W / 2) / (W / 2)) * (HFOV / 2)
   
    print(f"[INFO] Pixel ({x},{y}) → Distance: {distance:.2f} m | Angle: {h_angle:.2f}°")

try:
    print("Running RealSense depth+angle check. Press Ctrl+C to stop.")
    while True:
        get_depth_and_angles()
        time.sleep(1)  # Delay in seconds

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    pipeline.stop()
    print("Pipeline stopped.")

