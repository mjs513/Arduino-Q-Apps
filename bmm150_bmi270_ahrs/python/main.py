from arduino.app_utils import *
import time
from arduino.app_utils import App, Bridge
import numpy as np
import ahrs
from ahrs.filters import Madgwick

def get_data(ax: float, ay: float, az: float, gx: float, gy: float, gz: float, mx: int, my: int, mz: int):
  """Callback invoked by the board sketch via Bridge.notify to send sensor samples.
  """
  x_ms2 = ax * 9.81
  y_ms2 = ay * 9.81
  z_ms2 = az * 9.81
  gx_rads = gx * 0.01745329
  gy_rads = gy * 0.01745329
  gz_rads = gz * 0.01745329
  values = []
  values.append(x_ms2)
  values.append(y_ms2)
  values.append(z_ms2)
  values.append(gx_rads)
  values.append(gy_rads)
  values.append(gz_rads)
  values.append(mx)
  values.append(my)
  values.append(mz)
  process_values(values)

def process_values(values):
  #print("Accel: %f.6, %f.6, %f.6" % (values[0], values[1], values[2]))
  #print("Gyro: %f.6, %f.6, %f.6" % (values[3], values[4], values[5]))
  #print("Mag: %d, %d, %d" % (values[6], values[7], values[8]))

  # Update orientation using gyroscope + accelerometer + magnetometer
  global q
  q = madgwick.updateMARG(q, gyr=[values[3], values[4], values[5]], acc=[values[0], values[1], values[2]], mag=[values[6], values[7], values[8]])
  # If you don't have magnetometer data, use updateIMU:
  # q = madgwick.updateIMU(q, gyr=gyro_data, acc=accel_data)
  #print("Updated Quaternion:", q)

  quaternion_to_euler(q)
  print("---------------------------------------")

# Convert quaternion to Euler angles (roll, pitch, yaw) in degrees
def quaternion_to_euler(q):
    w, x, y, z = q
    # Roll (x-axis rotation)
    roll = np.degrees(np.arctan2(2*(w*x + y*z), 1 - 2*(x**2 + y**2)))
    # Pitch (y-axis rotation)
    pitch = np.degrees(np.arcsin(2*(w*y - z*x)))
    # Yaw (z-axis rotation)
    yaw = np.degrees(np.arctan2(2*(w*z + x*y), 1 - 2*(y**2 + z**2)))
    print(f"Roll: {roll:.2f}Â°, Pitch: {pitch:.2f}Â°, Yaw: {yaw:.2f}Â°")
    Bridge.notify("get_euler", roll, pitch, yaw)

# Create bridge to arduino
Bridge.provide("get_data", get_data)
# Initialize Madgwick filter
madgwick = Madgwick(frequency=1000/50, beta=0.05)
# Initial quaternion (no rotation)
q = np.array([1.0, 0.0, 0.0, 0.0], dtype=float)

print("Starting App...")
App.run()
