---
tags:
  - MASTER/MUSANTTA
  - drones/enjambre/ROS
date: 2026-06-05
---

```
$ ros2 topic list -v
Published topics:
 * /fmu/out/battery_status [px4_msgs/msg/BatteryStatus] 1 publisher
 * /fmu/out/estimator_status_flags [px4_msgs/msg/EstimatorStatusFlags] 1 publisher
 * /fmu/out/failsafe_flags [px4_msgs/msg/FailsafeFlags] 1 publisher
 * /fmu/out/manual_control_setpoint [px4_msgs/msg/ManualControlSetpoint] 1 publisher
 * /fmu/out/position_setpoint_triplet [px4_msgs/msg/PositionSetpointTriplet] 1 publisher
 * /fmu/out/sensor_combined [px4_msgs/msg/SensorCombined] 1 publisher
 * /fmu/out/timesync_status [px4_msgs/msg/TimesyncStatus] 1 publisher
 * /fmu/out/vehicle_attitude [px4_msgs/msg/VehicleAttitude] 1 publisher
 * /fmu/out/vehicle_control_mode [px4_msgs/msg/VehicleControlMode] 1 publisher
 * /fmu/out/vehicle_global_position [px4_msgs/msg/VehicleGlobalPosition] 1 publisher
 * /fmu/out/vehicle_gps_position [px4_msgs/msg/SensorGps] 1 publisher
 * /fmu/out/vehicle_local_position [px4_msgs/msg/VehicleLocalPosition] 1 publisher
 * /fmu/out/vehicle_odometry [px4_msgs/msg/VehicleOdometry] 1 publisher
 * /fmu/out/vehicle_status [px4_msgs/msg/VehicleStatus] 1 publisher
 * /parameter_events [rcl_interfaces/msg/ParameterEvent] 2 publishers
 * /rosout [rcl_interfaces/msg/Log] 2 publishers

Subscribed topics:
 * /fmu/in/actuator_motors [px4_msgs/msg/ActuatorMotors] 1 subscriber
 * /fmu/in/actuator_servos [px4_msgs/msg/ActuatorServos] 1 subscriber
 * /fmu/in/arming_check_reply [px4_msgs/msg/ArmingCheckReply] 1 subscriber
 * /fmu/in/aux_global_position [px4_msgs/msg/VehicleGlobalPosition] 1 subscriber
 * /fmu/in/config_control_setpoints [px4_msgs/msg/VehicleControlMode] 1 subscriber
 * /fmu/in/config_overrides_request [px4_msgs/msg/ConfigOverrides] 1 subscriber
 * /fmu/in/differential_drive_setpoint [px4_msgs/msg/DifferentialDriveSetpoint] 1 subscriber
 * /fmu/in/goto_setpoint [px4_msgs/msg/GotoSetpoint] 1 subscriber
 * /fmu/in/manual_control_input [px4_msgs/msg/ManualControlSetpoint] 1 subscriber
 * /fmu/in/message_format_request [px4_msgs/msg/MessageFormatRequest] 1 subscriber
 * /fmu/in/mode_completed [px4_msgs/msg/ModeCompleted] 1 subscriber
 * /fmu/in/obstacle_distance [px4_msgs/msg/ObstacleDistance] 1 subscriber
 * /fmu/in/offboard_control_mode [px4_msgs/msg/OffboardControlMode] 1 subscriber
 * /fmu/in/onboard_computer_status [px4_msgs/msg/OnboardComputerStatus] 1 subscriber
 * /fmu/in/register_ext_component_request [px4_msgs/msg/RegisterExtComponentRequest] 1 subscriber
 * /fmu/in/sensor_optical_flow [px4_msgs/msg/SensorOpticalFlow] 1 subscriber
 * /fmu/in/telemetry_status [px4_msgs/msg/TelemetryStatus] 1 subscriber
 * /fmu/in/trajectory_setpoint [px4_msgs/msg/TrajectorySetpoint] 1 subscriber
 * /fmu/in/unregister_ext_component [px4_msgs/msg/UnregisterExtComponent] 1 subscriber
 * /fmu/in/vehicle_attitude_setpoint [px4_msgs/msg/VehicleAttitudeSetpoint] 1 subscriber
 * /fmu/in/vehicle_command [px4_msgs/msg/VehicleCommand] 1 subscriber
 * /fmu/in/vehicle_command_mode_executor [px4_msgs/msg/VehicleCommand] 1 subscriber
 * /fmu/in/vehicle_mocap_odometry [px4_msgs/msg/VehicleOdometry] 1 subscriber
 * /fmu/in/vehicle_rates_setpoint [px4_msgs/msg/VehicleRatesSetpoint] 1 subscriber
 * /fmu/in/vehicle_thrust_setpoint [px4_msgs/msg/VehicleThrustSetpoint] 1 subscriber
 * /fmu/in/vehicle_torque_setpoint [px4_msgs/msg/VehicleTorqueSetpoint] 1 subscriber
 * /fmu/in/vehicle_trajectory_bezier [px4_msgs/msg/VehicleTrajectoryBezier] 1 subscriber
 * /fmu/in/vehicle_trajectory_waypoint [px4_msgs/msg/VehicleTrajectoryWaypoint] 1 subscriber
 * /fmu/in/vehicle_visual_odometry [px4_msgs/msg/VehicleOdometry] 1 subscriber

```


