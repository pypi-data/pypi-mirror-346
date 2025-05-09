#!/usr/bin/env python3
import grpc
import json
import time
import threading
import logging
import asyncio
import requests 
import argparse
import os
import sys
import platform

from .exceptions import ConnectionError, RequestError, ConfigurationError, SubscriptionError, DecryptionError
from .proto import service_pb2, service_pb2_grpc
from .subscriber import main_async
from .crypto import get_wallet_address,decrypt_alpha_message
from .utils import fetch_historical_entries


logger = logging.getLogger(__name__)

class LiberalAlphaClient:
    """
    Liberal Alpha SDK Client for sending data via gRPC, subscribing to WebSocket data,
    and fetching user's record information.

    Parameters:
      - host (optional, default "127.0.0.1"): Host address where the runner is located
      - port (optional, default 8128): Port number where the runner is listening
      - rate_limit_enabled (optional, default True): Whether rate limiting is enabled
      - api_key (optional): Your API key from Liberal Alpha
      - private_key (optional): Your Ethereum private key for decryption

    Note:
      - The wallet address is automatically computed from the private key if provided.
      - The base URL is fixed to "https://api.liberalalpha.com".
      - For data subscription, both api_key and private_key are required.
      - For sending data to runner, a local runner must be running at host:port.
    """
    
    def __init__(self, host=None, port=None, rate_limit_enabled=None, api_key=None, private_key=None):
        self.host = host if host is not None else "127.0.0.1"
        self.port = port if port is not None else 8128
        self.rate_limit_enabled = rate_limit_enabled if rate_limit_enabled is not None else True
        self.api_key = api_key
        self.private_key = private_key
        # Wallet is computed automatically from private_key (if provided)
        self.wallet = None
        if private_key:
            try:
                self.wallet = get_wallet_address(private_key)
                logger.info(f"Wallet address derived: {self.wallet}")
            except Exception as e:
                logger.error(f"Failed to derive wallet from private key: {e}")
                # Only log the error but don't raise an exception - only check when wallet is needed
        
        # Base URL is fixed
        self.base_url = "https://api.liberalalpha.com"
        self._lock = threading.Lock()
        self.channel = None
        self.stub = None
        
        # Don't try to connect during initialization - only connect when runner is needed
        # This way users can provide just api_key/private_key without needing a local runner
    
    def _ensure_runner_connection(self):
        """Ensure connection to runner is established, attempt to connect if not already connected"""
        if self.stub is not None:
            return True
            
        try:
            self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
            self.stub = service_pb2_grpc.JsonServiceStub(self.channel)
            # Set short timeout to quickly check if runner is available
            grpc.channel_ready_future(self.channel).result(timeout=3)
            logger.info(f"Successfully connected to gRPC server at {self.host}:{self.port}")
            return True
        except (grpc.RpcError, grpc.FutureTimeoutError) as e:
            error_msg = f"Cannot connect to Liberal Runner ({self.host}:{self.port}). "
            error_msg += "Please ensure the runner is installed and running. To install the runner, visit: https://capybaralabs.gitbook.io/liberal-alpha"
            logger.error(error_msg)
            raise ConnectionError(message=error_msg, details=str(e))
    
    def send_data(self, identifier: str, data: dict, record_id: str):
        """
        Send data via gRPC to the Liberal Runner.
        
        This method requires that a local runner is installed and running.
        The runner will receive your data and forward it to the backend.
        
        Args:
            identifier (str): Unique identifier for this data entry
            data (dict): Data payload to send
            record_id (str): ID of the record to store data against
            
        Returns:
            dict: Response from the runner
            
        Raises:
            ConnectionError: If no runner is running or cannot be reached
            RequestError: If the request fails or contains invalid data
            ConfigurationError: If required parameters are missing
        """
        # Try to connect to runner
        self._ensure_runner_connection()
            
        try:
            return self._send_request(identifier, data, "raw", record_id)
        except grpc.RpcError as e:
            error_msg = "Failed to send gRPC request. "
            error_msg += "Please make sure Liberal Runner is installed and running. "
            if isinstance(e, grpc.Call):
                error_msg += f"Error: {e.details()}"
            else:
                error_msg += f"Error: {str(e)}"
            
            raise RequestError(
                message=error_msg,
                code=e.code().value if hasattr(e, 'code') else None,
                details=str(e)
            )
    
    def send_alpha(self, identifier: str, data: dict, record_id: str):
        """
        Send alpha signal via gRPC to the Liberal Runner.
        
        This method requires that a local runner is installed and running.
        The runner will receive your alpha signal and forward it to the backend.
        
        Args:
            identifier (str): Unique identifier for this alpha entry
            data (dict): Alpha data payload to send
            record_id (str): ID of the record to store data against
            
        Returns:
            dict: Response from the runner
            
        Raises:
            ConnectionError: If no runner is running or cannot be reached
            RequestError: If the request fails or contains invalid data
            ConfigurationError: If required parameters are missing
        """
        # Try to connect to runner
        self._ensure_runner_connection()
            
        try:
            return self._send_request(identifier, data, "raw", record_id)
        except grpc.RpcError as e:
            error_msg = "Failed to send gRPC request. "
            error_msg += "Please make sure Liberal Runner is installed and running. "
            if isinstance(e, grpc.Call):
                error_msg += f"Error: {e.details()}"
            else:
                error_msg += f"Error: {str(e)}"
                
            raise RequestError(
                message=error_msg,
                code=e.code().value if hasattr(e, 'code') else None,
                details=str(e)
            )
    
    def _send_request(self, identifier: str, data: dict, event_type: str, record_id: str):
        # Check runtime environment
        if not self.host or not self.port:
            raise ConfigurationError("Missing host and port parameters. To send data, you need to specify the host and port of the runner.")
        
        # Check if stub is available
        if not self.stub:
            raise ConnectionError("No gRPC connection available. Please ensure Liberal Runner is started and reinitialize the client.")
        
        with self._lock:
            current_time_ms = int(time.time() * 1000)
            metadata = {
                "source": "liberal_alpha_sdk",
                "entry_id": identifier,
                "record_id": record_id,
                "timestamp_ms": str(current_time_ms)
            }
            request = service_pb2.JsonRequest(
                json_data=json.dumps(data),
                event_type=event_type,
                timestamp=current_time_ms,
                metadata=metadata
            )
            try:
                response = self.stub.ProcessJson(request)
                logger.info(f"gRPC Response: {response}")
                return {
                    "status": response.status,
                    "message": response.message,
                    "result": json.loads(response.result_json) if response.result_json else None,
                    "error": response.error if response.error else None
                }
            except grpc.RpcError as e:
                # Provide clearer error messages
                if e.code() == grpc.StatusCode.UNAVAILABLE:
                    raise ConnectionError(
                        message="Cannot connect to runner. Please ensure the runner is running.",
                        details=str(e)
                    )
                elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                    raise RequestError(
                        message="Request timed out. The runner may be overloaded or not responding.",
                        code=e.code().value,
                        details=str(e)
                    )
                else:
                    # For other error types, pass through
                    raise
    
    def subscribe_data(self, record_id=None, max_reconnect=5, on_message: callable = None):
        """
        Subscribe to real-time data via WebSocket.
        
        This method allows you to receive real-time data from the Liberal Alpha backend.
        It requires both API key and private key to be provided during initialization.
        
        Args:
            record_id (int, optional): Specific record ID to subscribe to. If not provided,
                                      automatically subscribes to all records the user has access to.
            max_reconnect (int, optional): Maximum number of reconnection attempts. Default is 5.
            on_message (callable, optional): Callback function to handle received messages.
            
        Note:
            This method requires both api_key and private_key to be set during client initialization.
            Unlike send_data and send_alpha, this method does NOT require a local runner.
        """
        if not self.api_key:
            error_msg = "Missing API key. Subscribing to data requires an API key. "
            error_msg += "Please provide the api_key parameter when initializing the client."
            logger.error(error_msg)
            raise ConfigurationError(error_msg)
            
        if not self.private_key:
            error_msg = "Missing private key. Subscribing to data and decrypting messages requires a private key. "
            error_msg += "Please provide the private_key parameter when initializing the client."
            logger.error(error_msg)
            raise ConfigurationError(error_msg)
            
        try:
            # Different handling for different Python versions
            if sys.version_info >= (3, 7):
                # Python 3.7+ has proper asyncio.run
                asyncio.run(
                    main_async(api_key=self.api_key, base_url=self.base_url, wallet_address=self.wallet,
                            private_key=self.private_key, record_id=record_id,
                            max_reconnect=max_reconnect, on_message=on_message)
                )
            else:
                # For Python 3.6, use a different method
                loop = asyncio.get_event_loop()
                try:
                    loop.run_until_complete(
                        main_async(api_key=self.api_key, base_url=self.base_url, wallet_address=self.wallet,
                                private_key=self.private_key, record_id=record_id,
                                max_reconnect=max_reconnect, on_message=on_message)
                    )
                finally:
                    # Cleanup
                    if hasattr(loop, 'is_running') and not loop.is_running():
                        loop.close()
        except KeyboardInterrupt:
            logger.info("Subscription interrupted by user")
        except Exception as e:
            logger.error(f"Error during subscription: {e}")
            raise
    
    def my_records(self):
        """
        Fetch the records associated with the current API key.
        
        This method makes an HTTP GET request to the backend endpoint /api/records
        using your API key for authentication.
        
        Returns:
            dict: The records in JSON format, or None if fetching fails.
            
        Note:
            This method requires an API key to be set during client initialization.
            It does NOT require a local runner.
        """
        if not self.api_key:
            error_msg = "Missing API key. Fetching records requires an API key. "
            error_msg += "Please provide the api_key parameter when initializing the client."
            logger.error(error_msg)
            raise ConfigurationError(error_msg)
            
        url = f"{self.base_url}/api/records"
        headers = {"X-API-Key": self.api_key}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                records = response.json()
                return records
            else:
                error_msg = f"Failed to fetch records: HTTP {response.status_code}"
                if response.text:
                    error_msg += f" - {response.text}"
                logger.error(error_msg)
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error when fetching records: {e}")
            return None
        
    def my_subscriptions(self):
        """
        Fetch the subscriptions associated with the current API key.
        
        This method makes an HTTP GET request to the backend endpoint /api/subscriptions
        using your API key for authentication.
        
        Returns:
            dict: The subscriptions in JSON format, or None if fetching fails.
            
        Note:
            This method requires an API key to be set during client initialization.
            It does NOT require a local runner.
        """
        if not self.api_key:
            error_msg = "Missing API key. Fetching subscription information requires an API key. "
            error_msg += "Please provide the api_key parameter when initializing the client."
            logger.error(error_msg)
            raise ConfigurationError(error_msg)
            
        url = f"{self.base_url}/api/subscriptions"
        headers = {"X-API-Key": self.api_key}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                subscriptions = response.json()
                return subscriptions
            else:
                error_msg = f"Failed to fetch subscription information: HTTP {response.status_code}"
                if response.text:
                    error_msg += f" - {response.text}"
                logger.error(error_msg)
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error when fetching subscription information: {e}")
            return None

    def my_historical_entries(self, record_id: int, page: int = 1, page_size: int = 10):
        """
        Fetch historical subscription data (entries) for a given record and decrypt the data if possible.
        
        Args:
            record_id (int): The record ID for which to fetch historical data.
            page (int): The page number (default is 1).
            page_size (int): Number of entries per page (default is 10).

        Returns:
            dict or None: Parsed JSON data with decrypted values if success; otherwise, None.
        """

        if not self.api_key:
            logger.error("API key is required to fetch historical entries.")
            return None

        # Delegate to utils.fetch_historical_entries
        result = fetch_historical_entries(
            self.base_url,
            self.api_key,
            record_id,
            page=page,
            page_size=page_size
        )

        if result is None:
            return None

        # If no private key or entries not encrypted, return raw result
        if not self.private_key:
            return result

                # Decrypt or return raw based on is_encrypted flag
        decrypted_entries = []
        for entry in result.get('entries', []):
            # if entry marked encrypted and we have a private key, attempt decryption
            if entry.get('is_encrypted') and self.private_key:
                try:
                    # raw data lives in entry['data'] or entry['raw_data']
                    raw = entry.get('data') or entry.get('raw_data')
                    decrypted = decrypt_alpha_message(self.private_key, raw)
                    entry['decrypted_data'] = decrypted
                except Exception:
                    entry['decrypted_data'] = None
            # else leave original data intact for plaintext entries
            decrypted_entries.append(entry)
        result['entries'] = decrypted_entries
        return result


