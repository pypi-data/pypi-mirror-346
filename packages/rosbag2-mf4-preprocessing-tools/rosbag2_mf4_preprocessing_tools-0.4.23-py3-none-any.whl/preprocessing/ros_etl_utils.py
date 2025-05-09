# -*- coding: utf-8 -*-
import os
import pickle
import logging
from typing import Dict, List, Optional, Any, Set, Type, Tuple, Union, Iterable
import importlib
import traceback
import re
import keyword
import time
import sys
from pathlib import Path


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def sanitize_hdf5_identifier(name: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    if sanitized and sanitized[0].isdigit():
        sanitized = "_" + sanitized
    if keyword.iskeyword(sanitized):
        sanitized += "_"
    if not sanitized:
        return "empty_name"
    return sanitized


def get_all_fields(
    typename: str,
    typestore: Any,
    current_prefix: str = "",
    visited: Optional[Set[str]] = None,
) -> List[Tuple[str, str, bool]]:
    task_logger = logging.getLogger(f"{__name__}.get_all_fields")
    if visited is None:
        visited = set()
    if typename in visited:
        return []
    visited.add(typename)
    fields_list = []
    errors_encountered = False
    try:
        if typename not in typestore.types:
            task_logger.warning(f"Type '{typename}' not found in typestore.")
            return []
        msg_def = typestore.get_msgdef(typename)
        field_defs = msg_def.fields
    except AttributeError:
        task_logger.warning(f"Type '{typename}' definition lacks 'fields' attribute.")
        return []
    except KeyError:
        task_logger.warning(f"Type '{typename}' definition not found (KeyError).")
        return []
    except Exception as e:
        task_logger.error(
            f"Error accessing definition for type '{typename}': {e}", exc_info=True
        )
        return []

    if isinstance(field_defs, dict):
        field_iterator = field_defs.items()
    elif isinstance(field_defs, (list, tuple)):
        field_iterator = field_defs
    else:
        task_logger.error(
            f"Unexpected structure for field definitions of type '{typename}': {type(field_defs)}."
        )
        field_iterator = []

    for field_info in field_iterator:
        try:
            field_name, field_type_tuple = field_info
        except (TypeError, ValueError):
            task_logger.warning(
                f"Unexpected element structure in field definitions for type '{typename}': {field_info}. Skipping."
            )
            errors_encountered = True
            continue

        flat_name = f"{current_prefix}{field_name}"
        is_array = False
        element_type_name = None

        try:
            if not isinstance(field_type_tuple, tuple) or len(field_type_tuple) < 2:
                task_logger.warning(
                    f"Unexpected field_type_info format for field '{flat_name}': {field_type_tuple}. Skipping."
                )
                errors_encountered = True
                continue

            node_type_int, type_details = field_type_tuple

            if node_type_int == 1:  # BASE
                if isinstance(type_details, (list, tuple)) and len(type_details) > 0:
                    element_type_name = type_details[0]
                else:
                    task_logger.warning(
                        f"Unexpected type_details format for BASE type: {type_details}. Field: '{flat_name}'. Skipping."
                    )
                    errors_encountered = True
                    continue
                is_array = False
            elif node_type_int == 2:  # NAME
                if isinstance(type_details, str):
                    element_type_name = type_details
                else:
                    task_logger.warning(
                        f"Unexpected type_details format for NAME type: {type_details}. Field: '{flat_name}'. Skipping."
                    )
                    errors_encountered = True
                    continue
                is_array = False
            elif node_type_int == 3 or node_type_int == 4:  # ARRAY or SEQUENCE
                is_array = True
                if not isinstance(type_details, (list, tuple)) or len(type_details) < 1:
                    task_logger.warning(
                        f"Unexpected type_details format for ARRAY/SEQUENCE: {type_details}. Field: '{flat_name}'. Skipping."
                    )
                    errors_encountered = True
                    continue

                element_type_tuple = type_details[0]
                if (
                    not isinstance(element_type_tuple, (list, tuple))
                    or len(element_type_tuple) < 2
                ):
                    task_logger.warning(
                        f"Unexpected element_type_tuple format for ARRAY/SEQUENCE: {element_type_tuple}. Field: '{flat_name}'. Skipping."
                    )
                    errors_encountered = True
                    continue

                element_nodetype_int, element_details = element_type_tuple

                if element_nodetype_int == 1:
                    if (
                        isinstance(element_details, (list, tuple))
                        and len(element_details) > 0
                    ):
                        element_type_name = element_details[0]
                    else:
                        task_logger.warning(
                            f"Unexpected element_details format for ARRAY/SEQUENCE -> BASE: {element_details}. Field: '{flat_name}'. Skipping."
                        )
                        errors_encountered = True
                        continue
                elif element_nodetype_int == 2:
                    if isinstance(element_details, str):
                        element_type_name = element_details
                    else:
                        task_logger.warning(
                            f"Unexpected element_details format for ARRAY/SEQUENCE -> NAME: {element_details}. Field: '{flat_name}'. Skipping."
                        )
                        errors_encountered = True
                        continue
                else:
                    task_logger.warning(
                        f"Nested ARRAY/SEQUENCE of type {element_nodetype_int} not fully handled for field '{flat_name}'. Skipping."
                    )
                    errors_encountered = True
                    continue
            else:
                task_logger.warning(
                    f"Unhandled node type integer '{node_type_int}' for field '{flat_name}'. Skipping."
                )
                errors_encountered = True
                continue

        except (IndexError, ValueError, TypeError) as parse_err:
            task_logger.warning(
                f"Error parsing field type tuple for field '{flat_name}' (type: {typename}, info: {field_type_tuple}): {parse_err}. Skipping."
            )
            errors_encountered = True
            continue

        if element_type_name is None:
            task_logger.warning(
                f"Could not determine element type name for field '{field_name}' (type: {typename}, info: {field_type_tuple}). Skipping."
            )
            errors_encountered = True
            continue

        is_complex = False
        if element_type_name in typestore.types:
            try:
                element_msg_def = typestore.get_msgdef(element_type_name)
                if hasattr(element_msg_def, "fields") and element_msg_def.fields:
                    is_complex = True
            except Exception:
                pass

        if is_complex:
            nested_fields = get_all_fields(
                element_type_name, typestore, f"{flat_name}_", visited.copy()
            )
            if nested_fields:
                fields_list.extend(nested_fields)
            elif not is_array: # Add the complex field itself if it's not an array and has no further nested fields (or they were skipped)
                fields_list.append((flat_name, element_type_name, is_array))

        else: # Not a complex type
            fields_list.append((flat_name, element_type_name, is_array))

    if errors_encountered:
        task_logger.info(f"Finished processing fields for type '{typename}' with some warnings. Found {len(fields_list)} valid fields.")
    return fields_list


def parse_external_msg_definitions(
    definition_folders: List[str], venv_logger: logging.Logger
) -> Dict[str, str]:
    all_external_defs: Dict[str, str] = {}
    files_processed = 0
    parse_errors = 0

    if not definition_folders:
        venv_logger.info("No external definition folders provided to parse.")
        return {}

    for folder_path_str in definition_folders:
        base_path = Path(folder_path_str)
        if not base_path.is_dir():
            venv_logger.warning(
                f"Provided definition path is not a directory, skipping: {folder_path_str}"
            )
            continue

        try:
            msg_files = list(base_path.rglob("*.msg")) + \
                        list(base_path.rglob("*.srv")) + \
                        list(base_path.rglob("*.action"))
        except OSError as e:
            venv_logger.error(
                f"Error scanning directory {base_path}: {e}. Skipping this path."
            )
            continue

        for def_file_path in msg_files:
            files_processed += 1
            try:
                relative_path = def_file_path.relative_to(base_path)
                parts = list(relative_path.parts)

                pkg_name = parts[0] if parts else None
                if not pkg_name:
                    venv_logger.warning(f"Could not determine package name from path: {def_file_path}. Skipping.")
                    continue

                type_stem = def_file_path.stem
                type_category = None
                if len(parts) > 1:
                    parent_dir = parts[-2]
                    if parent_dir in ("msg", "srv", "action"):
                        type_category = parent_dir
                    elif parent_dir in ("Goal", "Result", "Feedback") and len(parts) > 2 and parts[-3] == "action":
                        type_category = "action"
                        type_stem = f"{type_stem}_{parent_dir}"
                        parts.pop(-2)

                if type_category is None:
                    if def_file_path.suffix == ".msg": type_category = "msg"
                    elif def_file_path.suffix == ".srv": type_category = "srv"
                    elif def_file_path.suffix == ".action": type_category = "action"

                if not type_category:
                    venv_logger.warning(f"Could not determine type category (msg/srv/action) for: {def_file_path}. Skipping.")
                    continue

                ros_type_name = f"{pkg_name}/{type_category}/{type_stem}"
                content = def_file_path.read_text(encoding="utf-8")

                if ros_type_name in all_external_defs:
                    venv_logger.warning(
                        f"Duplicate definition found for type '{ros_type_name}' from file {def_file_path}. Overwriting."
                    )
                all_external_defs[ros_type_name] = content
            except OSError as e:
                venv_logger.error(
                    f"Error reading file {def_file_path}: {e}", exc_info=False
                )
                parse_errors += 1
            except Exception as e:
                venv_logger.error(
                    f"Unexpected error processing {def_file_path}: {e}", exc_info=False
                )
                parse_errors += 1

    venv_logger.info(
        f"Finished scanning external definition folders. Processed {files_processed} files."
    )
    if parse_errors > 0:
        venv_logger.error(
            f"Encountered {parse_errors} errors during external definition reading."
        )
    venv_logger.info(
        f"Collected {len(all_external_defs)} raw type definitions externally."
    )
    return all_external_defs


def get_config(**context) -> Dict[str, Any]:
    params = context["params"]
    config = {
        "input_folder": params["input_folder"],
        "output_folder": params["output_folder"],
        "ros_distro": params.get("ros_distro", "humble"),
        "custom_msg_definition_folders": params.get("custom_msg_definition_folders", [])
        or [],
        "timestamp_hdf5_name": params.get("timestamp_hdf5_name", "timestamp_s"),
    }
    logger.info(
        f"Configuration: Input='{config['input_folder']}', Output='{config['output_folder']}', ROS Distro='{config['ros_distro']}', "
        f"Custom Defs Provided={bool(config['custom_msg_definition_folders'])}, Timestamp HDF5 Name='{config['timestamp_hdf5_name']}'"
    )
    return config


def create_directories(config: Dict[str, Any]) -> Dict[str, Any]:
    input_f = config["input_folder"]
    output_f = config["output_folder"]
    try:
        if not os.path.isdir(input_f):
            logger.warning(f"Input directory {input_f} does not exist. It might be mounted later.")
        os.makedirs(output_f, exist_ok=True)
        logger.info(
            f"Ensured output directory exists: '{output_f}'"
        )
    except OSError as e:
        logger.error(f"Failed to create output directory '{output_f}': {e}", exc_info=True)
        raise
    return config


def load_already_transformed_folders(config: Dict[str, Any]) -> Set[str]:
    pickle_path = os.path.join(config["output_folder"], "processed_rosbags_folders.pkl")
    already_transformed_folders: Set[str] = set()
    if os.path.exists(pickle_path):
        try:
            with open(pickle_path, "rb") as f:
                loaded_data = pickle.load(f)
                if isinstance(loaded_data, set):
                    validated_data = {
                        item for item in loaded_data if isinstance(item, str)
                    }
                    if len(validated_data) != len(loaded_data):
                        logger.warning(
                            f"State file {pickle_path} contained non-string items. Filtering them out."
                        )
                    already_transformed_folders = validated_data
                else:
                    logger.warning(
                        f"State file {pickle_path} did not contain a set. Re-initializing. File content type: {type(loaded_data)}"
                    )
                    try:
                        os.remove(pickle_path)
                        logger.info(f"Removed potentially corrupted state file: {pickle_path}")
                    except OSError as rm_err:
                        logger.error(f"Could not remove corrupted state file {pickle_path}: {rm_err}")
            logger.info(
                f"Loaded {len(already_transformed_folders)} processed folder names from {pickle_path}"
            )
        except (pickle.UnpicklingError, EOFError, TypeError, ValueError, Exception) as e:
            logger.warning(
                f"Error loading state file {pickle_path}: {e}. Assuming empty state and attempting to remove corrupt file."
            )
            try:
                os.remove(pickle_path)
                logger.info(f"Removed potentially corrupted state file: {pickle_path}")
            except OSError as rm_err:
                logger.error(
                    f"Could not remove corrupted state file {pickle_path}: {rm_err}"
                )
    else:
        logger.info(
            f"State file {pickle_path} not found. Assuming no folders processed previously."
        )
    return already_transformed_folders


def find_untransformed_folders(
    config: Dict[str, Any], already_transformed_folders: Set[str]
) -> List[str]:
    input_folder = config["input_folder"]
    non_transformed_folders_list = []
    try:
        if not os.path.isdir(input_folder):
            logger.error(
                f"Input directory not found or is not a directory: {input_folder}"
            )
            return []

        all_potential_folders = [
            os.path.join(input_folder, d)
            for d in os.listdir(input_folder)
            if os.path.isdir(os.path.join(input_folder, d))
        ]

        rosbag_folders_paths = []
        for folder_path in all_potential_folders:
            metadata_path = os.path.join(folder_path, "metadata.yaml")
            if os.path.isfile(metadata_path):
                rosbag_folders_paths.append(folder_path)

        all_found_folder_names = {os.path.basename(p) for p in rosbag_folders_paths}
        non_transformed_folder_names = sorted(
            list(all_found_folder_names - already_transformed_folders)
        )
        non_transformed_folders_list = [
            os.path.join(input_folder, name) for name in non_transformed_folder_names
        ]

        logger.info(
            f"Found {len(all_found_folder_names)} potential rosbag folders. "
            f"{len(already_transformed_folders)} already processed. "
            f"{len(non_transformed_folders_list)} new folders to process."
        )
        if non_transformed_folders_list:
             logger.info(f"Folders to process: {[os.path.basename(p) for p in non_transformed_folders_list[:10]]}{'...' if len(non_transformed_folders_list) > 10 else ''}")


    except FileNotFoundError:
        logger.error(f"Input directory not found during scan: {input_folder}")
        return []
    except OSError as e:
        logger.error(f"Error listing directory {input_folder}: {e}", exc_info=True)
        return []

    return non_transformed_folders_list


def prepare_extract_arguments(
    config: Dict[str, Any], untransformed_folder_paths: List[str]
) -> List[Dict[str, Any]]:
    kwargs_list = [
        {"config": config, "folder_path": folder_path}
        for folder_path in untransformed_folder_paths
    ]
    logger.info(
        f"Prepared {len(kwargs_list)} arguments for extraction tasks."
    )
    return kwargs_list


def extract(config: Dict[str, Any], folder_path: str) -> Optional[Dict[str, Any]]:
    import os
    import logging
    import numpy as np
    import sys
    import time
    from pathlib import Path
    import pickle

    from rosbags.highlevel import AnyReader
    from rosbags.typesys import Stores, get_typestore, get_types_from_msg
    from rosbags.serde import deserialize_cdr

    try:
        from preprocessing.ros_etl_utils import (
            sanitize_hdf5_identifier,
            parse_external_msg_definitions,
            get_all_fields,
        )
    except ImportError:
        logging.error("Could not import helper functions within the virtualenv for extract. Ensure preprocessing_package is installed or path is correct.")
        raise

    venv_logger = logging.getLogger(f"{__name__}.extract_venv")
    output_folder = config["output_folder"]
    ros_distro = config.get("ros_distro", "humble")
    custom_msg_definition_folders = config.get("custom_msg_definition_folders", [])

    folder_name = os.path.basename(folder_path)
    safe_folder_name = sanitize_hdf5_identifier(folder_name)
    output_hdf5_filename = f"{safe_folder_name}.h5"
    output_hdf5_path = os.path.join(output_folder, output_hdf5_filename)
    intermediate_data_filename = f"{safe_folder_name}_extracted_data.pkl"
    intermediate_data_path = os.path.join(output_folder, intermediate_data_filename)

    if not os.path.isdir(folder_path):
        venv_logger.error(f"Input folder not found or not a directory: {folder_path}")
        return {"status": "failed_input_missing", "input_folder_path": folder_path}

    try:
        typestore_enum = getattr(Stores, f"ROS2_{ros_distro.upper()}", None)
        if typestore_enum is None:
            venv_logger.error(
                f"Invalid ROS distro '{ros_distro}'. Falling back to ROS2_HUMBLE."
            )
            typestore_enum = Stores.ROS2_HUMBLE
        typestore = get_typestore(typestore_enum)

        if custom_msg_definition_folders:
            external_type_defs = parse_external_msg_definitions(
                custom_msg_definition_folders, venv_logger
            )
            if external_type_defs:
                types_to_register = {}
                registration_errors = 0
                for type_name, type_def_str in external_type_defs.items():
                    try:
                        parsed_types = get_types_from_msg(type_def_str, type_name)
                        types_to_register.update(parsed_types)
                    except Exception as e:
                        venv_logger.error(f"Error processing definition for '{type_name}': {e}")
                        registration_errors += 1
                if registration_errors > 0:
                     venv_logger.error(f"Encountered {registration_errors} errors during parsing of external definitions.")
                if types_to_register:
                    typestore.register(types_to_register)
                elif registration_errors == 0:
                     venv_logger.warning("No valid types could be parsed from external definitions.")
    except Exception as e:
        venv_logger.error(f"Error initializing typestore or loading external types for {folder_path}: {e}", exc_info=True)
        return {"status": "failed_typestore_init", "input_folder_path": folder_path}

    extracted_data_by_topic: Dict[str, Dict[str, Any]] = {}
    msgtypes: Dict[str, str] = {}
    fields_by_topic: Dict[str, List[Tuple[str, str, bool]]] = {}
    unreadable_topics: Set[str] = set()
    start_time = time.time()

    try:
        bag_path = Path(folder_path)
        with AnyReader([bag_path], default_typestore=typestore) as reader:
            total_messages_expected = reader.message_count
            for conn in reader.connections:
                topic = conn.topic
                msgtype = conn.msgtype
                if topic not in extracted_data_by_topic:
                    if msgtype not in typestore.types:
                        msgdef_in_bag = getattr(conn, "msgdef", None)
                        if msgdef_in_bag:
                            try:
                                parsed_types = get_types_from_msg(msgdef_in_bag, msgtype)
                                typestore.register(parsed_types)
                                if msgtype not in typestore.types:
                                    venv_logger.error(f"Registration of '{msgtype}' from bag definition failed for topic '{topic}'.")
                                    unreadable_topics.add(topic)
                                    continue
                            except Exception as parse_reg_err:
                                venv_logger.error(f"Failed to parse/register definition for '{msgtype}' from bag (Topic: '{topic}'): {parse_reg_err}")
                                unreadable_topics.add(topic)
                                continue
                        else:
                            venv_logger.warning(f"Type '{msgtype}' for topic '{topic}' not found and no definition in bag. Skipping topic.")
                            unreadable_topics.add(topic)
                            continue

                    if msgtype not in fields_by_topic:
                        current_fields = get_all_fields(msgtype, typestore)
                        if not current_fields:
                            venv_logger.warning(f"Could not determine fields for '{msgtype}' (Topic: '{topic}'). Skipping topic.")
                            unreadable_topics.add(topic)
                            continue
                        fields_by_topic[msgtype] = current_fields

                    extracted_data_by_topic[topic] = {
                        "timestamps": [],
                        "fields": fields_by_topic[msgtype],
                        "data": {field[0]: [] for field in fields_by_topic[msgtype]},
                    }
                    msgtypes[topic] = msgtype
                elif msgtypes.get(topic) != msgtype:
                    venv_logger.warning(f"Topic '{topic}' has inconsistent message types. Sticking with first.")
                    if msgtype not in typestore.types and msgtype not in fields_by_topic:
                        unreadable_topics.add(topic)

            processed_count = 0
            deserialization_errors = 0
            field_access_errors = 0
            valid_connections = [c for c in reader.connections if c.topic not in unreadable_topics]

            for conn, timestamp_ns, rawdata in reader.messages(connections=valid_connections):
                topic = conn.topic
                msgtype = conn.msgtype
                try:
                    msg = typestore.deserialize_cdr(rawdata, msgtype)
                except Exception:
                    deserialization_errors += 1
                    continue

                extracted_data_by_topic[topic]["timestamps"].append(timestamp_ns / 1e9)
                topic_fields = extracted_data_by_topic[topic]["fields"]
                current_msg_data = {}

                def get_value_recursive(obj: Any, field_path_parts: List[str]):
                    value = obj
                    for i, part in enumerate(field_path_parts):
                        if value is None: return None
                        if isinstance(value, (list, tuple, np.ndarray)):
                            if i == len(field_path_parts) - 1: return value
                            else: return None # Cannot getattr on list elements this way
                        try: value = getattr(value, part)
                        except AttributeError: return None
                    if type(value).__name__ in ('Time', 'Duration') and hasattr(value, 'sec') and hasattr(value, 'nanosec'):
                        return value.sec + value.nanosec * 1e-9
                    return value

                for flat_field_name, _, _ in topic_fields:
                    try:
                        field_path_parts = flat_field_name.split('_')
                        value = get_value_recursive(msg, field_path_parts)
                        current_msg_data[flat_field_name] = value
                    except Exception:
                        current_msg_data[flat_field_name] = None
                        field_access_errors += 1
                for flat_field_name, _, _ in topic_fields:
                    extracted_data_by_topic[topic]["data"][flat_field_name].append(current_msg_data.get(flat_field_name))
                processed_count += 1
            
            if deserialization_errors > 0: venv_logger.warning(f"Folder {folder_path}: Encountered {deserialization_errors} deserialization errors.")
            if field_access_errors > 0: venv_logger.warning(f"Folder {folder_path}: Encountered {field_access_errors} field access errors.")

    except FileNotFoundError as e:
        venv_logger.error(f"Bag folder not found or inaccessible during reading: {folder_path}: {e}")
        return {"status": "failed_bag_read_nf", "input_folder_path": folder_path}
    except ImportError as e:
        venv_logger.critical(f"ImportError during bag reading for {folder_path} (is rosbags installed in venv?): {e}", exc_info=True)
        return {"status": "failed_import_error", "input_folder_path": folder_path}
    except Exception as e:
        venv_logger.error(f"Failed to read or process bag folder {folder_path}: {e}", exc_info=True)
        return {"status": "failed_bag_read_other", "input_folder_path": folder_path}

    final_data_to_return = {}
    for topic, data_dict in extracted_data_by_topic.items():
        if topic in unreadable_topics: continue
        if data_dict.get("timestamps"):
            try:
                data_dict["timestamps"] = np.array(data_dict["timestamps"], dtype=np.float64)
                final_data_to_return[topic] = data_dict
            except Exception as np_err:
                venv_logger.warning(f"Could not convert timestamps to numpy array for topic '{topic}' in {folder_path}. Skipping topic. Error: {np_err}")
                unreadable_topics.add(topic)
        else:
            venv_logger.warning(f"Topic '{topic}' in {folder_path} had no messages or empty timestamps. Excluding.")
            unreadable_topics.add(topic)

    total_time = time.time() - start_time
    
    if not final_data_to_return:
        venv_logger.error(f"No data successfully extracted for any topic in {folder_path}. Total time: {total_time:.2f}s.")
        return {"status": "failed_no_data", "input_folder_path": folder_path}

    try:
        os.makedirs(os.path.dirname(intermediate_data_path), exist_ok=True)
        with open(intermediate_data_path, 'wb') as f:
            pickle.dump(final_data_to_return, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        venv_logger.error(f"Failed to save intermediate data to {intermediate_data_path} for {folder_path}: {e}", exc_info=True)
        return {"status": "failed_intermediate_save", "input_folder_path": folder_path, "output_hdf5_path": output_hdf5_path, "msgtypes": msgtypes}

    venv_logger.info(f"Finished extraction for {folder_path}. Processed {processed_count} messages. Extracted {len(final_data_to_return)} topics. Time: {total_time:.2f}s. Intermediate data at: {intermediate_data_path}")
    return {"intermediate_data_path": intermediate_data_path, "input_folder_path": folder_path, "output_hdf5_path": output_hdf5_path, "msgtypes": msgtypes, "status": "success"}


def prepare_transform_arguments(
    config: Dict[str, Any],
    extracted_results: Union[Iterable[Optional[Dict[str, Any]]], List[Optional[Dict[str, Any]]]]
) -> List[Dict[str, Any]]:
    """
    Prepares list of kwargs for dynamic task mapping (transform).
    Filters results based on success status and intermediate file existence.
    Handles iterable input like LazyXComSelect from mapped Airflow tasks.
    """
    # Assuming logger is defined at the module level
    logger = logging.getLogger(f"{__name__}.prepare_transform_arguments")
    kwargs_list = []
    successful_extractions = 0
    skipped_extractions = 0
    total_results_iterated = 0

    if not isinstance(extracted_results, Iterable):
        logger.error(f"Expected an iterable for extracted_results, got {type(extracted_results)}. Returning empty list.")
        return []

    for result in extracted_results: # Iteration handles LazyXComSelect
        total_results_iterated += 1
        if (
            result is not None
            and isinstance(result, dict)
            and result.get("status") == "success"
            and result.get("intermediate_data_path")
        ):
            intermediate_path = result["intermediate_data_path"]
            if os.path.exists(intermediate_path):
                kwargs_list.append({"extracted_metadata": result, "config": config})
                successful_extractions += 1
            else:
                logger.warning(f"Skipping transform: intermediate file {intermediate_path} (from input {result.get('input_folder_path', 'unknown')}) does not exist.")
                skipped_extractions += 1
                output_hdf5 = result.get("output_hdf5_path")
                if output_hdf5 and os.path.exists(output_hdf5):
                    try:
                        os.remove(output_hdf5)
                    except OSError as e:
                        logger.warning(f"Could not remove HDF5 {output_hdf5} during cleanup: {e}")
        else:
            input_path = "unknown"
            status_reason = "result was None, not a dict, or missing critical keys"
            if isinstance(result, dict):
                input_path = result.get("input_folder_path", "unknown")
                if result.get("status") != "success":
                    status_reason = f"status was '{result.get('status', 'missing')}'"
                elif not result.get("intermediate_data_path"):
                    status_reason = "intermediate_data_path key was missing"
            skipped_extractions += 1

    logger.info(
        f"Processed {total_results_iterated} extraction results. "
        f"Prepared {len(kwargs_list)} arguments for transform task "
        f"({successful_extractions} successful, {skipped_extractions} skipped)."
    )
    return kwargs_list


def transform_and_load_single(
    extracted_metadata: Optional[Dict[str, Any]],
    config: Dict[str, Any]
) -> Optional[Dict[str, str]]:
    import logging
    import numpy as np
    import sys
    import time
    import tables
    import os
    import pickle

    try:
        from preprocessing.ros_etl_utils import (
            sanitize_hdf5_identifier,
            save_ros_topics_to_pytables,
        )
    except ImportError:
        logging.error("Could not import helper functions within the virtualenv for transform_and_load_single.")
        raise

    venv_logger = logging.getLogger(f"{__name__}.transform_load_venv")

    if extracted_metadata is None or not isinstance(extracted_metadata, dict):
        venv_logger.warning("Received invalid or no metadata from extraction, skipping transform/load.")
        return {"status": "failed_no_metadata"}

    intermediate_data_path: Optional[str] = extracted_metadata.get("intermediate_data_path")
    output_hdf5_path: Optional[str] = extracted_metadata.get("output_hdf5_path")
    input_folder_path: Optional[str] = extracted_metadata.get("input_folder_path")
    extraction_status: Optional[str] = extracted_metadata.get("status")
    timestamp_hdf5_name: str = config.get("timestamp_hdf5_name", "timestamp_s")
    input_foldername = os.path.basename(input_folder_path) if input_folder_path else "Unknown Folder"

    if extraction_status != "success":
        venv_logger.warning(f"Skipping transform for {input_foldername}, extraction status was '{extraction_status}'.")
        return {"input_foldername": input_foldername, "output_path": output_hdf5_path, "status": f"skipped_due_to_{extraction_status}"}
    if not intermediate_data_path or not output_hdf5_path or not input_folder_path:
        venv_logger.error(f"Missing required paths in metadata for {input_foldername}. Cannot proceed.")
        return {"input_foldername": input_foldername, "output_path": output_hdf5_path, "status": "failed_missing_paths"}

    extracted_data_by_topic: Optional[Dict[str, Dict]] = None
    try:
        if not os.path.exists(intermediate_data_path):
            venv_logger.error(f"Intermediate data file not found for {input_foldername}: {intermediate_data_path}")
            raise FileNotFoundError(f"Intermediate file missing: {intermediate_data_path}")
        with open(intermediate_data_path, 'rb') as f:
            extracted_data_by_topic = pickle.load(f)
    except FileNotFoundError:
        return {"input_foldername": input_foldername, "output_path": output_hdf5_path, "status": "failed_intermediate_missing"}
    except (pickle.UnpicklingError, EOFError, Exception) as e:
        venv_logger.error(f"Failed to load intermediate data from {intermediate_data_path} for {input_foldername}: {e}", exc_info=True)
        try: os.remove(intermediate_data_path)
        except OSError as rm_err: venv_logger.error(f"Could not remove corrupt intermediate file {intermediate_data_path}: {rm_err}")
        return {"input_foldername": input_foldername, "output_path": output_hdf5_path, "status": "failed_intermediate_load"}

    if not extracted_data_by_topic:
        venv_logger.error(f"Loaded intermediate data for {input_foldername} is empty.")
        try: os.remove(intermediate_data_path)
        except OSError as e: venv_logger.warning(f"Could not remove empty intermediate file {intermediate_data_path}: {e}")
        return {"input_foldername": input_foldername, "output_path": output_hdf5_path, "status": "failed_intermediate_empty"}

    data_to_write: Dict[str, Dict[str, Any]] = {}
    preparation_start_time = time.time()
    topics_prepared = 0
    topics_failed_preparation = 0

    for topic_name, topic_data_dict in extracted_data_by_topic.items():
        timestamps: Optional[np.ndarray] = topic_data_dict.get("timestamps")
        field_definitions: Optional[List[Tuple[str, str, bool]]] = topic_data_dict.get("fields")
        data_by_field: Optional[Dict[str, List[Any]]] = topic_data_dict.get("data")

        if timestamps is None or field_definitions is None or data_by_field is None:
            venv_logger.warning(f"Skipping topic '{topic_name}' in {input_foldername} due to incomplete data structure.")
            topics_failed_preparation += 1
            continue
        if not isinstance(timestamps, np.ndarray) or timestamps.ndim != 1:
            venv_logger.warning(f"Skipping topic '{topic_name}' in {input_foldername}: Timestamps not a 1D NumPy array.")
            topics_failed_preparation += 1
            continue
        if timestamps.size == 0:
            continue 

        num_rows = len(timestamps)
        table_fields_pytables = {}
        structured_array_data_input = {}
        valid_fields_count = 0
        table_fields_pytables[timestamp_hdf5_name] = tables.Float64Col(pos=0)
        structured_array_data_input[timestamp_hdf5_name] = timestamps
        col_position = 1

        for flat_field_name, ros_type, is_array in field_definitions:
            col_name_hdf5 = sanitize_hdf5_identifier(flat_field_name)
            if col_name_hdf5 in table_fields_pytables:
                venv_logger.error(f"Sanitized column name collision for '{col_name_hdf5}' (from '{flat_field_name}') in topic '{topic_name}', {input_foldername}. Skipping field.")
                continue
            raw_data_list = data_by_field.get(flat_field_name)
            if raw_data_list is None or len(raw_data_list) != num_rows:
                venv_logger.warning(f"Data missing or length mismatch for field '{flat_field_name}' in topic '{topic_name}', {input_foldername}. Skipping field.")
                continue
            
            col_type_pytables = None
            col_options = {"pos": col_position}
            final_data_for_col = None
            try:
                if is_array:
                    object_array = np.array(raw_data_list, dtype=object)
                    first_elem = next((item for row in object_array for item in np.atleast_1d(row) if item is not None), None)
                    first_row_elem = next((row for row in object_array if row is not None), None)
                    base_shape = np.shape(first_row_elem) if first_row_elem is not None else (1,)

                    if first_elem is None: target_dtype = np.float64
                    elif isinstance(first_elem, (int, np.integer)): target_dtype = np.int64
                    elif isinstance(first_elem, (float, np.floating)): target_dtype = np.float64
                    elif isinstance(first_elem, (bool, np.bool_)): target_dtype = np.bool_
                    elif isinstance(first_elem, (str, bytes)): target_dtype = object
                    else:
                        venv_logger.warning(f"Field '{flat_field_name}' in {input_foldername} is array of unsupported type '{type(first_elem)}'. Skipping.")
                        continue
                    
                    if target_dtype != object:
                        converted_array_list = []
                        default_val = np.nan if target_dtype == np.float64 else 0
                        for i, row_data in enumerate(object_array):
                            if row_data is None:
                                converted_row = np.full(base_shape, default_val, dtype=target_dtype)
                            else:
                                try:
                                    converted_row = np.asarray(row_data, dtype=target_dtype)
                                    if converted_row.shape != base_shape:
                                        padded_row = np.full(base_shape, default_val, dtype=target_dtype)
                                        src_slice = tuple(slice(0, min(s1, s2)) for s1, s2 in zip(base_shape, converted_row.shape))
                                        try: padded_row[src_slice] = converted_row[src_slice]; converted_row = padded_row
                                        except Exception: converted_row = np.full(base_shape, default_val, dtype=target_dtype)
                                except Exception: converted_row = np.full(base_shape, default_val, dtype=target_dtype)
                            converted_array_list.append(converted_row)
                        try:
                            final_data_for_col = np.stack(converted_array_list, axis=0)
                            if final_data_for_col.shape[1:] != base_shape: raise ValueError("Shape mismatch after stack")
                            col_options["shape"] = base_shape
                        except Exception as stack_err:
                            venv_logger.warning(f"Could not stack array for field '{flat_field_name}' in {input_foldername}. Skipping. Error: {stack_err}")
                            continue
                    else: # String/bytes array
                        max_len = max((len(s) for row in object_array if row is not None for s in np.atleast_1d(row) if isinstance(s, (str, bytes))), default=1)
                        col_type_pytables = tables.StringCol
                        col_options["itemsize"] = max_len
                        col_options["shape"] = base_shape
                        final_data_for_col = np.empty((num_rows,) + base_shape, dtype=f'S{max_len}')
                        for i, row_data in enumerate(object_array):
                            if row_data is None: final_data_for_col[i] = np.full(base_shape, b'', dtype=f'S{max_len}')
                            else:
                                try:
                                    row_array_iter = np.atleast_1d(row_data)
                                    encoded_row = np.array([(s.encode('utf-8', 'replace')[:max_len] if isinstance(s, str) else (s[:max_len] if isinstance(s, bytes) else b'')) for s in row_array_iter], dtype=f'S{max_len}')
                                    if encoded_row.shape != base_shape:
                                        padded_row = np.full(base_shape, b'', dtype=f'S{max_len}')
                                        src_slice = tuple(slice(0, min(s1, s2)) for s1, s2 in zip(base_shape, encoded_row.shape))
                                        try: padded_row[src_slice] = encoded_row[src_slice]; final_data_for_col[i] = padded_row
                                        except Exception: final_data_for_col[i] = np.full(base_shape, b'', dtype=f'S{max_len}')
                                    else: final_data_for_col[i] = encoded_row
                                except Exception: final_data_for_col[i] = np.full(base_shape, b'', dtype=f'S{max_len}')
                else: # Scalar
                    np_array = np.array(raw_data_list, dtype=object)
                    first_val = next((x for x in np_array if x is not None), None)
                    if first_val is None: final_data_for_col = np.full(num_rows, np.nan, dtype=np.float64)
                    elif isinstance(first_val, str):
                        max_len = max((len(s) for s in np_array if isinstance(s, str)), default=1)
                        col_type_pytables = tables.StringCol; col_options['itemsize'] = max_len
                        final_data_for_col = np.array([(s.encode('utf-8', 'replace')[:max_len] if isinstance(s, str) else b'') for s in np_array], dtype=f'S{max_len}')
                    elif isinstance(first_val, bytes):
                        max_len = max((len(b) for b in np_array if isinstance(b, bytes)), default=1)
                        col_type_pytables = tables.StringCol; col_options['itemsize'] = max_len
                        final_data_for_col = np.array([(b[:max_len] if isinstance(b, bytes) else b'') for b in np_array], dtype=f'S{max_len}')
                    elif isinstance(first_val, bool): final_data_for_col = np.array([(x if isinstance(x, bool) else False) for x in np_array], dtype=np.bool_)
                    elif isinstance(first_val, int): final_data_for_col = np.array([(int(x) if x is not None else 0) for x in np_array], dtype=np.int64)
                    elif isinstance(first_val, float): final_data_for_col = np.array([(float(x) if x is not None else np.nan) for x in np_array], dtype=np.float64)
                    else:
                        venv_logger.warning(f"Field '{flat_field_name}' in {input_foldername} has unsupported scalar type '{type(first_val)}'. Skipping.")
                        continue
                
                if col_type_pytables is None and final_data_for_col is not None:
                    kind = final_data_for_col.dtype.kind
                    if kind == 'i': col_type_pytables = tables.Int64Col
                    elif kind == 'u': col_type_pytables = tables.UInt64Col
                    elif kind == 'f': col_type_pytables = tables.Float64Col
                    elif kind == 'b': col_type_pytables = tables.BoolCol
                    elif kind == 'S': col_type_pytables = tables.StringCol; col_options['itemsize'] = final_data_for_col.dtype.itemsize
                
                if col_type_pytables and final_data_for_col is not None:
                    table_fields_pytables[col_name_hdf5] = col_type_pytables(**col_options)
                    structured_array_data_input[col_name_hdf5] = final_data_for_col
                    valid_fields_count += 1; col_position += 1
                else:
                    venv_logger.warning(f"Could not determine PyTables type or data for field '{flat_field_name}' in {input_foldername}. Skipping.")
            except Exception as field_prep_err:
                venv_logger.error(f"Error preparing field '{flat_field_name}' in {input_foldername}: {field_prep_err}", exc_info=True)
                continue
        
        if valid_fields_count == 0 and timestamp_hdf5_name not in table_fields_pytables:
             topics_failed_preparation += 1; continue
        elif valid_fields_count == 0 : # Timestamp only
             if timestamp_hdf5_name not in table_fields_pytables: table_fields_pytables[timestamp_hdf5_name] = tables.Float64Col(pos=0)
             if timestamp_hdf5_name not in structured_array_data_input: structured_array_data_input[timestamp_hdf5_name] = timestamps


        try:
            desc_name = f"TopicDesc_{sanitize_hdf5_identifier(topic_name)}"
            valid_py_names = {sanitize_hdf5_identifier(k): v for k, v in table_fields_pytables.items()}
            TopicTableDesc = type(desc_name, (tables.IsDescription,), valid_py_names)
            table_dtype = TopicTableDesc.columns
            structured_array = np.empty(num_rows, dtype=table_dtype)
            for hdf5_col_name in table_dtype.names:
                if hdf5_col_name in structured_array_data_input:
                    try: structured_array[hdf5_col_name] = structured_array_data_input[hdf5_col_name]
                    except (ValueError, TypeError) as assign_err:
                        venv_logger.error(f"Error assigning data for column '{hdf5_col_name}' (Topic: {topic_name}, {input_foldername}): {assign_err}. Using default.")
                        # Try to assign default
                        col_dtype_kind = table_dtype[hdf5_col_name].kind
                        default_val = 0 if col_dtype_kind in 'iub' else (0.0 if col_dtype_kind == 'f' else (b'' if col_dtype_kind == 'S' else None))
                        if default_val is not None:
                            try: structured_array[hdf5_col_name] = default_val
                            except Exception: pass
                else: # Should not happen if logic is correct
                    venv_logger.warning(f"Column '{hdf5_col_name}' in PyTables desc but not in prepared data for '{topic_name}', {input_foldername}.")


            hdf5_topic_path = "/" + "/".join(sanitize_hdf5_identifier(part) for part in topic_name.strip("/").split("/") if part)
            if not hdf5_topic_path or hdf5_topic_path == "/": hdf5_topic_path = f"/topic_{sanitize_hdf5_identifier(topic_name)}"
            if hdf5_topic_path in data_to_write:
                venv_logger.error(f"HDF5 path collision for '{hdf5_topic_path}' from topic '{topic_name}', {input_foldername}. Skipping.")
                topics_failed_preparation += 1; continue
            data_to_write[hdf5_topic_path] = {"description": TopicTableDesc, "data": structured_array}
            topics_prepared += 1
        except Exception as e:
            venv_logger.error(f"Failed structured array/description creation for topic '{topic_name}', {input_foldername}: {e}", exc_info=True)
            topics_failed_preparation += 1; continue

    preparation_time = time.time() - preparation_start_time
    if topics_failed_preparation > 0:
        venv_logger.warning(f"Failed to prepare data for {topics_failed_preparation} topics for {input_foldername}.")
    if not data_to_write:
        venv_logger.error(f"No topics prepared for writing for {input_foldername}. Intermediate file: {intermediate_data_path}")
        try: os.remove(intermediate_data_path)
        except OSError as e: venv_logger.warning(f"Could not remove intermediate file {intermediate_data_path}: {e}")
        return {"input_foldername": input_foldername, "output_path": output_hdf5_path, "status": "failed_prepare"}

    write_success = False
    final_status = "failed_write_unknown"
    try:
        write_success = save_ros_topics_to_pytables(output_hdf5_path, data_to_write)
        if write_success: final_status = "success"
        else:
            venv_logger.error(f"HDF5 writer reported FAILURE for {input_foldername} to {output_hdf5_path}.")
            final_status = "failed_write_reported"
    except Exception as writer_e:
        venv_logger.critical(f"HDF5 writer raised exception for {input_foldername} to {output_hdf5_path}: {writer_e}", exc_info=True)
        final_status = "failed_write_exception"
        if os.path.exists(output_hdf5_path):
            try: os.remove(output_hdf5_path)
            except OSError as rm_err: venv_logger.error(f"Failed to remove corrupted HDF5 {output_hdf5_path}: {rm_err}")

    if intermediate_data_path and os.path.exists(intermediate_data_path):
        try: os.remove(intermediate_data_path)
        except OSError as e: venv_logger.warning(f"Could not remove intermediate data file {intermediate_data_path} for {input_foldername}: {e}")

    venv_logger.info(f"Finished transform and load for {input_foldername}. Output: {output_hdf5_path}. Status: {final_status}. Topics prepared: {topics_prepared}. Prep time: {preparation_time:.2f}s.")
    return {"input_foldername": input_foldername, "output_path": output_hdf5_path, "status": final_status}


def save_ros_topics_to_pytables(
    output_hdf5_path: str, data_by_hdf5_path: Dict[str, Dict[str, Any]]
) -> bool:
    import tables
    import numpy as np
    import os
    import logging

    writer_logger = logging.getLogger(f"{__name__}.save_pytables_data")
    output_dir = os.path.dirname(output_hdf5_path)
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        writer_logger.error(f"Failed to ensure output directory {output_dir} for {output_hdf5_path}: {e}", exc_info=True)
        return False

    h5file = None
    topics_written = 0
    topics_failed = 0
    try:
        h5file = tables.open_file(output_hdf5_path, mode="w", title="Processed ROS Bag Data")
        filters = tables.Filters(complib="zlib", complevel=5)

        for hdf5_path, table_content in data_by_hdf5_path.items():
            description_class = table_content.get("description")
            structured_data = table_content.get("data")
            table_title = f"Data for {hdf5_path.replace('/', '_')}"

            if description_class is None or structured_data is None or \
               not (isinstance(description_class, type) and issubclass(description_class, tables.IsDescription)) or \
               not isinstance(structured_data, np.ndarray):
                writer_logger.warning(f"Skipping HDF5 path '{hdf5_path}' due to invalid description or data.")
                topics_failed += 1; continue
            if structured_data.dtype.names != description_class.columns.keys():
                 writer_logger.warning(f"Mismatch in dtype names vs PyTables keys for '{hdf5_path}'. Writing may fail.")

            try:
                if not hdf5_path.startswith("/"): hdf5_path = "/" + hdf5_path
                parent_group_path, table_name = os.path.split(hdf5_path)
                if not parent_group_path: parent_group_path = "/"
                
                parent_node = h5file.create_group(h5file.root, parent_group_path.lstrip('/'), title=f"Group for {parent_group_path}", createparents=True)
                if table_name in parent_node:
                    writer_logger.error(f"Node '{table_name}' already exists in group '{parent_node._v_pathname}' for HDF5 path: {hdf5_path}. Skipping.")
                    topics_failed += 1; continue

                data_table = h5file.create_table(
                    where=parent_node, name=table_name,
                    description=description_class, title=table_title, filters=filters,
                    expectedrows=(len(structured_data) if len(structured_data) > 0 else 1000)
                )
                if len(structured_data) > 0:
                    data_table.append(structured_data)
                    data_table.flush()
                topics_written += 1
            except tables.exceptions.NodeError as ne:
                writer_logger.error(f"PyTables NodeError for HDF5 path '{hdf5_path}': {ne}. Skipping.", exc_info=True)
                topics_failed += 1; continue
            except Exception as node_create_e:
                writer_logger.error(f"Failed group/table creation/writing for HDF5 path '{hdf5_path}': {node_create_e}", exc_info=True)
                topics_failed += 1; continue
        
        writer_logger.info(f"PyTables writing summary for {output_hdf5_path}: {topics_written} written, {topics_failed} failed out of {len(data_by_hdf5_path)}.")
        return topics_failed == 0
    except tables.exceptions.HDF5ExtError as hdf5_err:
        writer_logger.error(f"PyTables HDF5 Error for file {output_hdf5_path}: {hdf5_err}", exc_info=True)
        return False
    except OSError as os_err:
        writer_logger.error(f"OS Error for file {output_hdf5_path}: {os_err}", exc_info=True)
        return False
    except Exception as e:
        writer_logger.error(f"Unexpected error during PyTables write for {output_hdf5_path}: {e}", exc_info=True)
        return False
    finally:
        if h5file is not None and h5file.isopen:
            try: h5file.close()
            except Exception as close_err: writer_logger.error(f"Error closing HDF5 file {output_hdf5_path}: {close_err}", exc_info=True)


def log_processed_folders(
    config: Dict[str, Any],
    processed_results: List[Optional[Dict[str, str]]],
    previously_transformed_folders: Set[str],
) -> Set[str]:
    if not isinstance(processed_results, list):
        logger.error(f"Expected list for processed_results, got {type(processed_results)}. Cannot log state.")
        return previously_transformed_folders

    successfully_processed_info = [
        item for item in processed_results
        if item is not None and isinstance(item, dict) and "input_foldername" in item and item.get("status") == "success"
    ]

    if not successfully_processed_info:
        logger.info("No new folders successfully processed and loaded in this run.")
        return previously_transformed_folders

    pickle_path = os.path.join(config["output_folder"], "processed_rosbags_folders.pkl")
    newly_processed_foldernames = {info["input_foldername"] for info in successfully_processed_info if info.get("input_foldername")}

    if not newly_processed_foldernames:
        logger.info("Successful transform results found, but no valid folder names to log.")
        return previously_transformed_folders

    updated_folders_set = previously_transformed_folders.union(newly_processed_foldernames)

    try:
        os.makedirs(config["output_folder"], exist_ok=True)
        with open(pickle_path, "wb") as f:
            pickle.dump(updated_folders_set, f, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info(
            f"Logged {len(newly_processed_foldernames)} newly processed folders. State log at {pickle_path}. Total processed: {len(updated_folders_set)}"
        )
    except Exception as e:
        logger.critical(f"CRITICAL: Failed to write state file {pickle_path}: {e}", exc_info=True)
    return updated_folders_set