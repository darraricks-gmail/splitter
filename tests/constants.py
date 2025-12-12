
from pathlib import Path

CHUNK_SIZE = 4096
def project_root():
    return Path(__file__).resolve().parent.parent

IO_DIR = project_root()/"ingestion_io"
TARGET_HOST_1_PATH = IO_DIR/ "output_split_data" / "target_1" / "events.log"
TARGET_HOST_2_PATH = IO_DIR / "output_split_data" / "target_2" / "events.log"
INPUT_JSON_FILE_PATH = IO_DIR / "input_monitor_file_path.json"
INPUT_FILE_DIR = IO_DIR/ "input_files"
TESTS_DIR = Path.cwd()
ARTIFACTS_DIR = TESTS_DIR.parent / "test_artifacts"