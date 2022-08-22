# SpotMicro_STT_2022
SpotMicro with Google Cloud Speech-to-Text

<center>
    <img src="./SpotMicro.jpg" width="50%" height="50%">
</center>

### News
- There's Full video instruction about this project [youtube link](https://www.youtube.com/watch?v=RocfxXIWZd4&list=PLK2UKp8KOXe1ZRbSmcO3VvE_TNs66K6lA)
- And also there's Notion Note for whole project process [Notion Link](https://www.notion.so/SpotMicro-for-G-Camp-c541934a4bad4ad48d1e37ab94c10de8) 
- Those Contents above are written in Korean

## Abstract:

Let's build quadruped robot. Only requires few low-cost parts and this repository :)

## Hardware:

The hardware for SpotMicro is designed to be both aesthetically pleasing as well as easily obtainable and readily available. Wherever possible standard screws, bolts, and bearings are used. Standard hobby grade servos are currently used for locomotion in development however, they don't appear to have sufficient power to drive the robot at more than the slowest speeds. Other options are currently being investigated (including high-voltage and brushless hobby servos typically used with RC cars) which we hope will lead to a balance between an economical as well as robust robot.

The vast majority of the hardware by volume is designed to be 3D printed. So far complete prints have been successful in PLA, though no technical barriers should exist to printing the robot in other material such as PETG, nylon, ABS, etc. The majority of parts require significant supports to print.

The files available both as STL and STP. As a community we have not yet settled on a servo for this project and therefore multiple versions of the hardware exist to support the physical dimensions of the servos and their respective servo horns. For the most up-to-date version of the hardware please visit: [https://www.thingiverse.com/thing:3761340](https://www.thingiverse.com/thing:3761340). Please see documentation for details as to which files correspond to which servo. (I use MG996R)

## Electronics:

The `Jetson Nano` operates at 5.6v, and the `PCA9658` for driving the servomotor operates at 6v. In this project, the electronic department was constructed using 11.1v LiPo batteries and `xL4015` DC Converter.

![Logo](https://gitlab.com/custom_robots/spotmicroai/website/raw/master/docs/assets/logo.png)
