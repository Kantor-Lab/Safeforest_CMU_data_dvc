# Launch covnversion nodes and an rviz
tmux new-session -s visualize \; \
  send-keys 'ROS_NAMESPACE=/left/camera rosrun image_proc image_proc' C-m \; \
  split-window -v \; \
  send-keys 'ROS_NAMESPACE=/right/camera rosrun image_proc image_proc' C-m \; \
  split-window -h \; \
  send-keys 'roslaunch scripts/visualization/transform_lidar.launch' C-m \; \
  select-pane -t 0 \; \
  split-window -h \; \
  send-keys 'rviz -d scripts/visualization/aiira.rviz -f velodyne' C-m \; \
