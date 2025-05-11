import requests
import websockets
import asyncio
import json
from typing import Optional, Dict, Any, List, Generator, IO
from pathlib import Path
import os

from .exceptions import (
    RunRLError,
    AuthenticationError,
    PermissionError,
    NotFoundError,
    APIServerError,
    RequestError
)

DEFAULT_BASE_URL = "https://runrlusercontent.com"

class RunRL:
    """Client for interacting with the RunRL API."""

    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL):
        if not api_key:
            raise ValueError("API key is required.")
        if not api_key.startswith("rl-"):
             print("Warning: API key does not start with 'rl-'. Ensure it's a valid RunRL API key.")

        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": self.api_key,
            "Accept": "application/json",
        }
        # Determine WebSocket base URL based on the scheme of the input base_url
        # Use the original base_url (before rstrip) for scheme checking
        if base_url.startswith("https://"):
            self.websocket_base_url = base_url.replace("https://", "wss://", 1).rstrip('/')
        elif base_url.startswith("http://"):
            self.websocket_base_url = base_url.replace("http://", "ws://", 1).rstrip('/')
        else:
            # Fallback for URLs that might not have a scheme, though DEFAULT_BASE_URL does.
            # This could also be an error condition depending on expected inputs.
            print(f"Warning: base_url '{base_url}' does not start with http:// or https://. WebSocket URL ('{base_url.rstrip('/')}') may be incorrect if it's not a relative path or requires a ws/wss scheme explicitly.")
            self.websocket_base_url = base_url.rstrip('/')

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Processes the HTTP response, checking for errors and returning JSON."""
        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            response_json = {"detail": response.text} # Use raw text if JSON fails

        if 200 <= response.status_code < 300:
            return response_json
        elif response.status_code == 401:
            raise AuthenticationError(f"Authentication failed: {response_json.get('detail', 'Unauthorized')}")
        elif response.status_code == 403:
            raise PermissionError(f"Permission denied: {response_json.get('detail', 'Forbidden')}")
        elif response.status_code == 404:
            raise NotFoundError(f"Resource not found: {response_json.get('detail', 'Not Found')}")
        elif 400 <= response.status_code < 500:
            # More specific client error handling can be added here if needed
            raise RequestError(f"Client error ({response.status_code}): {response_json.get('detail', 'Bad Request')}")
        elif response.status_code >= 500:
            raise APIServerError(f"Server error ({response.status_code}): {response_json.get('detail', 'Internal Server Error')}")
        else:
            raise RunRLError(f"Unexpected status code {response.status_code}: {response_json.get('detail', 'Unknown Error')}")

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> requests.Response:
        """Makes an authenticated HTTP request to the API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self.headers.copy()
        if not files: # requests handles Content-Type for multipart/form-data
             headers['Content-Type'] = 'application/json'

        try:
            response = requests.request(
                method,
                url,
                params=params,
                json=json_data,
                headers=headers,
                files=files,
                data=data,
                stream=stream
            )
            return response
        except requests.exceptions.RequestException as e:
            raise RunRLError(f"HTTP request failed: {e}")

    # --- User Data --- 
    def get_user_data(self) -> Dict[str, Any]:
        response = self._request("GET", "/user-data")
        return self._handle_response(response)

    # --- Runs --- 
    def list_runs(self) -> List[Dict[str, Any]]:
        """Lists all runs for the user, removing verbose metrics and logs data."""
        response = self._request("GET", "/runs")
        response_data = self._handle_response(response)

        try:
            runs_list = response_data.get("runs", [])
        except AttributeError:
             runs_list = response_data if isinstance(response_data, list) else []

        processed_runs = []
        if isinstance(runs_list, list):
            for i, run in enumerate(runs_list):
                if not isinstance(run, dict):
                    # Keep this warning print, it's useful for malformed API responses
                    print(f"Warning: Skipping non-dictionary item in runs list at index {i}: {type(run)}")
                    continue

                processed_run = run.copy()
                processed_run.pop('metrics', None) # Remove metrics if exists
                processed_run.pop('logs', None)    # Remove logs if exists
                processed_runs.append(processed_run)
        else:
            # Keep this warning print too
            print(f"Warning: Could not extract a list of runs from response: {type(response_data)}")
            return []

        return processed_runs

    def create_run(self, **kwargs) -> Dict[str, Any]: 
        """Creates a new run with the specified parameters.

        Args:
            gpu_type (str): The type of GPU to use.
            n_gpus (int): The number of GPUs.
            model_name (str): The name of the model.
            lora_rank (int): The LoRA rank.
            max_seq_length (int): Maximum sequence length.
            epochs (int): Number of training epochs.
            prompt_file (Optional[str]): ID of the uploaded prompt file.
            reward_file (Optional[str]): ID of the uploaded reward file.
            learning_rate (Optional[float]): Learning rate.
            adam_beta1 (Optional[float]): Adam beta1 parameter.
            adam_beta2 (Optional[float]): Adam beta2 parameter.
            weight_decay (Optional[float]): Weight decay.
            warmup_ratio (Optional[float]): Warmup ratio.
            kl_beta (Optional[float]): KL beta parameter.
            hf_token (Optional[str]): Hugging Face token.

        Returns:
            Dict[str, Any]: The details of the created run.

        Raises:
            ValueError: If required arguments are missing or invalid.
            TypeError: If argument types are incorrect.
        """
        required_args = {
            "gpu_type": str,
            "n_gpus": int,
            "model_name": str,
            "lora_rank": int,
            "max_seq_length": int,
            "epochs": int
        }
        optional_args = {
            "prompt_file": str,
            "reward_file": str,
            "learning_rate": float,
            "adam_beta1": float,
            "adam_beta2": float,
            "weight_decay": float,
            "warmup_ratio": float,
            "kl_beta": float,
            "hf_token": str
        }
        all_expected_args = set(required_args.keys()) | set(optional_args.keys())

        # Check for missing required arguments
        missing_required = [arg for arg in required_args if arg not in kwargs]
        if missing_required:
            raise ValueError(f"Missing required arguments for create_run: {', '.join(missing_required)}")

        # Check for unexpected arguments
        unexpected_args = [arg for arg in kwargs if arg not in all_expected_args]
        if unexpected_args:
             print(f"Warning: Unexpected arguments provided to create_run: {', '.join(unexpected_args)}. These will be ignored by the client but sent to the API.")
             # Or raise ValueError(f"Unexpected arguments: {', '.join(unexpected_args)}") if strict

        # Type checking
        for arg, expected_type in required_args.items():
            if arg in kwargs and not isinstance(kwargs[arg], expected_type):
                raise TypeError(f"Argument '{arg}' must be type {expected_type.__name__}, got {type(kwargs[arg]).__name__}")

        for arg, expected_type in optional_args.items():
            if arg in kwargs and kwargs[arg] is not None and not isinstance(kwargs[arg], expected_type):
                 raise TypeError(f"Argument '{arg}' must be type {expected_type.__name__} or None, got {type(kwargs[arg]).__name__}")

        # : Validate kwargs against RunCreate model if desired - Basic validation added above
        response = self._request("POST", "/runs", json_data=kwargs)
        return self._handle_response(response)

    def get_run_details(self, run_id: str) -> Dict[str, Any]:
        response = self._request("GET", f"/runs/{run_id}")
        return self._handle_response(response)

    def cancel_run(self, run_id: str) -> Dict[str, Any]:
        response = self._request("POST", f"/runs/{run_id}/cancel")
        return self._handle_response(response)

    # --- Prompt Files --- 
    def list_prompt_files(self) -> List[Dict[str, Any]]:
        response = self._request("GET", "/prompt-files")
        return self._handle_response(response).get("files", [])

    def upload_prompt_file(self, file_path: str, friendly_name: Optional[str] = None) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        files = {'file': (path.name, open(path, 'rb'), 'application/octet-stream')}
        data = {}
        if friendly_name:
            data['friendly_name'] = friendly_name

        response = self._request("POST", "/prompt-files", files=files, data=data)
        return self._handle_response(response)

    def delete_prompt_file(self, file_id: str) -> Dict[str, Any]:
        response = self._request("DELETE", f"/prompt-files/{file_id}")
        return self._handle_response(response)

    def get_prompt_file_preview(self, file_id: str) -> Dict[str, Any]:
        response = self._request("GET", f"/prompt-files/{file_id}")
        return self._handle_response(response)

    # --- Reward Files --- 
    def list_reward_files(self) -> List[Dict[str, Any]]:
        response = self._request("GET", "/reward-files")
        return self._handle_response(response).get("files", [])

    def upload_reward_file(self, file_path: str, friendly_name: Optional[str] = None) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        files = {'file': (path.name, open(path, 'rb'), 'application/octet-stream')}
        data = {}
        if friendly_name:
            data['friendly_name'] = friendly_name

        response = self._request("POST", "/reward-files", files=files, data=data)
        return self._handle_response(response)

    def delete_reward_file(self, file_id: str) -> Dict[str, Any]:
        response = self._request("DELETE", f"/reward-files/{file_id}")
        return self._handle_response(response)

    def get_reward_file_content(self, file_id: str) -> Dict[str, Any]:
        response = self._request("GET", f"/reward-files/{file_id}")
        return self._handle_response(response)

    # --- Models & Deployments --- 
    def download_model(self, job_name: str, output_path: str) -> None:
        response = self._request("GET", f"/download-model/{job_name}", stream=True)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Model '{job_name}' downloaded to {output_path}")
        else:
            # Use _handle_response to raise appropriate error based on status code
            self._handle_response(response)

    def list_deployments(self, job_name: str) -> List[Dict[str, Any]]:
        response = self._request("GET", f"/deployments/{job_name}")
        return self._handle_response(response)

    def deploy_model(self, job_name: str) -> Dict[str, Any]:
        response = self._request("POST", f"/deploy-model/{job_name}")
        return self._handle_response(response)

    # --- Metrics & Logs --- 
    def get_stored_metrics(self, run_id: str) -> Dict[str, Any]:
        response = self._request("GET", f"/runs/{run_id}/stored-metrics")
        return self._handle_response(response)

    def get_stored_logs(self, run_id: str, max_lines: int = 2000) -> Dict[str, Any]:
        params = {"max_lines": max_lines}
        response = self._request("GET", f"/runs/{run_id}/stored-logs", params=params)
        return self._handle_response(response)

    async def _stream_logs_async(self, run_id: str, follow: bool = True) -> Generator[Dict[str, Any], None, None]:
        uri = f"{self.websocket_base_url}/ws/runs/{run_id}/logs?follow={'true' if follow else 'false'}&token={self.api_key}"
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    try:
                        message = await websocket.recv()
                        yield json.loads(message)
                    except websockets.exceptions.ConnectionClosedOK:
                        print("Log stream finished.")
                        break
                    except websockets.exceptions.ConnectionClosedError as e:
                        print(f"Log stream connection closed unexpectedly: {e}")
                        raise RunRLError(f"WebSocket connection error: {e}")
                    except json.JSONDecodeError:
                        print(f"Received non-JSON message: {message}") # Or handle as plain text
                        yield {"type": "raw", "content": message}
                    except Exception as e:
                         print(f"Error receiving log message: {e}")
                         raise RunRLError(f"Log streaming error: {e}")

        except websockets.exceptions.InvalidURI:
            raise ValueError(f"Invalid WebSocket URI: {uri}")
        except websockets.exceptions.WebSocketException as e:
             raise RunRLError(f"Failed to connect to WebSocket: {e}")

    def stream_logs(self, run_id: str, follow: bool = True) -> Generator[Dict[str, Any], None, None]:
        async def main():
            log_generator = self._stream_logs_async(run_id, follow)
            async for log_entry in log_generator:
                yield log_entry

        # This approach is basic. For robust integration into non-async apps,
        # consider running the async part in a separate thread.
        # However, yielding from an async generator directly into sync code is tricky.
        # A common pattern is using asyncio.run() within the method, but that blocks
        # and doesn't fit the generator pattern well for streaming.
        # For now, let's return the async generator and note it needs an async context.
        print("Note: stream_logs returns an async generator. Use 'async for' to iterate.")
        loop = asyncio.get_event_loop()
        if loop.is_running():
             # If already in an event loop (e.g., Jupyter), we might need a different approach
             # like creating a new thread or using nest_asyncio. Returning the async gen is safest.
             return self._stream_logs_async(run_id, follow)
        else:
             # A simple way to run, but blocks. Not ideal for true streaming in sync code.
             # For a simple script, this might be okay.
             # For library use, requiring the user to handle async is better.
             # Let's stick to returning the async generator.
             return self._stream_logs_async(run_id, follow)
             # Alternative (blocking): asyncio.run(main()) # Doesn't work for yield

    # --- GPU Prices --- 
    def get_gpu_price(self, gpu_type: str) -> Dict[str, Any]:
        response = self._request("GET", f"/gpu-price/{gpu_type}")
        return self._handle_response(response)

    def get_all_gpu_prices(self) -> List[Dict[str, Any]]:
        response = self._request("GET", "/gpu-prices")
        return self._handle_response(response).get("prices", []) 
