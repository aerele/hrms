from datetime import datetime, time

import frappe


@frappe.whitelist()
def get_next_checkin_action(employee):
	now = frappe.utils.now_datetime().time()

	shift = frappe.db.get_value(
		"Shift Assignment",
		{"employee": employee},
		["start_time", "end_time"],
		as_dict=True,
		order_by="creation desc",
	)

	if not shift:
		return {"action": "IN"}

	start_time = shift.start_time
	end_time = shift.end_time

	last_log = frappe.db.get_value(
		"Employee Checkin", {"employee": employee}, ["log_type", "time"], as_dict=True, order_by="time desc"
	)

	if last_log:
		last_type = last_log.log_type

	if now > end_time:
		return {"action": "OUT"}

	if now < start_time:
		return {"action": "IN"}

	if not last_log:
		return {"action": "IN"}

	if start_time <= now <= end_time and last_type == "IN":
		return {"action": "OUT"}

	if start_time <= now <= end_time and last_type == "OUT":
		return {"action": "IN"}

	return {"action": "IN"}
