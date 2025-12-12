
## Purpose
This repo contains a test setup to verify data is processed sufficiently via the following application

Agent: Reads from a specified file and forwards the contents to a ‘Splitter’

Splitter: - Receives data from an ‘Agent’ and randomly splits the data between the two configured ‘Target’ hosts

Target: Receives data from a ‘Splitter’ and writes it to a file on disk

The application will be hosted in docker each service Agent, Splitter and 2 Targets run in an individual docker container.  A test
container will also be deployed with the application

## Project Highlights:  
-  Agent is driven test harness using a volume shared across application containers to iterate through any set of data scenarios in a set of files
(include file structure explanation)
- Each test case is associated with a specific data file covering a different expectation
- CI: Deploy and Test Github Action workflow automatically triggers and deploys application and tests, trigged by pushes to main branch and also uses test results to   gate pull requests to main branch  
- Target Host output event.log artifacts are timestamped and stored for reference for each test run)
- Test logs show bytes character counts used in test verification
- Published test report after each Deploy and Test workflow run triggered by a change to main branch only at: https://darraricks-gmail.github.io/splitter/


## Prerequisites 

To run this project locally, ensure 'docker' and 'docker compose; are installed on your machine to build and deploy application
containers 

**To verify docker installation:**
   
   docker --version
   
**To verify docker compose installation:** 

  docker compose version

If you find docker is not installed you can download an installation file for Docker Desktop: https://www.docker.com/products/docker-desktop/


Once installed , repeat the verification steps


## Deploying Application and Test Containers

Verify the Docker daemon has started.  To do this make sure your Docker Desktop application is launch

Once you have docker running, at the root of the project directory run, you will see a docker-compose.yml file in this directory run:
docker compose up --build -d

To Run Test Suite: 
run the following also in the root directory:
docker compose exec tests pytest -v
after tests are complete you can retrieve the test artifacts in the /test_artifacts directory artifact details 

Tear Down Application and Test Containers
docker compose down  

Troubleshooting:
On rare occasion after many docker builds and deploys you might start to see various file not found errors in the test logs if this starts to occur
consistently try tearing down the deployment container along with deleting the volumes as well, just remember all data associated with them will be wiped:
docker compose down -v
then deploy again
docker compose up --build 


# Test Strategy

**High Level Directory Structure**

- app/ :   contains all application code files agent,splitter and targets to run, each of these contains a Dockerfile for container build

- html_report_pkg:   used for github pages publish contain index.html that points to the report.html

- ingestion_io:    shared volume directory  agent,targets and test container share this volume

- ingestion_io/input_files:     contains all test input files used in test set, visible to agent and test container

- ingestion_io/output_split_data:  this is what is updated as each target recieves split file data as it is mapped their container event.log, the test container empties the event.logs at the beginning of each test and targets write new file data

- ingestion_io/input_monitor_file_path.json:       updated by tests to spe

- test_artifacts/   all test artifacts for tests run

- tests/ :  Dockerfile for test container and 

- docker-compose.yml

   The agent application sends one specified file at a time upon node ./app.js ./ , in order to run multiple test scenarios in a test run this
test harness is setup to drive the agent app by updating the input file configuration the agent app reads from ./app/agent/inputs.json.  This
is done from the test container by updating the input_monitor_file_path.json file stored on the shared docker volume 

 Test Setup Steps:
   1. Update the input file configuration that the agent app reads from ./app/agent/inputs.json.  This is done from the test container by updating the input_monitor_file_path.json file stored on the shared docker volume 
   2. Run the node command for the agent to initialize file processing, this is done by binding the test containers docker daemon socket to the host docker daemon
   3. monitors shared volume ingestion_io/output_split_data/target*/event.log files until data is no longer being added to them
   4. Next step is verify the data within event logs this is explained in the following Test Cases section


#  Test Cases
    
    Verify file is processed correctly by verifying the counts of each byte value in the file then compare the count of these
    same byte values on target host files. The sum of the counts of each byte value in the target host files should equal the totals in the original
    input file.

    "test_random_char_lines.txt": Contains lines of random lengths and a wide variety of characters.
     captures data loss  since the distribution of each byte value should be highly varied and unique

    "large_1M_events.log": verifies application can process large files without timeouts, performances issues or data loass
    "test_empty_file": verifies application can process empty files without errors or crashing
    "test_image.jpg,png,pdf": verifies application can process binary without data loss and application errors



Test Artifacts

After executing a local run
/splitter/test_artifacts will contain a timestamped directory for each run, within this directory 
- the event.log file for each target host can be found named according to the target host number and the initial input test file
used 
- report.html : html test report of last run
![img.png](img.png)
- 
Test Report of Latest Run CI against  Master can be found at:
Also in the bottom summary section of each gh action test workflow
- Test Summary of the amount of tests that passed and failed , this will also out
- run you can find a downloadable zipped copy of the test_artifacts directory described above as well 
- report.html downloadable artifact
![img_1.png](img_1.png)

Test Logging Output
- shows byte count validations
- progress of processing from monitoring shared volume between target hosts and test container for event.log updates to complet
As explained in the test strategy section data for each file is validated by counting the number of occurrences of each byte value, the logs will
show the byte value count of the original input file and the sum of the byte value counts from the target host event.logs

So for the example below:  the byte value 101 ASCII 'e' has the correct t_count (total count) of 'e' since t_count=t1_count +t2_count==in_file_count
 Byte 101 (e): in_file_count=3000000, t1_count=1481523, t2_count=1518477, t_count=3000000 
![img_2.png](img_2.png)






