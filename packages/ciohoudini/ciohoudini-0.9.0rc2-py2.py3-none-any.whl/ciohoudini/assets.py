import hou
import pxr.UsdUtils
import re
import os
from ciopath.gpath_list import PathList, GLOBBABLE_REGEX
from ciopath.gpath import Path
from ciohoudini import common

import ciocore.loggeria

logger = ciocore.loggeria.get_conductor_logger()

ADDITIONAL_PATH_PARMS = {
    # === LOPs (Solaris/USD) ===
    'Lop/reference::2.0': ('filepath1',),
    'Lop/usdrender_rop': ('lopoutput',),
    'Lop/layer': ('filepath',),
    'Lop/sublayer': ('filepath',),
    'Lop/payload': ('filepath',),
    'Lop/materiallibrary': ('filepath',),
    'Lop/file': ('filepath',),

    # === SOPs (Geometry / FX / Volumes) ===
    'Sop/file': ('file',),
    'Sop/alembic': ('fileName',),
    'Sop/vm_geo_alembic': ('attribfile',),
    'Sop/attribfrommap': ('file',),
    'Sop/volume': ('file',),
    'Sop/mdd': ('file',),
    'Sop/heightfield_file': ('file',),
    'Sop/pointcloudiso': ('file',),
    'Sop/bgeo': ('file',),
    'Sop/hfile': ('file',),
    'Sop/image': ('filename',),
    'Sop/trace': ('input',),
    'Sop/lineart': ('image',),
    'Sop/pic': ('filename',),

    # === SHOPs / MATs / VOPs (Shading & Lighting) ===
    'Shop/arnold_image': ('filename',),
    'Vop/arnold::image': ('filename',),
    'Shop/arnold_light': ('filename',),
    'Light/arnold_light': ('filename',),
    'Vop/texture': ('map',),
    'Vop/v_texture': ('map',),
    'Light/envlight': ('env_map',),
    'Vop/materialx/mtlximage': ('file',),
    'Vop/arnold::procedural': ('filename',),
    'Vop/arnold::volume': ('filename',),
    'Shop/pxrtexture': ('filename',),
    'Vop/pxrTexture': ('filename',),

    # === Redshift ===
    'Vop/redshift::TextureSampler': ('tex0', 'tex1', 'tex2', 'tex3'),
    'Light/redshift_lightDome': ('tex0',),
    'Light/redshift_IES': ('profile',),
    'Object/redshift_proxy': ('fileName',),
    'Sop/redshift_volume': ('fileName',),

    # === Karma ===
    'Light/karmadomelight::1.0': ('texture',),

    # === ROPs / Drivers ===
    'Driver/geometry': ('sopoutput',),
    'Driver/alembic': ('filename',),
    'Driver/filmboxfbx': ('output',),
    'Driver/mantra': ('vm_picture', 'vm_deepresolver_file'),
    'Driver/usd': ('usdoutput',),
    'Driver/karma': ('picture',),
    'Driver/Redshift_ROP': ('RS_outputFileNamePrefix',),
    'Driver/ifd': ('vm_picture',),
    'Driver/rop_vdbsequence': ('vdb_file_path',),

    # === COPs (Compositing) ===
    'Cop/file': ('filename',),
    'Cop/rop_file_output': ('copoutput',),
    'Cop/composite': ('inputfile',),
    'Cop/generate_thumbnail': ('thumbnail_path',),

    # === CHOPs (Channel / Audio) ===
    'Chop/file': ('file',),
    'Chop/sound': ('file',),
    'Chop/record': ('filename',),
}


def resolve_payload(node, **kwargs):
    """
    Resolve the upload_paths field for the payload.
    """
    path_list = PathList()
    path_list.add(*auxiliary_paths(node))
    path_list.add(*extra_paths(node))

    do_asset_scan = kwargs.get("do_asset_scan", False)
    if do_asset_scan:
        path_list.add(*scan_paths(node))

    expanded_path = expand_env_vars(node.parm('output_folder').eval())
    output_folder = Path(expanded_path)

    current_assets = []
    seen = set()

    for path in path_list:
        path = str(path).replace("\\", "/")
        normalized = path.lower()
        if normalized not in seen:
            current_assets.append(path)
            seen.add(normalized)

    filtered_paths = [path for path in current_assets if not is_within_output_folder(path, output_folder)]

    if len(current_assets) > len(filtered_paths):
        node.parm("output_excludes").set(0)

    return {"upload_paths": filtered_paths}


def is_within_output_folder(path, output_folder):
    normalized_path = os.path.normpath(str(path))
    normalized_output_folder = os.path.normpath(str(output_folder))
    return normalized_path.startswith(normalized_output_folder)


