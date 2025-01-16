#
# Author: Wonho Yoon, Sungho Woo

import os
import yaml
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro


def generate_launch_description():

    ld = LaunchDescription()

    use_sim = LaunchConfiguration('use_sim')
    declare_use_sim = DeclareLaunchArgument(
        'use_sim',
        default_value='true',
        description='Start robot in Gazebo simulation.')
    ld.add_action(declare_use_sim)

    # Robot description
    robot_description_config = xacro.process_file(
        os.path.join(
            get_package_share_directory("sim"),
            "urdf",
            "open_manipulator_x_robot.urdf.xacro",
        )
    )
    robot_description = {"robot_description": robot_description_config.toxml()}

    # Robot description Semantic config
    robot_description_semantic_path = os.path.join(
        get_package_share_directory("sim"),
        "config",
        "open_manipulator_x.srdf",
    )
    try:
        with open(robot_description_semantic_path, "r") as file:
            robot_description_semantic_config = file.read()
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None

    robot_description_semantic = {
        "robot_description_semantic": robot_description_semantic_config
    }

        # kinematics yaml
    kinematics_yaml_path = os.path.join(
        get_package_share_directory("sim"),
        "config",
        "kinematics.yaml",
    )
    with open(kinematics_yaml_path, "r") as file:
        kinematics_yaml = yaml.safe_load(file)

    # Get parameters for the Servo node
    servo_yaml_path = os.path.join(
        get_package_share_directory("sim"),
        "config",
        "moveit_servo.yaml",
    )
    try:
        with open(servo_yaml_path, "r") as file:
            servo_params = {"moveit_servo": yaml.safe_load(file)}
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None

    # Launch as much as possible in components
    servo_node = Node(
        package="moveit_servo",
        executable="servo_node_main",
        parameters=[
            {'use_gazebo':use_sim},
            servo_params,
            robot_description,
            robot_description_semantic,
            kinematics_yaml,
        ]
    )
    ld.add_action(servo_node)

    return ld 
