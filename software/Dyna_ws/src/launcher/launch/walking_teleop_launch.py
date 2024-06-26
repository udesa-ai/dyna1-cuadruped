from launch import LaunchDescription, LaunchContext
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
import launch.actions
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory
from pathlib import Path
from launch.substitutions import LaunchConfiguration
from launch.actions import RegisterEventHandler
from launch.events.process import ProcessStarted

def generate_launch_description():
    MAX_CURRENT = LaunchConfiguration('MAX_CURRENT')
    MAX_CURRENT_launch_arg = launch.actions.DeclareLaunchArgument(
        'MAX_CURRENT',
        default_value='10'
    )

    motores = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(get_package_share_directory('motor_can'),'launch'),'/motor_launch.py']
        )
    )

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    can_bridge = Node(
            package='ros2socketcan_bridge',
            namespace='',
            executable='ros2can_bridge',
            name='CANbridge',
            parameters=[{'use_sim_time': use_sim_time}],
            output="screen")
 

    control = IncludeLaunchDescription(
    	PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory('controler_cpp'), 'launch'),
             			  '/real_interface_launch.py'
            ]
        ),
        launch_arguments={'MAX_CURRENT':MAX_CURRENT}.items()
    )

    imu = IncludeLaunchDescription(
    	PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory('bno055'), 'launch'),
             			  '/bno055.launch.py'
            ]
        )
    )

    state_machine = Node(
            package='dyna_sm',
            namespace='',
            executable='state_machine',
            output="screen",
            name='state_machine',
            parameters=[
                {"frequency": 160.0}
            ])

    teleoperation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(get_package_share_directory('teleoperation'),'launch'),'/teleop_launch.py']
        )
    )

    # trace = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         [os.path.join(get_package_share_directory('tracetools_launch'),'launch'),'/example.launch.py']
    #     )
    # )

    safety = Node(
            package='safety',
            namespace='',
            executable='precautions',
            name='Precautions',
            parameters=[{'use_sim_time': use_sim_time}],
            output="screen")
    
    return LaunchDescription([
        MAX_CURRENT_launch_arg,
        # trace,
        imu,
        motores,
        can_bridge,
        # teleoperation,
        # state_machine,
        control,
        # bag,
        # imu_translator
        safety])