def auxiliary_paths(node, **kwargs):
    """
    Add the hip file, the OCIO file, and the render script to the list of assets.
    """
    path_list = PathList()
    try:
        path_list.add(hou.hipFile.path())
        ocio_file = os.environ.get("OCIO")
        if ocio_file:
            path_list.add(os.path.dirname(ocio_file))
        render_script = node.parm("render_script").eval()
        if render_script:
            render_script = "{}[{}]".format(render_script[:-1], render_script[-1])
            path_list.add(render_script)
        if path_list:
            path_list = _resolve_absolute_existing_paths(path_list)
        exclude_pattern = node.parm("asset_excludes").unexpandedString()
        if exclude_pattern:
            path_list.remove_pattern(exclude_pattern)
    except Exception as e:
        logger.error("Error while getting auxiliary paths: %s", e)
    return path_list


def extra_paths(node, **kwargs):
    path_list = PathList()
    try:
        num = node.parm("extra_assets_list").eval()
        for i in range(1, num + 1):
            asset = node.parm("extra_asset_{:d}".format(i)).eval()
            asset = os.path.expandvars(asset)
            if asset:
                path_list.add(asset)
        if path_list:
            path_list = _resolve_absolute_existing_paths(path_list)
    except Exception as e:
        logger.error("Error while getting extra paths: %s", e)
    return path_list


def scan_paths(submitter_node):
    """
    Scans the Houdini scene for assets referenced by various nodes, configured by the submitter node.
    """
    logger.info("=" * 20 + " Starting Asset Scan " + "=" * 20)
    logger.info(f"Submitter Node: {submitter_node.path()}")

    raw_paths = PathList()
    final_resolved_paths = PathList()
    parms_to_scan = []

    try:
        # --- 1. Read configuration ---
        regex_pattern = submitter_node.parm("asset_regex").unexpandedString()
        exclude_pattern = submitter_node.parm("asset_excludes").unexpandedString()

        REGEX = None
        if regex_pattern:
            try:
                REGEX = re.compile(regex_pattern, re.IGNORECASE)
            except re.error as regex_err:
                logger.error(f"Invalid regex pattern '{regex_pattern}': {regex_err}. Regex substitution skipped.",
                             exc_info=True)
        else:
            logger.warning("Asset regex parameter is empty. Regex substitution will be skipped.")

        # --- 2. Gather parameters ---
        try:
            parms_from_refs = _get_file_ref_parms()
            parms_to_scan.extend(parms_from_refs)
            parms_from_additional = _get_additional_file_ref_parms()
            parms_to_scan.extend(parms_from_additional)
            logger.info(f"Found {len(parms_to_scan)} total potential parameters to scan.")
        except Exception as e:
            logger.error(f"Error gathering parameters for asset scan: {e}", exc_info=True)

        # --- 3. Evaluate parameters & Expand Variables ---
        processed_parms = set()
        raw_paths_temp = set()

        for i, parm in enumerate(parms_to_scan):
            if parm is None or parm in processed_parms: continue
            processed_parms.add(parm)
            try:
                evaluated = parm.eval()
                if evaluated and isinstance(evaluated, str):
                    try:
                        expanded_str = hou.expandString(evaluated)
                        if expanded_str:
                            raw_paths_temp.add(expanded_str)
                    except Exception as expand_e:
                        logger.warning(
                            f"Could not expand Houdini vars for path '{evaluated}' from {parm.path()}: {expand_e}. Using original.")
                        raw_paths_temp.add(evaluated)
            except hou.OperationFailed as e:
                logger.warning(f"Could not evaluate parameter {parm.path()}: {e}")
            except Exception as e:
                logger.error(f"Error processing parameter {parm.path()}: {e}", exc_info=True)

        raw_paths = PathList()
        for path_str in raw_paths_temp:
            raw_paths.add(path_str)
        logger.info(f"Collected {len(raw_paths)} unique raw paths after evaluation and expansion.")

        # --- 4. USD Dependency Scanning ---
        usd_dependencies = set()
        if pxr and pxr.UsdUtils:
            for i, file_path_obj in enumerate(list(raw_paths)):
                file_path = str(file_path_obj)
                is_usd = False
                try:
                    if file_path and ('/' in file_path or '\\' in file_path):
                        if os.path.isfile(file_path) and os.path.splitext(file_path)[-1].lower() in (".usd", ".usda",
                                                                                                     ".usdc", ".usdz"):
                            is_usd = True
                except Exception as path_check_e:
                    logger.warning(f"Error checking if path is file for USD scan '{file_path}': {path_check_e}")
                    continue
                if is_usd:
                    try:
                        layers, assets, unresolved = pxr.UsdUtils.ComputeAllDependencies(file_path)
                        for layer in layers:
                            if layer.realPath: usd_dependencies.add(layer.realPath)
                        usd_dependencies.update(set(assets))
                        if unresolved:
                            logger.warning(f"Unresolved USD paths found for {file_path}: {unresolved}")
                    except Exception as usd_e:
                        logger.error(f"Error computing USD dependencies for {file_path}: {usd_e}", exc_info=True)
            original_raw_count = len(raw_paths)
            for dep_path in usd_dependencies:
                raw_paths.add(dep_path)
            if len(raw_paths) > original_raw_count:
                logger.info(
                    f"Added {len(raw_paths) - original_raw_count} unique USD dependencies. Raw path count now: {len(raw_paths)}")
        else:
            logger.warning("pxr.UsdUtils not available. Skipping USD dependency scan.")

        # --- 5. Filter Paths (check_path) ---
        checked_paths = PathList()
        rejected_count = 0
        for i, path_obj in enumerate(raw_paths):
            path_str = str(path_obj)
            if check_path(path_str):
                checked_paths.add(path_obj)
            else:
                rejected_count += 1
                logger.debug(f"Rejected path: {path_str}")
        logger.info(f"Paths remaining after check_path filter: {len(checked_paths)} (Rejected: {rejected_count})")

        # --- 6. Regex Substitution ---
        substituted_paths = PathList()
        if REGEX:
            substitution_count = 0
            for i, path_obj in enumerate(checked_paths):
                path_str = str(path_obj)
                try:
                    pth_sub = REGEX.sub(r"*", path_str)
                    substituted_paths.add(pth_sub)
                    if pth_sub != path_str: substitution_count += 1
                except Exception as sub_e:
                    logger.error(f"Error applying regex substitution to '{path_str}': {sub_e}", exc_info=True)
                    substituted_paths.add(path_str)
            logger.info(
                f"Paths after regex substitution: {len(substituted_paths)} ({substitution_count} substitutions occurred)")
        else:
            substituted_paths = checked_paths

        # --- 7. Resolve Paths (Absolute, Existing, Globbing) ---
        try:
            final_resolved_paths = _resolve_absolute_existing_paths(substituted_paths)
            logger.info(f"Paths remaining after resolving absolute/existing and globbing: {len(final_resolved_paths)}")
        except Exception as e:
            logger.error(f"Error during final path resolution (_resolve_absolute_existing_paths): {e}", exc_info=True)

        # --- 8. Apply Exclude Pattern ---
        if exclude_pattern:
            try:
                original_count = len(final_resolved_paths)
                final_resolved_paths.remove_pattern(exclude_pattern)
                removed_count = original_count - len(final_resolved_paths)
                if removed_count > 0:
                    logger.info(
                        f"Excluded {removed_count} paths based on pattern. Final count: {len(final_resolved_paths)}")
            except Exception as remove_e:
                logger.error(f"Error applying exclude pattern '{exclude_pattern}': {remove_e}", exc_info=True)

    except Exception as e:
        logger.critical(f"CRITICAL: Unhandled error during scan_paths execution: {e}", exc_info=True)
        final_resolved_paths = final_resolved_paths or PathList()

    logger.info("=" * 20 + " Asset Scan Finished " + "=" * 20)
    logger.info(f">>> Found {len(final_resolved_paths)} final asset paths.")
    return final_resolved_paths


