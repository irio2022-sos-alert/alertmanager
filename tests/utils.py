import requests


def call_datamanager_api(
    endpoint,
    service_name,
    service_url,
    frequency,
    alerting_window,
    allowed_resp_time,
    email1,
    email2,
) -> requests.Response:
    endpoint += f"/change_service/{service_name}"
    params = {
        "url": service_url,
        "frequency": frequency,
        "alerting_window": alerting_window,
        "allowed_resp_time": allowed_resp_time,
        "email1": email1,
        "email2": email2,
    }
    response = requests.post(endpoint, params=params)
    return response
