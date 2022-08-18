## ISU-CMU data sharing
This data was collected the SafeForest project, in collaboration between CMU and multiple Portuguese consortium members.

# Installation
This data is managed using the [dvc](https://dvc.org/). Install `dvc` and run `dvc pull`. The first time you do so, it will ask you to give DVC permissions to your Google Drive. Do so using the account I shared the data to. The data is large (~2TB) so if you want to pull a subset of it you can run `dvc pull <dvc filenames>` for the files you want. 

# Adding data
I'd like to follow this naming convention:
`site_<site name>/date/collect_<number>`

After placing data in the appropriate location, you can add it with the following commmands. Begin by ensuring that nothing is staged in your git workspace. Then use `dvc add -R <data folders>` to recursively add the files in the folders. The recursive option allows us to download individual files in the future, which is useful given the size of the data. This process will take some time. Once it is complete, run `dvc push` to upload the data to the default remote. In parellel, you can check your git staging area. You should see that `*.dvc` files pointing to the raw data files and `.gitignore` files ignoring the raw data have been automatically staged. Commit these changes and push them to github.

You can add default documentation using `python scripts/default_documentation.py`. Ideally, fill out the template, and then add, commit, and push these files to git.

# Visualization
Install `sudo apt install ros-<ros-version>-velodyne-pointcloud` and `sudo apt install ros-melodic-velodyne-pointcloud`  
Fix the path in `scripts/transform_lidar.launch` to point to the current location and run `roslaunch scripts/transform_lidar.launch`.  
Run `roscore`  
Run `ROS_NAMESPACE=/right/camera rosrun image_proc image_proc`
Run `ROS_NAMESPACE=/left/camera rosrun image_proc image_proc`
Run `roslaunch <current directory>/scripts/visualizationo/transform_lidar.launch`
Run `rosrun rviz -d <current directory>/scripts/visualization/aiira.rviz -f velodyne`  

You can also run all of these commands in `tmux` with `source scripts/visualization/start_vis_tmux.sh`.   

To play a subset of data you can run the following command
`find -name "*bag" | sort | tail -n +<start index> | head -n <number to play> | xargs rosbag play`
