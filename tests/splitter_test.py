import os
import logging
import shutil
from pathlib import Path

import pytest

from constants import TARGET_HOST_1_PATH, TARGET_HOST_2_PATH, INPUT_FILE_DIR, ARTIFACTS_DIR
from file_processing_utils import process_input_files, check_target_host_file_bytes
from file_processing_utils import get_byte_counter


@pytest.fixture(scope="function", autouse=True)
def empty_existing_target_files():
    """
    Delete existing output event logs on shared volume
    """
    if os.path.exists(TARGET_HOST_1_PATH):
        logging.info(f"Found Target host file emptying file before test run at {TARGET_HOST_1_PATH}")
        open(TARGET_HOST_1_PATH, "w").close()

    if os.path.exists(TARGET_HOST_2_PATH):
        logging.info(f"Found Target host files emptying file before test run at {TARGET_HOST_2_PATH}")
        open(TARGET_HOST_2_PATH, "w").close()


@pytest.mark.parametrize("input_file_name", ["large_1M_events.log",
                                             "test_empty_file",
                                             "test_image.jpg",
                                             "test_image.png", "test_image.pdf", "test_random_char_lines.txt",
                                             "test_three_line_small_file.txt"])
def test_agent_splitter_and_target_file_stores(input_file_name, test_run_timestamp):
    """
    Verify file is processed correctly by verifying the counts of each byte value in the file then compare the count of these
    same byte values on target host files. The sum of the counts of each byte value in the target host files should equal the totals in the original
    input file.

    "test_random_char_lines.txt": Contains lines of random lengths and a wide variety of characters.
     captures data loss  since the distribution of each byte value should be highly varied and unique

    "large_1M_events.log": verifies application can process large files without timeouts, performances issues or data loass
    "test_empty_file": verifies application can process empty files without errors or crashing
    "test_image.jpg,png,pdf": verifies application can process binary without data loss and application errors
    """

    test_file_path = INPUT_FILE_DIR / input_file_name
    # configure agent to use test input file_name, run agent app and wait for targets to have updated files
    process_input_files(input_file_name)
    # verify byte counts in target host events.log files match that of the input file processed
    check_target_host_file_bytes(test_file_path)
    logging.info(f"\n\n{input_file_name} Successfully processed and stored by splitter application!")

    store_test_artifacts(test_run_timestamp, input_file_name)


def test_two_files_ingested_wo_clearing_eventslog(test_run_timestamp):
    """
    Verifies when event.logs capture data from more than one file without being cleared no data is lost
    """
    test_file_path_1 = INPUT_FILE_DIR / "test_random_char_lines.txt"
    test_file_path_2 = INPUT_FILE_DIR / "test_image.png"

    # configure agent to use test input file_name, run agent app and wait for targets to have updated files
    process_input_files(test_file_path_1)
    #wait for processing to completely stop in docker before sending another file
    time.sleep(20)
    process_input_files(test_file_path_2)

    input_file_total_byte_ctr = (get_byte_counter(test_file_path_1) + get_byte_counter(test_file_path_2))

    target_1_new_line_count = get_byte_counter(TARGET_HOST_1_PATH)
    target_2_new_line_count = get_byte_counter(TARGET_HOST_2_PATH)
    store_test_artifacts(test_run_timestamp, "multi_ingest_")

    assert input_file_total_byte_ctr == target_1_new_line_count + target_2_new_line_count


def store_test_artifacts(timestamp, artifact_prefix):
    # store artifacts
    artifact_dir = f"{ARTIFACTS_DIR}/{timestamp}/"
    os.makedirs(artifact_dir, exist_ok=True)
    input_file_name = artifact_prefix.replace(".", '_')
    shutil.copy(TARGET_HOST_1_PATH, Path(artifact_dir, f"{artifact_prefix}_target_1_events.log"))
    shutil.copy(TARGET_HOST_2_PATH, Path(artifact_dir, f"{artifact_prefix}_target_2_events.log"))
