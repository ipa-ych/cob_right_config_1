import os
import xacro
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler, ExecuteProcess, IncludeLaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from srdfdom.srdf import SRDF
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launch_utils import (
    add_debuggable_node,
    DeclareBooleanLaunchArg,
)



def generate_launch_description():
    moveit_demo_dir = get_package_share_directory('cob_right_config_1')
    moveit_demo = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(moveit_demo_dir, 'launch', 'demo.launch.py')
            ),
        )
    
    urdf_file = os.path.join(get_package_share_directory("cob_right_config_1"),"config","right_arm.urdf")
    doc = xacro.parse(open(urdf_file))
    xacro.process_doc(doc)
    #urdf parsing
    params = {'robot_description': doc.toxml()}
    robot_description = {'robot_description': doc.toxml()}

    gazebo_rosPackageLaunch = PythonLaunchDescriptionSource(os.path.join(get_package_share_directory("gazebo_ros"),'launch', 'gazebo.launch.py'))

    gazeboLaunch = IncludeLaunchDescription(gazebo_rosPackageLaunch)

    spawn_entity = Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                output='screen',
                arguments=['-topic','robot_description','-entity', 'right_arm'],
                emulate_tty=True
                )
    
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )

    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )    


    return LaunchDescription([
        # moveit_demo,
        gazeboLaunch,
        spawn_entity,
        robot_state_publisher_node,
        load_joint_state_broadcaster
        
    ])