# Global instance for simplified usage
liberal = None

def initialize(host=None, port=None, rate_limit_enabled=None, api_key=None, private_key=None):
    """
    Initialize the global Liberal Alpha client instance.
    
    This function creates a global client instance that can be imported and used
    across your application without having to pass the client around.
    
    Args:
        host (str, optional): Host address of the Liberal Runner. Default is "127.0.0.1".
        port (int, optional): Port number of the Liberal Runner. Default is 8128.
        rate_limit_enabled (bool, optional): Whether to enable rate limiting. Default is True.
        api_key (str, optional): Your Liberal Alpha API key. Required for subscriptions and fetching records.
        private_key (str, optional): Your Ethereum private key. Required for decrypting subscription data.
        
    Note:
        - If you only need to fetch records or subscriptions, only api_key is required.
        - If you need to subscribe to data, both api_key and private_key are required.
        - If you need to send data to a runner, host and port must point to a running Liberal Runner.
    """
    global liberal
    try:
        liberal = LiberalAlphaClient(host, port, rate_limit_enabled, api_key, private_key)
        logger.info(f"SDK initialized: liberal={liberal}")
        return liberal
    except Exception as e:
        logger.error(f"Failed to initialize SDK: {e}")
        print(f"ERROR: Failed to initialize Liberal Alpha SDK: {e}")
        liberal = None
        # Re-raise to allow caller to handle
        raise

