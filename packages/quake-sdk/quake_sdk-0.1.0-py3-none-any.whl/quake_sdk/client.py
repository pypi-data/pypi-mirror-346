import requests
import json # For debug printing
import logging # Added for logger
from typing import Optional, Any, Tuple, List, Dict 
from pydantic import ValidationError
from pyrate_limiter import Limiter, BucketFullException, Rate, Duration, InMemoryBucket


from .exceptions import QuakeAPIException, QuakeAuthException, QuakeRateLimitException, QuakeInvalidRequestException, QuakeServerException
from .models import (
    UserInfoResponse, FilterableFieldsResponse,
    ServiceSearchResponse, ServiceScrollResponse, ServiceAggregationResponse,
    HostSearchResponse, HostScrollResponse, HostAggregationResponse,
    SimilarIconResponse, QuakeResponse,
    RealtimeSearchQuery, ScrollSearchQuery, AggregationQuery, FaviconSimilarityQuery
)

class QuakeClient:
    """
    A Python client for the Quake API, using Pydantic for data validation.
    """
    BASE_URL = "https://quake.360.net/api/v3"

    def __init__(self, api_key: str, timeout: int = 30, rate_limiter: Optional[Limiter] = None, logger: Optional[logging.Logger] = None): # Changed debug_raw_response to logger
        """
        Initializes the QuakeClient.

        :param api_key: Your Quake API key.
        :param timeout: Request timeout in seconds.
        :param rate_limiter: An optional pyrate-limiter Limiter instance for client-side rate limiting.
        """
        if not api_key:
            raise ValueError("API key cannot be empty.")
        self.api_key = api_key
        self.timeout = timeout
        
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger("QuakeClient")
            if not self.logger.handlers: # Avoid adding multiple handlers if already configured
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
                self.logger.setLevel(logging.WARNING) # Default to WARNING if not configured by user

        if rate_limiter is None:
            # 如果没有提供速率限制器，则创建一个默认的：每3秒1个请求
            default_rates = [Rate(1, Duration.SECOND * 3)]
            default_bucket = InMemoryBucket(default_rates)
            # 配置 max_delay 以便 try_acquire 可以阻塞等待
            self.rate_limiter = Limiter(default_bucket, max_delay=5000) # 调整为5秒以适应更长的间隔
        else:
            self.rate_limiter = rate_limiter
            
        self._session = requests.Session()
        self._session.headers.update({
            "X-QuakeToken": self.api_key,
            "Content-Type": "application/json"
        })

    def _handle_api_error(self, error_data: dict, http_status_code: int):
        """Helper to raise specific exceptions based on API error codes."""
        code = error_data.get("code")
        message = error_data.get("message", "Unknown API error")

        if code in ["u3004", "u3011"]:  # Specific auth errors
            raise QuakeAuthException(message, code, http_status_code)
        elif code in ["u3005", "q3005"]:  # Rate limit codes
            raise QuakeRateLimitException(message, code, http_status_code)
        elif code in ["u3007", "u3009", "u3010", "u3015", "u3017", "q2001", "q3015", "t6003"]:  # Invalid request codes, added q3015, t6003
            raise QuakeInvalidRequestException(message, code, http_status_code)
        # Add other specific error codes if Quake defines them for server errors etc.
        # For now, any other non-zero code is a generic QuakeAPIException
        raise QuakeAPIException(f"API Error {code}: {message}", code, http_status_code)


    def _request(self, method: str, endpoint: str, response_model: type[QuakeResponse], params: dict = None, json_data: dict = None) -> QuakeResponse: # Return type changed back
        """
        Makes an HTTP request to the Quake API and parses the response.

        :param method: HTTP method (GET, POST).
        :param endpoint: API endpoint path.
        :param response_model: The Pydantic model to parse the response into.
        :param params: URL parameters for GET requests.
        :param json_data: JSON body for POST requests (as dict).
        :return: The parsed Pydantic model response.
        :raises QuakeAPIException: If the API returns an error or response is malformed.
        """
        if self.rate_limiter:
            # This call will block and wait until the item (1 request) can be acquired,
            # if the Limiter is configured with max_delay.
            # Using a common name "quake_api_call" for the item being rate-limited.
            try:
                self.rate_limiter.try_acquire("quake_api_call", 1)
            except BucketFullException as e:
                # This might happen if max_delay is not set or is too short.
                # Re-raise as a QuakeRateLimitException, as the client expects this type.
                # The original exception 'e' contains meta_info about the rate that was hit.
                raise QuakeRateLimitException(
                    f"Client-side rate limit exceeded: {e.meta_info.get('error', 'Bucket full')}", 
                    api_code="CLIENT_RATE_LIMIT", # Custom code for client-side limit
                    response_status_code=None # Not an HTTP error
                ) from e
            # LimiterDelayException could also be raised if max_delay is exceeded.
            # For now, let it propagate or be caught by generic QuakeAPIException if not handled by user.

        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self._session.request(method, url, params=params, json=json_data, timeout=self.timeout)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
                self._handle_api_error(error_data, e.response.status_code)
            except (requests.exceptions.JSONDecodeError, ValueError, KeyError): # If error response is not JSON or doesn't have expected keys
                if e.response.status_code == 401:
                    raise QuakeAuthException(
                        f"Authentication failed: {e.response.status_code} - {e.response.text}",
                        api_code=None, # No API code if JSON parsing failed
                        response_status_code=e.response.status_code
                    )
                else:
                    raise QuakeAPIException(
                        f"HTTP Error: {e.response.status_code} - {e.response.text}",
                        api_code=None, # No API code if JSON parsing failed
                        response_status_code=e.response.status_code
                    )
        except requests.exceptions.RequestException as e: # Catch other request exceptions like ConnectionError
            raise QuakeAPIException(f"Request failed: {e}")

        try:
            response_json = response.json()
        except ValueError: # JSONDecodeError inherits from ValueError
            raise QuakeAPIException(f"Failed to decode JSON response: {response.text}", response_status_code=response.status_code)
        
        # Log raw data if logger is at DEBUG level
        if self.logger.isEnabledFor(logging.DEBUG) and response_model is ServiceSearchResponse and 'data' in response_json:
            try:
                self.logger.debug(
                    "Raw API response data for ServiceSearchResponse:\n%s",
                    json.dumps(response_json['data'], indent=2, ensure_ascii=False)
                )
            except Exception as e:
                self.logger.debug("Could not json.dumps raw API response data: %s. Error: %s", response_json.get('data'), e)


        # Validate and parse the successful response using the provided Pydantic model
        try:
            parsed_response = response_model.model_validate(response_json)
        except ValidationError as e:
            raise QuakeAPIException(f"Failed to validate API response: {e}. Raw response: {response_json}", response_status_code=response.status_code)

        # Check for API-level errors indicated by 'code' field in the successfully parsed response
        if parsed_response.code != 0:
            self._handle_api_error({"code": parsed_response.code, "message": parsed_response.message}, response.status_code)
            # The above will raise, so this part is more for logical completeness
            raise QuakeAPIException(f"API Error {parsed_response.code}: {parsed_response.message}", parsed_response.code, response.status_code)

        return parsed_response # Return type changed back

    def get_user_info(self) -> UserInfoResponse:
        """
        Retrieves the current user's information.
        Endpoint: /user/info
        Method: GET

        :return: UserInfoResponse Pydantic model.
        """
        return self._request("GET", "/user/info", response_model=UserInfoResponse)

    def get_service_filterable_fields(self) -> FilterableFieldsResponse:
        """
        Retrieves the filterable fields for service data.
        Endpoint: /filterable/field/quake_service
        Method: GET

        :return: FilterableFieldsResponse Pydantic model.
        """
        return self._request("GET", "/filterable/field/quake_service", response_model=FilterableFieldsResponse)

    def search_service_data(self, query_params: RealtimeSearchQuery) -> ServiceSearchResponse: # Return type changed back
        """
        Performs a real-time search for service data.
        Endpoint: /search/quake_service
        Method: POST

        :param query_params: RealtimeSearchQuery Pydantic model containing query details.
        :return: ServiceSearchResponse Pydantic model.
        """
        return self._request("POST", "/search/quake_service", response_model=ServiceSearchResponse, json_data=query_params.model_dump(exclude_none=True))

    def scroll_service_data(self, query_params: ScrollSearchQuery) -> ServiceScrollResponse:
        """
        Performs a scroll (deep pagination) search for service data.
        Endpoint: /scroll/quake_service
        Method: POST

        :param query_params: ScrollSearchQuery Pydantic model.
        :return: ServiceScrollResponse Pydantic model.
        """
        return self._request("POST", "/scroll/quake_service", response_model=ServiceScrollResponse, json_data=query_params.model_dump(exclude_none=True))

    def get_service_aggregation_fields(self) -> FilterableFieldsResponse:
        """
        Retrieves the filterable fields for service aggregation data.
        Endpoint: /aggregation/quake_service (GET for fields)
        Method: GET

        :return: FilterableFieldsResponse Pydantic model.
        """
        return self._request("GET", "/aggregation/quake_service", response_model=FilterableFieldsResponse)

    def aggregate_service_data(self, query_params: AggregationQuery) -> ServiceAggregationResponse:
        """
        Performs an aggregation query on service data.
        Endpoint: /aggregation/quake_service (POST for query)
        Method: POST

        :param query_params: AggregationQuery Pydantic model.
        :return: ServiceAggregationResponse Pydantic model.
        """
        return self._request("POST", "/aggregation/quake_service", response_model=ServiceAggregationResponse, json_data=query_params.model_dump(exclude_none=True))

    def get_host_filterable_fields(self) -> FilterableFieldsResponse:
        """
        Retrieves the filterable fields for host data.
        Endpoint: /filterable/field/quake_host
        Method: GET

        :return: FilterableFieldsResponse Pydantic model.
        """
        return self._request("GET", "/filterable/field/quake_host", response_model=FilterableFieldsResponse)

    def search_host_data(self, query_params: RealtimeSearchQuery) -> HostSearchResponse:
        """
        Performs a real-time search for host data.
        Endpoint: /search/quake_host
        Method: POST

        :param query_params: RealtimeSearchQuery Pydantic model.
        :return: HostSearchResponse Pydantic model.
        """
        # Note: Host search doesn't have 'latest' or 'shortcuts' in its documented params
        # RealtimeSearchQuery includes them as optional, they will be excluded if None by model_dump
        host_query_data = query_params.model_dump(exclude_none=True)
        host_query_data.pop('latest', None)
        host_query_data.pop('shortcuts', None)
        return self._request("POST", "/search/quake_host", response_model=HostSearchResponse, json_data=host_query_data)

    def scroll_host_data(self, query_params: ScrollSearchQuery) -> HostScrollResponse:
        """
        Performs a scroll (deep pagination) search for host data.
        Endpoint: /scroll/quake_host
        Method: POST

        :param query_params: ScrollSearchQuery Pydantic model.
        :return: HostScrollResponse Pydantic model.
        """
        # Note: Host scroll doesn't have 'latest' in its documented params
        host_query_data = query_params.model_dump(exclude_none=True)
        host_query_data.pop('latest', None)
        return self._request("POST", "/scroll/quake_host", response_model=HostScrollResponse, json_data=host_query_data)

    def get_host_aggregation_fields(self) -> FilterableFieldsResponse:
        """
        Retrieves the filterable fields for host aggregation data.
        Endpoint: /aggregation/quake_host (GET for fields)
        Method: GET

        :return: FilterableFieldsResponse Pydantic model.
        """
        return self._request("GET", "/aggregation/quake_host", response_model=FilterableFieldsResponse)

    def aggregate_host_data(self, query_params: AggregationQuery) -> HostAggregationResponse:
        """
        Performs an aggregation query on host data.
        Endpoint: /aggregation/quake_host (POST for query)
        Method: POST

        :param query_params: AggregationQuery Pydantic model.
        :return: HostAggregationResponse Pydantic model.
        """
        # Note: Host aggregation doesn't have 'latest' in its documented params
        host_query_data = query_params.model_dump(exclude_none=True)
        host_query_data.pop('latest', None)
        return self._request("POST", "/aggregation/quake_host", response_model=HostAggregationResponse, json_data=host_query_data)

    def query_similar_icons(self, query_params: FaviconSimilarityQuery) -> SimilarIconResponse:
        """
        Performs a favicon similarity search.
        Endpoint: /query/similar_icon/aggregation
        Method: POST

        :param query_params: FaviconSimilarityQuery Pydantic model.
        :return: SimilarIconResponse Pydantic model.
        """
        return self._request("POST", "/query/similar_icon/aggregation", response_model=SimilarIconResponse, json_data=query_params.model_dump(exclude_none=True))

    def close(self):
        """Closes the underlying requests session."""
        if self._session:
            self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