def _get_file_ref_parms():
    parms = []
    try:
        refs = hou.fileReferences()
        for parm, ref_path in refs:
            if parm:
                node_type_name = parm.node().type().nameWithCategory()
                if not node_type_name.startswith("conductor::"):
                    parms.append(parm)
    except Exception as e:
        logger.error(f"Error retrieving hou.fileReferences(): {e}", exc_info=True)
    return parms


def _get_additional_file_ref_parms():
    parms = []
    all_categories = hou.nodeTypeCategories()
    try:
        for node_type_key, node_parms_tuple in ADDITIONAL_PATH_PARMS.items():
            node_type_obj = None
            try:
                category_name_str = None
                type_name_with_version = None
                if '/' in node_type_key:
                    parts = node_type_key.split('/', 1)
                    category_name_str = parts[0]
                    type_name_with_version = parts[1]
                else:
                    logger.warning(f"Unexpected format for key '{node_type_key}'. Skipping.")
                    continue
                type_name_base = type_name_with_version.split('::')[0]
                category_obj = all_categories.get(category_name_str)
                if not category_obj:
                    # logger.warning(f"Category '{category_name_str}' not found. Skipping key '{node_type_key}'.")
                    continue
                node_type_obj = hou.nodeType(category_obj, type_name_base)
                if node_type_obj is None:
                    # logger.warning(f"Could not retrieve node type object for key '{node_type_key}'. Skipping.")
                    continue
            except hou.OperationFailed:
                logger.warning(
                    f"Node type '{type_name_base}' not found in category '{category_name_str}' for key '{node_type_key}'. Skipping.")
                continue
            except Exception as type_lookup_e:
                logger.error(f"Error looking up node type for key '{node_type_key}': {type_lookup_e}", exc_info=True)
                continue
            try:
                instances = node_type_obj.instances()
                if not instances:
                    continue
                for node_instance in instances:
                    for parm_name in node_parms_tuple:
                        additional_parm = node_instance.parm(parm_name)
                        if additional_parm:
                            parms.append(additional_parm)
            except Exception as instance_e:
                logger.error(
                    f"Error processing instances of node type '{node_type_obj.nameWithCategory()}': {instance_e}",
                    exc_info=True)
    except Exception as e:
        logger.error(f"Unhandled error in _get_additional_file_ref_parms: {e}", exc_info=True)
    return parms