def main():
    """Command-line interface for Liberal Alpha SDK"""
    parser = argparse.ArgumentParser(
        prog="liberal_alpha",
        description="Liberal Alpha CLI - interact with gRPC backend & WebSocket stream"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Send data
    send_parser = subparsers.add_parser("send", help="Send data via gRPC")
    send_parser.add_argument("--id", required=True, help="Record ID (entry_id)")
    send_parser.add_argument("--data", required=True, help="Data in JSON format")
    send_parser.add_argument("--record", required=True, help="Record ID")

    # Show records
    subparsers.add_parser("records", help="List your records")

    # Show subscriptions
    subparsers.add_parser("subscriptions", help="List your subscriptions")

    # Subscribe
    sub_parser = subparsers.add_parser("subscribe", help="Subscribe to data")
    sub_parser.add_argument("--record", help="Specific record ID (optional)")

    # Fetch historical entries
    history_parser = subparsers.add_parser("history", help="Fetch historical subscription data for a record")
    history_parser.add_argument("--record", required=True, help="Record ID")
    history_parser.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    history_parser.add_argument("--page-size", type=int, default=10, help="Number of entries per page (default: 10)")

    # Show version
    subparsers.add_parser("version", help="Show CLI version")

    # Show system info
    subparsers.add_parser("info", help="Show system information")

    args = parser.parse_args()

    # Read API key and private key from environment variables
    api_key = os.environ.get("LIBALPHA_API_KEY")
    private_key = os.environ.get("LIBALPHA_PRIVATE_KEY")

    # Print initial CLI header
    print("\n=== Liberal Alpha CLI ===")
    print(f"Version: 0.1.8")
    
    # Initialize client
    try:
        global liberal
        
        if args.command == "info":
            # Just show system information without connecting
            print("\nSystem Information:")
            print(f"Python Version: {platform.python_version()}")
            print(f"Platform: {platform.platform()}")
            print(f"Host: {platform.node()}")
            
            # Check if API key and private key are set
            print("\nConfiguration Status:")
            print(f"API Key: {'Set' if api_key else 'Not set'}")
            print(f"Private Key: {'Set' if private_key else 'Not set'}")
            
            # Show connection requirements for different operations
            print("\nConnection Requirements:")
            print(" - To send data: Need to run Liberal Runner locally")
            print(" - To fetch records/subscriptions: Need API key only")
            print(" - To subscribe to data: Need both API key and private key")
            sys.exit(0)
        
        # For sending data, we need host/port (local runner)
        if args.command == "send":
            initialize(api_key=api_key, private_key=private_key)
        else:
            # For other commands, we don't need to connect to runner
            initialize(host=None, port=None, api_key=api_key, private_key=private_key)
        
        if not liberal:
            print("ERROR: Failed to initialize Liberal Alpha SDK")
            sys.exit(1)
            
    except ConnectionError as e:
        if args.command == "send":
            print(f"ERROR: {str(e)}")
            print("\nTo send data, you need to install and run the Liberal Runner:")
            print("1. Read doc from https://capybaralabs.gitbook.io/liberal-alpha")
            print("2. Run it with your API key")
            print("3. Try this command again")
            sys.exit(1)
        else:
            # For commands that don't need runner, continue without it
            initialize(host=None, port=None, api_key=api_key, private_key=private_key)
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

    try:
        if args.command == "send":
            data = json.loads(args.data)
            result = liberal.send_data(identifier=args.id, data=data, record_id=args.record)
            print("✅ Send result:", json.dumps(result, indent=2))

        elif args.command == "records":
            if not api_key:
                print("ERROR: API key is required to fetch records")
                print("Set the LIBALPHA_API_KEY environment variable and try again")
                sys.exit(1)
                
            records = liberal.my_records()
            print(json.dumps(records, indent=2) if records else "No records found.")

        elif args.command == "subscriptions":
            if not api_key:
                print("ERROR: API key is required to fetch subscriptions")
                print("Set the LIBALPHA_API_KEY environment variable and try again")
                sys.exit(1)
                
            subs = liberal.my_subscriptions()
            print(json.dumps(subs, indent=2) if subs else "No subscriptions found.")

        elif args.command == "subscribe":
            if not api_key:
                print("ERROR: API key is required to subscribe to data")
                print("Set the LIBALPHA_API_KEY environment variable and try again")
                sys.exit(1)
                
            if not private_key:
                print("ERROR: Private key is required to decrypt subscription data")
                print("Set the LIBALPHA_PRIVATE_KEY environment variable and try again")
                sys.exit(1)
                
            print(f"Subscribing to data{f' for record {args.record}' if args.record else ''}...")
            print("Press Ctrl+C to stop")
            liberal.subscribe_data(record_id=args.record)

        elif args.command == "history":
            if not api_key:
                print("ERROR: API key is required to fetch historical data")
                print("Set the LIBALPHA_API_KEY environment variable and try again")
                sys.exit(1)
                
            try:
                record_id = int(args.record)
            except ValueError:
                print("ERROR: Record ID must be an integer")
                sys.exit(1)
                
            print(f"Fetching historical data for record {record_id}...")
            historical_data = liberal.my_historical_entries(record_id, page=args.page, page_size=args.page_size)
            if historical_data:
                print(json.dumps(historical_data, indent=2))
            else:
                print("No historical data found or an error occurred")

        elif args.command == "version":
            print("Liberal Alpha CLI v0.1.8")
            print(f"Python Version: {platform.python_version()}")

        else:
            parser.print_help()
            
    except ConnectionError as e:
        print(f"ERROR: Connection problem - {str(e)}")
        sys.exit(1)
    except RequestError as e:
        print(f"ERROR: Request failed - {str(e)}")
        sys.exit(1)
    except ConfigurationError as e:
        print(f"ERROR: Configuration problem - {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()