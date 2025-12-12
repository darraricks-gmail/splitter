import json
import logging
import os
import time
import docker
from collections import Counter

from constants import INPUT_JSON_FILE_PATH, TARGET_HOST_1_PATH, TARGET_HOST_2_PATH, CHUNK_SIZE


def process_input_files(test_file_name):
    """
    Sets input file configuration name in agent container and runs app.js in agent container. so that the specfied
    input file will be sent to splitter to be processed
    :param test_file_name:
    """
    logging.info(f"Processing input file {test_file_name}")

    # update input.json monitor file with test file name
    file_path = INPUT_JSON_FILE_PATH
    new_input_file_json = {"monitor": f"inputs/{test_file_name}"}
    if os.path.exists(file_path):

        with open(file_path, "w") as new_input_file:
            new_input_file.write(json.dumps(new_input_file_json))

            logging.info(f"\nInput file {test_file_name} has been written to {file_path}")
        os.chmod(file_path, 0o644)

    else:
        Exception("Input file json spec does not exist please add input file spec")

    #create docker client to run app.js on agent container
    docker_client = docker.from_env()
    if not docker_client.containers.get("splitter-agent-1"):
            Exception("Docker container has splitter-agent-1 not been created")
    agent_container = docker_client.containers.get("splitter-agent-1")
    response = agent_container.exec_run("node /app/agent/app.js /app/agent", demux=True)
    std_out, std_err = response.output
    logging.info(std_out)
    logging.info(std_err)
    if response.exit_code != 0:
            raise Exception(
                f"\nFailed to start agent app.js to process {test_file_name} failed with exit code {std_out} \n {std_err}\n")

    wait_until_splitter_is_done_processing()


def wait_until_splitter_is_done_processing():
    """
    Wait until the splitter process has finished processing data by continually checking target host files siz
    """
    prev_size = 0
    retries = 20
    wait_time_seconds = 5
    target_file_1_done = False
    target_file_2_done = False

    if os.path.exists(TARGET_HOST_1_PATH) and os.path.exists(TARGET_HOST_2_PATH):
        for retry in range(retries):

            current_size = os.path.getsize(TARGET_HOST_1_PATH)
            if current_size == prev_size:
                target_file_1_done = True
                break
            prev_size = current_size
            time.sleep(wait_time_seconds)
            logging.info(
                f"Waiting for {wait_time_seconds} seconds for splitter process to finish on target host 1 retry {retry+1}/{retries} ")
    else:
        Exception("Target host files does not exist before test run, add input file spec and run agent first")

    retries = 2
    prev_size = 0
    for retry in range(retries):
        current_size = os.path.getsize(TARGET_HOST_2_PATH)
        if current_size == prev_size:
            target_file_2_done = True
            break
        prev_size = current_size
        time.sleep(wait_time_seconds)
        logging.info(
            f"Waiting for {wait_time_seconds} seconds for splitter process to finish on target host 2 retry {retry}/{retries} ")

    if not target_file_1_done and target_file_2_done:
        Exception("Timed out waiting for splitter process to finish")


def check_target_host_file_bytes(input_file_path):
    """
    Check if target host file bytes count are equalivalent to original file input file byte counts
    :param input_file_path: string file path of input file agent
    """

    input_new_line_count = Counter()
    with open(input_file_path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            input_new_line_count.update(chunk)
    target_1_new_line_count = Counter()
    with open(TARGET_HOST_1_PATH, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            target_1_new_line_count.update(chunk)
    target_2_new_line_count = Counter()
    with open(TARGET_HOST_2_PATH, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            target_2_new_line_count.update(chunk)
    targets_char_count = (target_1_new_line_count + target_2_new_line_count)
    show_character_differences(input_new_line_count, targets_char_count)

    assert input_new_line_count == (
                target_1_new_line_count + target_2_new_line_count), "Data corrupted during splitting, bytes mismatch between input and target host files"


def show_character_differences(input_file_byte_counts, target_file_byte_counts):
    """
    Show the differences between number of each character in input file versus target file byte counts.
    """
    bytes = set(input_file_byte_counts.keys()) | set(target_file_byte_counts.keys())
    logging.info("\n")
    for byte in sorted(bytes):
        input_file_byte_count = input_file_byte_counts.get(byte, 0)
        target_file_byte_count = target_file_byte_counts.get(byte, 0)

        if 32 <= byte <= 126:
            ascii_repr = chr(byte)
        elif byte == 10:
            ascii_repr = r"\n"
        elif byte == 13:
            ascii_repr = r"\r"
        else:
            ascii_repr = f"0x{byte:02x}"  # if no printable ascii

        logging.info(
            f"Byte {byte} ({ascii_repr}): "
            f"input_file_char_count={input_file_byte_count}, target_files_char_count={target_file_byte_count}, "
        )