def clear_all_assets(node, **kwargs):
    node.parm("extra_assets_list").set(0)


def browse_files(node, **kwargs):
    files = hou.ui.selectFile(
        title="Browse for files to upload",
        collapse_sequences=True,
        file_type=hou.fileType.Any,
        multiple_select=True,
        chooser_mode=hou.fileChooserMode.Read,
    )
    if not files:
        return
    files = [f.strip() for f in files.split(";") if f.strip()]
    add_entries(node, *files)


def browse_folder(node, **kwargs):
    files = hou.ui.selectFile(title="Browse for folder to upload", file_type=hou.fileType.Directory)
    if not files:
        return
    files = [f.strip() for f in files.split(";") if f.strip()]
    add_entries(node, *files)


def add_entries(node, *entries):
    path_list = PathList()
    try:
        num = node.parm("extra_assets_list").eval()
        for i in range(1, num + 1):
            asset = node.parm("extra_asset_{:d}".format(i)).eval()
            asset = os.path.expandvars(asset)
            if asset:
                path_list.add(asset)
        for entry in entries:
            path_list.add(entry)
        paths = [p.fslash() for p in path_list]
        node.parm("extra_assets_list").set(len(paths))
        for i, arg in enumerate(paths):
            index = i + 1
            node.parm("extra_asset_{:d}".format(index)).set(arg)
    except Exception as e:
        logger.error("Error while adding entries: %s", e)


def remove_asset(node, index):
    try:
        curr_count = node.parm("extra_assets_list").eval()
        for i in range(index + 1, curr_count + 1):
            from_parm = node.parm("extra_asset_{}".format(i))
            to_parm = node.parm("extra_asset_{}".format(i - 1))
            to_parm.set(from_parm.unexpandedString())
        node.parm("extra_assets_list").set(curr_count - 1)
    except Exception as e:
        logger.error("Error while removing asset: %s", e)


def add_hdas(node, **kwargs):
    hda_paths = [hda.libraryFilePath() for hda in common.get_plugin_definitions()]
    if not hda_paths:
        return
    add_entries(node, *hda_paths)


def _resolve_absolute_existing_paths(path_list):
    hip = hou.getenv("HIP")
    job = hou.getenv("JOB")
    internals = ("op:", "temp:")
    resolved = PathList()
    try:
        for path in path_list:
            if path.relative:
                if not path.fslash().startswith(internals):
                    resolved.add(
                        os.path.join(hip, path.fslash()),
                        os.path.join(job, path.fslash()),
                    )
            else:
                resolved.add(path)
        resolved.remove_missing()
        resolved.glob()
    except Exception as e:
        logger.error("Error while resolving absolute existing paths: %s", e)
    return resolved


def expand_env_vars(path):
    return os.path.expandvars(path)


def check_path(file_path):
    if not file_path:
        return False
    file_path = file_path.replace("\\", "/")
    if "*" in file_path:
        logger.debug(f"Rejected path (contains wildcard): {file_path}")
        return False
    if file_path.startswith("/tmp/"):
        logger.debug(f"Rejected path (temporary file): {file_path}")
        return False
    if "houdini_temp" in file_path:
        logger.debug(f"Rejected path (Houdini temp): {file_path}")
        return False
    try:
        hip_folder = hou.getenv("HIP")
        if hip_folder:
            normalized_file_path = os.path.normpath(os.path.abspath(file_path))
            normalized_hip_folder = os.path.normpath(os.path.abspath(hip_folder))
            if normalized_file_path == normalized_hip_folder:
                logger.debug(f"Rejected path (HIP folder): {file_path}")
                return False
    except Exception as e:
        logger.warning(f"Could not check if path is HIP folder due to error: {e}")
    return True