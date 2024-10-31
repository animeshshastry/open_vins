#!/usr/bin/env python3

# Main launch file for mav bringup. Runs either on the vehicle or in
# simulation. Contains nodes for a single mav agent.

# import os
# import launch
# import launch.substitutions
# import fileinput
# import socket
# import netifaces
# import re
# from packaging                          import version
# from ament_index_python.packages        import get_package_share_directory
# from launch                             import LaunchDescription
from launch.actions                     import (DeclareLaunchArgument,
                                                IncludeLaunchDescription, GroupAction,
                                                ExecuteProcess, TimerAction, RegisterEventHandler)
# from launch.event_handlers              import OnProcessStart, OnExecutionComplete
# from launch.launch_description_sources  import PythonLaunchDescriptionSource
# from launch.substitutions               import LaunchConfiguration as LC
# from launch_ros.actions                 import Node, PushRosNamespace, ComposableNodeContainer
from launch_ros.descriptions            import ComposableNode, ParameterFile
# from launch.conditions                  import IfCondition

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, OpaqueFunction
from launch.conditions import IfCondition
from launch.substitutions               import LaunchConfiguration as LC
from launch.substitutions               import TextSubstitution
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory, get_package_prefix
import os
import sys

def generate_launch_description():

    return LaunchDescription([

        DeclareLaunchArgument('namespace',                  default_value='alfa'),

        # Run OpenVINS VIO. Note that appropriate cameras must be enabled
        DeclareLaunchArgument('openvins_enable',            default_value='true'),
        DeclareLaunchArgument('openvins_config',            
            default_value=os.path.join(
                get_package_share_directory('ov_msckf'), 'config', 'multisense', 'estimator_config.yaml')),

        ################### OpenVINS VIO ######################

        Node(
            condition=IfCondition(LC('openvins_enable')),
            package='ov_msckf',
            executable='run_subscribe_msckf',
            namespace=[LC('namespace'),'/openvins'],
            output='both',
            # arguments=['--ros-args', '--log-level', (LC('namespace'),'.openvins.run_subscribe_msckf:=INFO')],
            parameters=[
                {"verbosity": "DEBUG"},
                # {'use_sim_time': LC('use_sim_time')},
                {"config_path": LC('openvins_config')},
                {'imu_frame': (LC('namespace'), '/base_link')},
                {'global_frame': (LC('namespace'), '/map')},
            ],
            remappings=[
                ('imu',('/',LC('namespace'),'/imu/data')),
                ('tracking/image_raw',('/',LC('namespace'),'/tracking/color/tracking/image_raw')),
                # ('stereo/left/image_raw',('/',LC('namespace'),'/stereo/left/image_raw')),
                # ('stereo/right/image_raw',('/',LC('namespace'),'/stereo/right/image_raw')),
            ],
            # additional_env={
            #     'ROS_DOMAIN_ID': LC('domain_id'),
            # },
        ),
    ])
