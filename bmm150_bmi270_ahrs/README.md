# 😀 BMM150_BMI270_AHRS

### Description

The app reads in data from the BMI270 and the BMM150 on the arduino side and transfers the accl/gyro/mag data to the linux side for process through a Madgwick filter using a AHRS package. Once processed Roll/Pitch/Yaw are transferred back to the Arduino.

### Installing libraries
On the left side of AppLab Click on the Add libraries icon. When the pop up appears I had to actually type in the name of the whole name of the library

  1. SparkFun BMI270 Arduino Library
  
  2. DFRobot_BMM150

Inorder to avoid a M_PI error @ptillisch suggest to do the following instead of the modifing platorm.txt directly:

Suggest injecting the -D_XOPEN_SOURCE=700 flag via the platform.local.txt file. This will isolate your modifications to a dedicated file, leaving platform.txt completely stock.

1. Type the following command in the terminal:
```
STORAGE_FOLDER="<some storage location>"
```
2. Replace the <some storage location> placeholder in the command with the path of a folder that can be used to persistently store files.
> Do not use the platform installation path, as this will be erased at every update of the "UNO Q Board" platform.
3. Press the ENTER key.
4. Type the following command in the terminal:
```
echo "compiler.cpp.extra_flags=-D_XOPEN_SOURCE=700" > "$STORAGE_FOLDER/
```
5. Press the ENTER key.
6. Type the following command in the terminal:
```
cp "$STORAGE_FOLDER/platform.local.txt" ~/.arduino15/package
```
7. Replace the <version> placeholder in the command with the version number of the installed "UNO Q Board" platform.
8. Press the ENTER key.

### Add AHRS package to install list

To add Python packages to your application, select the main.py file and click on the “Add file“ icon. Create a requirements.txt file and list the Python packages you need. See Requirements File Format - pip documentation v25.2 for more information.

For more info on the package

1. AHRS · PyPI: https://pypi.org/project/AHRS/

2. AHRS: Attitude and Heading Reference Systems — AHRS 0.4.0 documentation: https://ahrs.readthedocs.io/en/latest/

Now with that out of the way I then had the MCU (arduino) send data to a telemetry app once I received it from the MCU - Roll/pitch/yaw - and it worked.





