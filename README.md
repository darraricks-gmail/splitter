
Prerequisites




docker
docker compose

docker --version
docker compose version

Build and Deploy Splitter App and Tests

Run Tests

Git Action Workflows
Test Report
Stored artifacts
Teardown application
Approach
(test cases )
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
agent execution

Troubleshooting
(volumes)
File Structure
Shared Mount
Explanation of File 
`   root:file_processing_utils.py:17 Processing input file test_three_line_small_file.txt
INFO     root:file_processing_utils.py:27 
Input file test_three_line_small_file.txt has been written to /ingestion_io/input_monitor_file_path.json
INFO     root:file_processing_utils.py:40 b"My hostname is: 8138dcbd6cdf\nWorking as agent\ntcp= { host: 'splitter', port: 9997 }\nmonitored_filename= /app/agent/inputs/test_three_line_small_file.txt\nConnecting to  { host: 'splitter', port: 9997 }\nconnected to target { host: 'splitter', port: 9997 }\n"
INFO     root:file_processing_utils.py:41 None
INFO     root:file_processing_utils.py:68 Waiting for 5 seconds for splitter process to finish on target host 1 retry 1/20 
INFO     root:file_processing_utils.py:82 Waiting for 5 seconds for splitter process to finish on target host 2 retry 0/2 
INFO     root:file_processing_utils.py:133 Byte 10 (\n): input_file_char_count=2, target_files_char_count=2, 
INFO     root:file_processing_utils.py:133 Byte 32 ( ): input_file_char_count=10, target_files_char_count=10, 
INFO     root:file_processing_utils.py:133 Byte 73 (I): input_file_char_count=1, target_files_char_count=1, 
INFO     root:file_processing_utils.py:133 Byte 87 (W): input_file_char_count=1, target_files_char_count=1, 
INFO     root:file_processing_utils.py:133 Byte 97 (a): input_file_char_count=4, target_files_char_count=4, 
INFO     root:file_processing_utils.py:133 Byte 100 (d): input_file_char_count=1, target_files_char_count=1, 
...
`
