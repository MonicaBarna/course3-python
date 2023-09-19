import requests
from robocorp import workitems
from robocorp.tasks import task


@task
def consume_traffic_data():
    """
    Inhuman Insurance, Inc. Artificial Intelligence System robot.
    Consumes traffic data work items.
    """
    process_traffic_data()


def process_traffic_data():
    for item in workitems.inputs:
        payload = item.payload
        traffic_data = payload["traffic_data"]
        valid = validate_traffic_data(traffic_data)
        if valid:
            status, return_json = post_traffc_data_to_sales_system(traffic_data)
            if status == 200:
                item.done
            else:
                item.fail(
                    exception_type="APPLICATION",
                    code="TRAFFIC_DATA_POST_FAILED",
                    message=return_json["message"],
                )
        else:
            item.fail(
                exception_type="BUSINESS",
                code="INVALID_TRAFFIC_DATA",
                message=item.payload,
            )


def validate_traffic_data(traffic_data):
    country = traffic_data["country"]
    if len(country) == 3:
        return True
    else:
        return False


def post_traffc_data_to_sales_system(traffic_data):
    url = "https://robocorp.com/inhuman-insurance-inc/sales-system-api"
    response = requests.post(url, json=traffic_data)
    return response.status_code, response.json()
