
import math
from flask import (Blueprint,
                   jsonify,
                   request)

from deepracer_interfaces_pkg.msg import ServoCtrlMsg
from deepracer_interfaces_pkg.srv import (ActiveStateSrv,
                                          EnableStateSrv,
                                          NavThrottleSrv,
                                          GetCtrlModesSrv)
from webserver_pkg import constants
from webserver_pkg.utility import (api_fail,
                                   call_service_sync)
from webserver_pkg import webserver_publisher_node


VEHICLE_CONTROL_BLUEPRINT = Blueprint("vehicle_control", __name__)


def get_rescaled_manual_speed(categorized_throttle, max_speed_pct):
    return categorized_throttle * max_speed_pct


def get_categorized_manual_throttle(throttle):
    return throttle


def get_categorized_manual_angle(angle):
    return angle


@VEHICLE_CONTROL_BLUEPRINT.route("/api/manual_drive", methods=["PUT", "POST"])
def api_manual_drive():
    """API that publishes control messages to control the angle and throttle in
       manual drive mode.

    Returns:
        dict: Execution status if the API call was successful.
    """
    webserver_node = webserver_publisher_node.get_webserver_node()
    angle = request.json.get("angle")
    throttle = request.json.get("throttle")
    max_speed = request.json.get("max_speed")

    if angle is None:
        return api_fail("angle is required")
    if throttle is None:
        return api_fail("throttle is required")
    if max_speed is None:
        return api_fail("max_speed is required")

    if angle < -1.0 or angle > 1.0:
        return api_fail("angle out of range")
    if throttle < -1.0 or throttle > 1.0:
        return api_fail("throttle out of range")

    webserver_node.get_logger().info(f"Angle: {angle}  Throttle: {throttle}")

    # Create the servo message.
    msg = ServoCtrlMsg()
    # bound the throttle value based on the categories defined
    msg.angle = -1.0 * get_categorized_manual_angle(angle)
    categorized_throttle = get_categorized_manual_throttle(throttle)
    msg.throttle = -1.0 * get_rescaled_manual_speed(categorized_throttle, max_speed)
    webserver_node.pub_manual_drive.publish(msg)
    return jsonify({"success": True})


@VEHICLE_CONTROL_BLUEPRINT.route("/api/drive_mode", methods=["PUT", "POST"])
def api_set_drive_mode():
    """API to toggle the drive mode between Autonomous/Manual mode.

    Returns:
        dict: Execution status if the API call was successful and error
              reason if failed.
    """
    webserver_node = webserver_publisher_node.get_webserver_node()
    drive_mode = request.json.get("drive_mode")
    if drive_mode is None:
        return jsonify({"success": False, "reason": "drive_mode must be set."})

    webserver_node.get_logger().info(f"Changed the vehicle state to {drive_mode}")
    drive_mode_state = 0 if drive_mode == "manual" else 1

    try:
        vehicle_state_req = ActiveStateSrv.Request()
        vehicle_state_req.state = drive_mode_state
        vehicle_state_res = call_service_sync(webserver_node.vehicle_state_cli,
                                              vehicle_state_req)
        if vehicle_state_res and (vehicle_state_res.error == 0):
            return jsonify(success=True)
        else:
            webserver_node.get_logger().error("Vehicle state service call failed")
            return jsonify(success=False, reason="Error")

    except Exception as ex:
        webserver_node.get_logger().error(f"Unable to reach vehicle state server: {ex}")
        return jsonify({"success": False,
                        "reason": "Unable to reach vehicle state server."})


@VEHICLE_CONTROL_BLUEPRINT.route("/api/start_stop", methods=["PUT", "POST"])
def api_set_start_stop():
    """API to call the enable_state service to start and stop the vehicle.

    Returns:
        dict: Execution status if the API call was successful and error
              reason if failed.
    """
    webserver_node = webserver_publisher_node.get_webserver_node()
    start_stop = request.json.get("start_stop")
    if start_stop is None:
        return jsonify({"success": False, "reason": "start_stop must be set."})

    webserver_node.get_logger().info(f"Changed the enable state to {start_stop}")
    start_stop_state = False if start_stop == "stop" else True
    try:
        enable_state_req = EnableStateSrv.Request()
        enable_state_req.is_active = start_stop_state
        enable_state_res = call_service_sync(webserver_node.enable_state_cli, enable_state_req)
        if enable_state_res and (enable_state_res.error == 0):
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "reason": "Error"})

    except Exception as ex:
        webserver_node.get_logger().error(f"Unable to reach enable state server: {ex}")
        return jsonify({"success": False,
                        "reason": "Unable to reach enable state server."})


@VEHICLE_CONTROL_BLUEPRINT.route("/api/max_nav_throttle", methods=["PUT", "POST"])
def max_nav_throttle():
    """API to call the navigation_throttle service to set the throttle scale in the
       autonomous mode.

    Returns:
        dict: Execution status if the API call was successful and error
              reason if failed.
    """
    webserver_node = webserver_publisher_node.get_webserver_node()
    nav_throttle = request.json.get("throttle")
    if nav_throttle is None:
        return jsonify({"success": False, "reason": "value must be set."})
    webserver_node.get_logger().info(f"Setting max navigation throttle to {nav_throttle}")
    try:
        set_throttle_req = NavThrottleSrv.Request()
        set_throttle_req.throttle = nav_throttle / constants.MAX_AUTO_THROTTLE_VAL
        set_throttle_res = call_service_sync(webserver_node.set_throttle_cli, set_throttle_req)
        if set_throttle_res and (set_throttle_res.error == 0):
            return jsonify({"success": True})
        else:
            return jsonify(success=False, reason="Failed to call the navigation throttle service")
    except Exception as ex:
        webserver_node.get_logger().error(f"Unable to reach navigation throttle server: {ex}")
        return jsonify(success=False, reason="Unable to reach navigation throttle server")


@VEHICLE_CONTROL_BLUEPRINT.route("/api/control_modes_available", methods=["GET"])
def control_modes_available():
    """API to call the GetCtrlModesCountSrv service to get the list of available modes
       in ctrl_pkg (autonomous/manual/calibration).

    Returns:
        dict: Execution status if the API call was successful, list of available modes
              and error reason if call fails.
    """
    webserver_node = webserver_publisher_node.get_webserver_node()
    webserver_node.get_logger().info("Providing the number of available modes")
    try:
        get_ctrl_modes_req = GetCtrlModesSrv.Request()
        get_ctrl_modes_res = call_service_sync(webserver_node.get_ctrl_modes_cli,
                                               get_ctrl_modes_req)

        control_modes_available = list()
        for mode in get_ctrl_modes_res.modes:
            control_modes_available.append(constants.MODE_DICT[mode])

        data = {
            "control_modes_available": control_modes_available,
            "success": True
        }
        return jsonify(data)

    except Exception as ex:
        webserver_node.get_logger().error(f"Unable to reach get ctrl modes service: {ex}")
        return jsonify(success=False, reason="Error")
