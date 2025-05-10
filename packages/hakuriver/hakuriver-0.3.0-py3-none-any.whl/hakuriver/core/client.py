import json
import sys
import httpx
from hakuriver.utils.logger import logger
from hakuriver.core.config import CLIENT_CONFIG


# --- Helper Functions ---
def print_response(response: httpx.Response):
    """Helper to print formatted JSON response or error text."""
    print(f"HTTP Status Code: {response.status_code}")
    try:
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            data = response.json()
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print("Response Text:")
            print(response.text)
    except json.JSONDecodeError:
        print("Response Text (non-JSON or parse error):")
        print(response.text)
    except Exception as e:
        print(f"Error processing response content: {e}")
        print("Raw Response Text:")
        print(response.text)


def parse_key_value(items: list[str]) -> dict[str, str]:
    """Parses ['KEY1=VAL1', 'KEY2=VAL2'] into {'KEY1': 'VAL1', 'KEY2': 'VAL2'}"""
    result = {}
    if not items:
        return result
    for item in items:
        parts = item.split("=", 1)
        if len(parts) == 2:
            result[parts[0].strip()] = parts[1].strip()
        else:
            print(
                f"Warning: Ignoring invalid environment variable format: {item}",
                file=sys.stderr,
            )
    return result


# --- Client API Functions ---
def submit_task(
    command: str,
    args: list[str],
    env: dict[str, str],
    cores: int,
    memory_bytes: int | None,
    targets: list[str],  # Changed from individual target/sandbox flags
    container_name: str | None = None,  # Matches TaskRequest model field
    privileged: bool | None = None,  # Matches TaskRequest model field
    additional_mounts: list[str] | None = None,  # Matches TaskRequest model field
    gpu_ids: (
        list[list[int]] | list[int] | None
    ) = None,  # Matches TaskRequest model field
) -> list[str] | None:  # Returns list of task IDs
    """Submits a task potentially to multiple targets."""
    url = f"{CLIENT_CONFIG.host_url}/submit"
    # Construct payload based on the Host's TaskRequest model
    if targets:
        target_desc = ", ".join(targets)
        logger.info(f"Submitting task to {url} for target(s): {target_desc}")
    elif gpu_ids:
        logger.warning("GPU IDs provided but no targets specified. Ignored.")
        gpu_ids = None
    else:
        if isinstance(gpu_ids[0], int):
            gpu_ids = [gpu_ids] * len(targets)
    payload = {
        "command": command,
        "arguments": args,
        "env_vars": env,
        "required_cores": cores,
        "required_memory_bytes": memory_bytes,
        "targets": targets,  # Pass the list of target strings
        "container_name": container_name,
        "privileged": privileged,
        "additional_mounts": additional_mounts,
        "required_gpus": gpu_ids,
    }
    print(payload)
    logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
    return submit_payload(url, payload)


def create_vps(
    public_key: str,
    cores: int = 0,
    memory_bytes: int | None = None,
    targets: str | None = None,
    container_name: str | None = None,  # Matches TaskRequest model field
    privileged: bool | None = None,  # Matches TaskRequest model field
    additional_mounts: list[str] | None = None,  # Matches TaskRequest model field
    gpu_ids: list[int] | None = None,  # Matches TaskRequest model field
) -> list[str] | None:  # Returns list of task IDs
    """Submits a task potentially to multiple targets."""
    url = f"{CLIENT_CONFIG.host_url}/submit"
    # Construct payload based on the Host's TaskRequest model
    if targets:
        assert isinstance(targets, str), "Targets must be a string for VPS tasks."
        logger.info(f"Submitting task to {url} for target(s): {targets}")
        if gpu_ids:
            gpu_ids = [gpu_ids]
        targets = [targets]
    elif gpu_ids:
        logger.warning("GPU IDs provided but no targets specified. Ignored.")
        gpu_ids = None
    payload = {
        "task_type": "vps",
        "command": public_key,
        "arguments": [],
        "env_vars": {},
        "required_cores": cores,
        "required_memory_bytes": memory_bytes,
        "targets": targets,
        "container_name": container_name,
        "privileged": privileged,
        "additional_mounts": additional_mounts,
        "required_gpus": gpu_ids,
    }
    logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
    return submit_payload(url, payload)


def submit_payload(url, payload):
    try:
        with httpx.Client(timeout=CLIENT_CONFIG.default_timeout) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            logger.info("--- Submission Response ---")
            # Print formatted response using helper
            print_response(response)
            # Extract and return the list of task IDs
            task_ids = result.get("task_ids")
            if isinstance(task_ids, list):
                # Convert IDs to string as they might be large integers (Snowflake)
                return [str(tid) for tid in task_ids]
            else:
                logger.error(
                    f"Host response missing or invalid 'task_ids' list: {result}"
                )
                return None
    except httpx.HTTPStatusError as e:
        print_response(e.response)  # Print detailed error from host
    except httpx.RequestError as e:
        logger.error(f"Error connecting to host at {url}: {e}")
    except Exception as e:
        logger.exception(
            f"An unexpected error occurred during submission: {e}"
        )  # Use logger.exception
    return None


