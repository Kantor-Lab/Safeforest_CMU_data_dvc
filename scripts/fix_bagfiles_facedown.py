import rosbag
import os
import sys
import rospy
import pdb
from sensor_msgs.msg import Image, CameraInfo
# from camera_info_manager import CameraInfoManager

def main(args):

    if len(args) < 2:
        print('Usage: python swap_camera_info.py <path-to-bag-files>')
        sys.exit(-1)


    bagpath = args[1]
    bagfiles = []
    for bag in os.listdir(bagpath):

        if '.bag' in bag:
            bagfiles.append(os.path.join(bagpath,bag))

    #pdb.set_trace()
    inbag = rosbag.Bag(bagfiles[0],'r')
    topics = inbag.get_type_and_topic_info()[1].keys()

    timestamps = {}
    isFirst = {}
    isFirst_ = {}
    global_time = {}
    diff_times = {}
    count_topic = {}
    new_global_time = {}
    new_header_time = {}
    start_reindexing = {}
    delta_time = {}

    for topic in topics:
        global_time[topic] = []
        diff_times[topic] = []
        timestamps[topic] = []
        new_global_time[topic] = []
        new_header_time[topic] = []
        delta_time[topic] = []
        isFirst[topic] = True
        isFirst_[topic] = True
        start_reindexing[topic] = False
        count_topic[topic] = 0


    periods = {
        '/converted_odom':0.1,
        '/ekf/global_odom':0.033,
        '/ekf/local_odom':0.033,
        '/gps/fix':0.2, 
        '/mapping/left/camera_info':0.04587156, 
        '/mapping/left/image_raw':0.04587156, 
        '/mapping/right/camera_info':0.04587156, 
        '/mapping/right/image_raw':0.04587156, 
        '/odometry/gps/trust':0.,
        '/velodyne_packets':0.092421442,
        '/velodyne_points':0.092421442,
        '/xsens/imu/data': 0.002289902,
        '/xsens/imu/data/transform': 0.002289902
    }

    # print("timestamps", timestamps)


    for bag in bagfiles:

        # print("all_topics", len(topics))

        print('Processing bag :',bag)

        inbag = rosbag.Bag(bag,'r')

        for topic, msg, t in inbag.read_messages():
            # if topic == "/velodyne_points":
            if msg._has_header:
                if isFirst_[topic]:
                    global_time[topic] = t.secs + (t.nsecs)*1e-9
                    isFirst_[topic] = False
                else:                    
                    curr_global_time = t.secs + (t.nsecs)*1e-9
                    # print("curr_global_time", curr_global_time)
                    # print("past_global_time", past_global_time)
                    # print("topic", topic)
                    diff_times[topic].append(curr_global_time - global_time[topic])
                    # print("diff", diff_times[topic])
                    global_time[topic] = curr_global_time                    
                    # input()

        inbag.close()

        # print("test_diffs", diff_times['/xsens/imu/data'])
        # print("test_diffs", diff_times['/ekf/global_odom'])
        # input()

        #open the bag file and read the left and right camera info topics
        inbag = rosbag.Bag(bag,'r')


        outbag = rosbag.Bag(bag[:-6]+'_modified_'+bag[-6:],'w')
        for topic, msg, t in inbag.read_messages():
            # new_time = rospy.get_rostime()
            if msg._has_header:
                if isFirst[topic]:   
                    new_time = t 
                    new_global_time[topic] = t.secs + (t.nsecs)*1e-9#.append(new_time)
                    outbag.write(topic, msg, new_time)
                    global_time[topic] = t.secs + (t.nsecs)*1e-9
                    timestamps[topic] = msg.header.stamp.secs + (msg.header.stamp.nsecs)*1e-9      
                    new_header_time[topic] = msg.header.stamp.secs + (msg.header.stamp.nsecs)*1e-9      
                    isFirst[topic] = False
                else:
                    diff_time = diff_times[topic]
                    curr_msg_time = msg.header.stamp.secs + (msg.header.stamp.nsecs)*1e-9
                    curr_global_time = t.secs + (t.nsecs)*1e-9
                    delta = curr_global_time - global_time[topic]
                    if delta > 2:
                        start_reindexing[topic] = True                        
                        delta_time[topic] = periods[topic]
                        
                        # print("topic", topic)
                        # print("seq", msg.header.seq)
                        # print("here", curr_global_time)
                        # print("before", timestamps[topic])
                        # print("delta", delta)
                        # print("time", t)
                        # print("count_topic", count_topic[topic])
                        # print("count_topic", diff_time[count_topic[topic]-1])
                        # input()
                    else:
                        delta_time[topic] =  diff_time[count_topic[topic]-1] 

                    new_global_time[topic] = new_global_time[topic] + delta_time[topic]
                    new_time  = rospy.Time.from_sec(new_global_time[topic])
                    new_header_time[topic] = new_header_time[topic] + delta_time[topic]
                    new_header_time_ = rospy.Time.from_sec(new_header_time[topic])
                    msg.header.stamp.secs = new_header_time_.secs
                    msg.header.stamp.nsecs = new_header_time_.nsecs 
                    outbag.write(topic, msg, new_time)                    

                    global_time[topic] = curr_global_time
                    timestamps[topic] = curr_msg_time
                count_topic[topic]+=1

            else:
                a = 1
                # outbag.write(topic, msg, new_time)


            # print("t", t.secs)
            # print("topic", topic)
            # print("msg", msg)
            # input()
            # if 'right/camera_info' in topic:
            #     right_info = msg

            # elif 'left/camera_info' in topic:
            #     left_info = msg

            # if right_info is not None and left_info is not None:
            #     break
        outbag.close()
        inbag.close()
    
                            
    rospy.init_node('time_reindexer')
    

if __name__ == '__main__':
    main(sys.argv)