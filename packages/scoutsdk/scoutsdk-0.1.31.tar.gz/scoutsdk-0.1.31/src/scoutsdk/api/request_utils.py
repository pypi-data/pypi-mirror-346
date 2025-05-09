import json
import requests
from typing import Any, Optional, Tuple


class RequestUtils:
    @staticmethod
    def post(
        url: str,
        headers: dict,
        json_payload: Optional[dict] = None,
        data: Optional[dict] = None,
        files: Optional[dict] = None,
        stream: bool = False,
    ) -> Tuple[Any, int]:
        if files is not None and json_payload is not None:
            data = {"json_payload": json.dumps(json_payload)}
            json_payload = None

        response = requests.post(
            url=url, headers=headers, files=files, json=json_payload, data=data
        )
        return RequestUtils._process_response(response, stream=stream)

    @staticmethod
    def put(
        url: str,
        headers: dict,
        payload: Optional[dict] = None,
    ) -> Tuple[Any, int]:
        response = requests.put(url=url, headers=headers, json=payload)
        return RequestUtils._process_response(response)

    @staticmethod
    def get(
        url: str,
        headers: dict,
        stream: bool = False,
        params: Optional[dict] = None,
    ) -> Tuple[Any, int]:
        response = requests.get(url=url, headers=headers, params=params)
        return RequestUtils._process_response(response, stream=stream)

    @staticmethod
    def delete(
        url: str,
        headers: dict,
        json_payload: Optional[dict] = None,
    ) -> Tuple[Any, int]:
        response = requests.delete(url=url, headers=headers, json=json_payload)
        return RequestUtils._process_response(response)

    @staticmethod
    def _process_response(
        response: requests.Response,
        stream: bool = False,
    ) -> Tuple[Any, int]:
        try:
            response.raise_for_status()
            if stream:
                return (
                    RequestUtils._handle_stream_response(response=response),
                    response.status_code,
                )
            else:
                return (response.json(), response.status_code)
        except Exception as e:
            print(f"Error processing response: {e}")
            response_content = response.content.decode("utf-8")
            print(f"Response content: {response_content}")
            error_message = f"{str(e)}\n{response_content}"
            raise type(e)(error_message) from e

    @staticmethod
    def _handle_stream_response(
        response: requests.Response,
    ) -> Any:
        try:
            accumulated_current_data = ""
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    current_data = accumulated_current_data + chunk.decode(
                        "utf-8"
                    ).replace(r":\n\n", "")
                    accumulated_current_data = ""

                    if not current_data.endswith("\n"):
                        accumulated_current_data += current_data
                        continue

                    if not current_data:
                        continue

                    chunks = current_data.split("\n")
                    received_stream_chunks = [
                        json.loads(chunk) for chunk in chunks if chunk
                    ]

                    # only return the last chunk if the stream is finished
                    for received_chunk in received_stream_chunks:
                        if received_chunk.get("finish_reason") == "stop":
                            return received_chunk

        except Exception as e:
            print(e)

        return {}