```sh title:"Restart topics"
ros2 daemon stop/start
```


```sh
ros2 topic echo /fmu/out/vehicle_status_v4
```


---

``` title:"Ejemplo lectura de topic vehicle status"
ros2 topic echo /fmu/out/vehicle_status_v4

timestamp: 1780750443274110
armed_time: 0
takeoff_time: 0
arming_state: 1
latest_arming_reason: 0
latest_disarming_reason: 0
nav_state_timestamp: 5560000
nav_state_user_intention: 4
nav_state: 4
executor_in_charge: 0
nav_state_display: 4
accepts_offboard_setpoints: false
valid_nav_states_mask: 2147411455
can_set_nav_states_mask: 8308223
hil_state: 0
vehicle_type: 1
failsafe: false
failsafe_and_user_took_over: false
failsafe_defer_state: 0
gcs_connection_lost: true
gcs_connection_lost_counter: 0
high_latency_data_link_lost: false
is_vtol: false
is_vtol_tailsitter: false
in_transition_mode: false
in_transition_to_fw: false
system_type: 2
system_id: 1
component_id: 1
safety_button_available: true
safety_off: true
power_input_valid: true
usb_connected: false
open_drone_id_system_present: false
open_drone_id_system_healthy: false
parachute_system_present: false
parachute_system_healthy: false
traffic_avoidance_system_present: false
rc_calibration_in_progress: false
calibration_enabled: false
pre_flight_checks_pass: false
```

---

```sh
ros2 topic echo /fmu/out/
```


### Armar desde ROS2

```sh title:"Muestra topic de comandos"
ros2 interface show px4_msgs/msg/VehicleCommand
```


```sh title:"Estructura topic para armar"
ros2 topic pub --once /fmu/in/vehicle_command px4_msgs/msg/VehicleCommand "
timestamp: 0
param1: 1.0
param2: 0.0
command: 400
target_system: 1
target_component: 1
source_system: 1
source_component: 1
from_external: true
"
```

> [!failure]  normalmente PX4 rechazará el armado si no estás en modo Offboard o no se cumplen ciertas condiciones

###### Entrar en modo Offboard

mantener un flujo continuo de mensajes.

publicar continuamente:

```
/fmu/in/offboard_control_mode
```

y

```
/fmu/in/trajectory_setpoint
```

a unos 10 Hz o más.

```sh title
ros2 interface show px4_msgs/msg/OffboardControlMode
```

```sh
ros2 interface show px4_msgs/msg/TrajectorySetpoint
```

----

ver: [[]]