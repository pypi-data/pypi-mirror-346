import json
import hou

from ciohoudini import (
    job_title,
    project,
    instances,
    software,
    environment,
    driver,
    frames,
    task,
    assets,
    miscellaneous,
    render_rops,
)


def set_stats_panel(node, **kwargs):
    """Update the stats panel.

    Currently, only gets frames info, but will probably get other (non-payload) info like cost
    estimate. Example, when chunk size of frames change value.
    """
    frames.set_stats_panel(node, **kwargs)


def set_preview_panel(node, **kwargs):
    """Update the payload preview panel.

    Payload preview displays the JSON object that is submitted to Conductor. For optimization
    reasons, we don't always do a dependency scan or generate all tasks.

    User can set task_limit to -1 to see all tasks
    if user hits the display_assets button the assets list will include the result of a scan.
    """
    kwargs["task_limit"] = node.parm("display_tasks").eval()
    kwargs["do_asset_scan"] = kwargs.get("parm_name") == "do_asset_scan"

    payload = resolve_payload(node, **kwargs)

    node.parm("payload").set(json.dumps(payload, indent=2))

def refresh_lop_network():
    # Get the LOP Network object
    lop_network = hou.node("/stage")

    # Force a cook to refresh the LOP network
    lop_network.cook(force=True)


def resolve_payload(node, **kwargs):
    # set_stats_panel(node, **kwargs)
    # Get the payload for the current node.
    render_rops_data = render_rops.get_render_rop_data(node)
    if not render_rops_data:
        return None

    # Refresh the LOP network
    refresh_lop_network()

    # Get the payload for each rop.
    payload_list = []
    for render_rop in render_rops_data:
        payload = {}
        rop_path = render_rop.get("path", None)
        frame_range = render_rop.get("frame_range", None)
        kwargs["rop_path"] = rop_path
        kwargs["frame_range"] = frame_range
        kwargs["do_asset_scan"] = True

        # print("rop_path: {}".format(rop_path))
        # print("frame_range: {}".format(frame_range))

        payload.update(job_title.resolve_payload(node, rop_path))
        payload.update(project.resolve_payload(node))
        payload.update(instances.resolve_payload(node))
        payload.update(software.resolve_payload(node))
        payload.update(environment.resolve_payload(node))
        # Get the payload for the driver using the rop path.
        payload.update(render_rops.resolve_payload(node, rop_path))
        payload.update(miscellaneous.resolve_payload(node))
        payload.update(frames.resolve_payload(node, frame_range=frame_range))
        # Get the payload for the assets using the rop path and frame range.
        payload.update(task.resolve_payload(node, **kwargs))
        payload.update(assets.resolve_payload(node, **kwargs))
        payload_list.append(payload)


    return payload_list
