import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition

def generate_launch_description():
    # Define package name and URDF file
    package_name = 'simulation'  # Replace with your actual package name
    urdf_file_name = 'open_manipulator_x.urdf'

    # Get the full path to the URDF file
    urdf_file_path = os.path.join(
        get_package_share_directory(package_name),
        'urdf',
        urdf_file_name
    )

    # Declare an argument to conditionally launch RViz
    declare_rviz_arg = DeclareLaunchArgument(
        'rviz',
        default_value='true',
        description='Launch RViz to visualize the robot'
    )

    # Robot State Publisher Node (publishes /robot_description from URDF)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': open(urdf_file_path).read()}]
    )

    # Joint State Publisher GUI (for manual joint movement)
    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
    )

    # RViz Node (optional)
    rviz_config_file = os.path.join(
        get_package_share_directory(package_name),
        'rviz',
        'open_manipulator_x.rviz'
    )
    
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen',
        condition=IfCondition(LaunchConfiguration('rviz'))  # Using IfCondition for evaluation
    )

    return LaunchDescription([
        declare_rviz_arg,
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz_node
    ])
