import os

from ament_index_python.packages import get_package_share_directory
from ament_index_python.packages import get_package_prefix


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='my_bot' #<--- CHANGE ME
    dev_ws_dir = os.getcwd()
    src_dir = dev_ws_dir + "/src/" + package_name
    config_dir = src_dir + "/config"

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
            launch_arguments={'gz_args': [' ', 'default.sdf'], 'on_exit_shutdown': 'true'}.items()
    )


    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='ros_gz_sim', executable='create',
                        arguments=['-topic', 'robot_description',
                                   '-name', 'my_bot','-z','0.1'],
                        output='screen')

    # Bridges GZ2ROS & ROS2GZ
    bridge_params = config_dir + "/topic_bridge.yaml"

    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',
        ],
        output='screen',
    )

    # RQt
    rqt = Node(
        package='rqt_topic',
        executable='rqt_topic',
        arguments=['-t']
    )

    # control_param = config_dir + "/my_controllers.yaml"
    # control_node = Node(
    #     package="controller_manager",
    #     executable="ros2_control_node",
    #     parameters=[control_param],
    #     output="both",
    # )

    # For camera, use dedicated gz_image bridge instead
    # start_gazebo_ros_image_bridge_cmd = Node(
    #     package='ros_gz_image',
    #     executable='image_bridge',
    #     arguments=['/camera/image_raw'],
    #     output='screen',
    # )

    # diff_drive_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["diff_cont"],
    # )

    # joint_broad_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["joint_broad"],
    # )




    # Launch them all!
    return LaunchDescription([
        rsp,
        rqt,
        gazebo,
        spawn_entity,
        start_gazebo_ros_bridge_cmd,
    ])
