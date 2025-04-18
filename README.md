# **THOR APT SCANNER** to Timesketch
This log conversion utility makes it easy to import [THOR](https://www.nextron-systems.com/thor/) logs into [Timesketch](https://timesketch.org/). Combining **THOR** findings on a shared timeline it enables cybersecurity analysts to enhance detection and analysis of malicious activity.

---

## Table of Contents

1. [Description](#description)
2. [Field Mapping Logic](#field-mapping-logic)
3. [Features](#features)
4. [Installation for MacOS and Linux](#installation-for-macos-and-linux)
   - [Prerequisites](#prerequisites)
   - [Installation Steps](#steps)
5. [Usage](#usage)
   - [Command-Line Arguments](#command-line-arguments)
   - [Examples](#examples)
6. [Configuration for Timesketch Ingestion](#configuration-for-timesketch-ingestion)
7. [Input and Output Files](#input-and-output-files)
   - [Warning](#warning)
8. [Ingesting into Timesketch](#ingesting-into-timesketch)
   - [File `jsonl`](#file-jsonl)
   - [Sketch flag](#sketch-flag)
9. [Contributing](#contributing)
10. [Support](#support)

---

## Description
This utility processes **THOR** JSON logs and maps them to Timesketch’s required timeline format by:

* Extracting relevant fields from **THOR** logs

* Generating entries with the required Timesketch fields: message, datetime, and timestamp_desc

* Handling **THOR** events with multiple timestamps by duplicating the log entry for each timestamp found
---
## Field Mapping Logic
This utility maps the following fields from THOR logs to Timesketch's required format:

- **message**
  - A key detection detail generated by **THOR**, providing context or justification for the event.
- **datetime**
  - The **THOR** scan execution time, or
  - A timestamp found within the specific event related to a module or feature.
- **timestamp_desc**:
  - If datetime refers to the THOR scan start time → "Timestamp of THOR scan execution"
  - If datetime originates from a specific module field → "ModuleName - FieldName" (e.g., Filescan - modified)

**Note**: **ruledate** field is not mapped to datetime.

This utility supports THOR JSON log format v2 and is designed with forward compatibility for JSON log format v3.

## Features

1. Validates and reads the input THOR JSON file
2. Flattening THOR logs for efficient indexing and searching
3. Identifies the THOR log version and selects the appropriate mapper
4. Extracts relevant information and timestamps from each log entry
5. Maps THOR fields to Timesketch's required format (message, datetime, timestamp_desc)
6. Writes the mapped events to a single JSONL output file
7. The resulting .jsonl file can be ingested into Timesketch using either the Web UI or the [Importer CLI tool](https://timesketch.org/guides/user/cli-client/)
8. Supports ingestion into Timesketch sketch by specifying the sketch ID or name
---

## Installation for MacOS and Linux
### Prerequisites
Make sure you have the following installed on your system:
- [Git](https://git-scm.com/downloads)
- [Python 3.9](https://www.python.org/downloads/) or higher
- Python venv package 
 *(e.g., on Ubuntu/Debian: `sudo apt install python3-venv`)*
- [THOR](https://www.nextron-systems.com/thor/) JSON logs (v2 or v3) as input for `thor2ts`

### Steps
1. Clone the repository:
```bash
git clone https://github.com/TBD/thor-ts-mapper.git
cd thor-ts-mapper
```
2. Install `thor2ts` by sourcing the `install_thor2ts.sh` script:
```bash
source install_thor2ts.sh
```
This script will:

* Check for prerequisites
* Create a virtual environment named `venv-thor2ts`
* Install thor2ts within the virtual environment
* Activate the virtual environment

Alternatively, you can run the script with `bash`:
```bash
bash install_thor2ts.sh
```
> **Note:** Activate the virtual environment `venv-thor2ts`

3. Future Use
To use `thor2ts` in the new terminal, activate the virtual environment:
```bash
source /path/to/thor-ts-mapper/venv-thor2ts/bin/activate
```
Alternatively, you can source the `install_thor2ts.sh` script again.

---

## Usage
Once the virtual environment is active, you can run the tool from the command line:

```bash
thor2ts <input_file> [-o <output_file>] [--ts_sketch <sketch_id_or_name>] [-v]
```
### Command-Line Arguments
* `input_file` - Path to the THOR JSON file that you want to convert

* `-o output_file` - Path to the output file.

* `--ts_sketch <sketch_id_or_name>` - Specifies the Timesketch sketch ID or name for automatic ingestion.
  - If the sketch does not exist, it will be created.
* `-v, --verbose` - Enable verbose output (optional)
* `--version` - Show the version of the tool and exit (optional)
### Examples
- **Basic Usage**: Convert a THOR JSON file to Timesketch format:
```bash
thor2ts thor_scan.json -o mapped_events.jsonl
```
- **Ingest into Timesketch**: Convert and ingest the THOR JSON events into a Timesketch sketch:
```bash
thor2ts thor_scan.json --ts_sketch "THOR APT Sketch"
```
- **Verbose Output**: Enable verbose output for debugging:
```bash
thor2ts thor_scan.json -o mapped_events.jsonl -v
```
---
## Configuration for Timesketch Ingestion
**First-time configuration**: When using this flag for the first time, you'll be prompted to configure Timesketch settings:
* `host_uri` - The URL of the Timesketch server.
* `auth_mode` - Authentication mode, valid choices are: "userpass" (user/pass) or "oauth"
* `username` - Your Timesketch username.
* `password` - Your Timesketch password. **Note:** The password will be tokenized.
This creates two configuration files in the user's home directory `$HOME/`:

  - `~/.timesketch.token` - Stores authentication tokens
  - `~/.timesketchrc` - Stores connection configuration with the following format:
```ini
[timesketch]
host_uri = http://timessketch.example.com
username = yourusername
verify = True
client_id = 
client_secret = 
auth_mode = userpass
cred_key = <generated_key>
```
---
## Input and Output Files

**Input Files:**
- **THOR** JSON log files (version **v2** or **v3**).

**Output Files:**
- The tool produces a JSONL file containing timesketch formated events.
- If the specified output file does not end with `.jsonl`, the tool updates the extension.
- If the file exists, new events are appended.
- If the output directory does not exist, it is created automatically.
### Warning
> Timesketch accepts only JSON files with a `.jsonl` extension.

---


## Ingesting into Timesketch
### File `jsonl`
The resulting (`.jsonl`) file can be ingested into Timesketch using either the Web UI or the [Importer CLI tool](https://timesketch.org/guides/user/cli-client/).
### Sketch flag
If you specify the `--ts_sketch` flag, the tool will automatically ingest the mapped events into the specified Timesketch sketch.

---
## Contributing
Contributions to `thor2ts` are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with your improvements or bug fixes.

---
## Support
If you encounter any issues or have questions, please open an issue in the [GitHub repository](https://github.com/NextronSytems/thor-ts-mapper.git).

---