def get_active_vps_status():
    """Fetches the status of active VPS tasks."""
    url = f"{CLIENT_CONFIG.host_url}/vps/status"  # Call the new endpoint
    logger.info(f"Fetching active VPS status from {url}")

    try:
        with httpx.Client(timeout=CLIENT_CONFIG.status_timeout) as client:
            response = client.get(url)
            response.raise_for_status()
            logger.info("--- Active VPS Status ---")
            print_response(response)  # Use the helper to print JSON

    except httpx.HTTPStatusError as e:
        print_response(e.response)
        logger.error(f"HTTP error occurred while fetching active VPS status.")
    except httpx.RequestError as e:
        logger.error(f"Network error occurred while connecting to {url}: {e}")
    except Exception as e:
        logger.exception(
            f"An unexpected error occurred fetching active VPS status: {e}"
        )


# Also, add a new function for the 'command' endpoint
def send_task_command(task_id: str, action: str):
    """Sends a control command (e.g., pause, resume) to a task."""
    url = f"{CLIENT_CONFIG.host_url}/command/{task_id}/{action}"
    logger.info(f"Sending command '{action}' to task {task_id} at {url}")
    try:
        with httpx.Client(timeout=CLIENT_CONFIG.default_timeout) as client:
            response = client.post(url)
            response.raise_for_status()
            logger.info(f"--- Command '{action}' Response ---")
            print_response(response)
    except httpx.HTTPStatusError as e:
        print_response(e.response)
        logger.error(f"HTTP error occurred while sending command.")
    except httpx.RequestError as e:
        logger.error(f"Network error occurred while connecting to {url}: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred sending command: {e}")


def check_status(task_id: str) -> str | None:
    """Checks the status of a specific task."""
    url = f"{CLIENT_CONFIG.host_url}/status/{task_id}"
    print(f"Checking status for task {task_id} at {url}")
    try:
        with httpx.Client(timeout=CLIENT_CONFIG.status_timeout) as client:
            response = client.get(url)
            response.raise_for_status()
            print("--- Task Status ---")
            print_response(response)
            try:
                # Return status for wait logic
                return response.json().get("status")
            except (json.JSONDecodeError, AttributeError):
                print("Warning: Could not parse status from response.", file=sys.stderr)
                return None
    except httpx.HTTPStatusError as e:
        print_response(e.response)
    except httpx.RequestError as e:
        print(f"Error connecting to host at {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None


def kill_task(task_id: str):
    """Requests the host to kill a task."""
    url = f"{CLIENT_CONFIG.host_url}/kill/{task_id}"
    print(f"Requesting kill for task {task_id} at {url}")
    try:
        with httpx.Client(timeout=CLIENT_CONFIG.kill_timeout) as client:
            response = client.post(url)  # Defined as POST in host
            response.raise_for_status()
            print("--- Kill Request Response ---")
            print_response(response)
    except httpx.HTTPStatusError as e:
        print_response(e.response)
    except httpx.RequestError as e:
        print(f"Error connecting to host at {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def list_nodes():
    """Fetches the status of compute nodes, including NUMA info."""
    url = f"{CLIENT_CONFIG.host_url}/nodes"
    logger.info(f"Fetching node status from {url}")
    try:
        with httpx.Client(timeout=CLIENT_CONFIG.nodes_timeout) as client:
            response = client.get(url)
            response.raise_for_status()
            logger.info("--- Nodes Status ---")
            print_response(response)

    except httpx.HTTPStatusError as e:
        print_response(e.response)
    except httpx.RequestError as e:
        logger.error(f"Error connecting to host at {url}: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")  # Use logger.exception


def get_health(hostname: str | None = None):
    """Fetches the health status, including NUMA info."""
    url = f"{CLIENT_CONFIG.host_url}/health"
    params = {}
    log_msg = "Fetching cluster health status"
    if hostname:
        params["hostname"] = hostname
        log_msg = f"Fetching health status for node {hostname}"
    logger.info(f"{log_msg} from {url}")

    try:
        with httpx.Client(timeout=CLIENT_CONFIG.health_timeout) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            logger.info("--- Health Status ---")
            # print_response will dump the full JSON including numa_topology
            print_response(response)
            # Optional: Add custom formatting here later

    except httpx.HTTPStatusError as e:
        print_response(e.response)
    except httpx.RequestError as e:
        logger.error(f"Error connecting to host at {url}: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")  # Use logger.exception
