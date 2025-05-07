import os
import yaml
import requests
import pytest
import allure
from api_ninja.core import APINinja

# Load YAML config
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, "config.yaml")

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

openapi_spec = {}
if "openapi_spec" in config.get("api", {}):
    openapi_spec = requests.get(config["api"]["openapi_spec"]).json()

api_base_url = config["api"]["base_url"]
defaults = config.get("defaults", [])

ninja = APINinja(openapi_spec=openapi_spec, api_base_url=api_base_url)

test_flows = []
for collection_name, collection in config["collections"].items():
    for flow_id in collection["flows"]:
        flow = config["flows"][flow_id]
        test_flows.append(
            {
                "flow_id": flow_id,
                "description": flow.get("description", "").strip(),
                "expectations": flow.get("expectations", "").strip(),
                "notes": flow.get("notes", "").strip(),
                "collection": collection_name,
                "collection_description": collection.get("description", "").strip(),
                "defaults": defaults,
            }
        )


@pytest.mark.parametrize("flow", test_flows)
def test_api_flow(flow):
    allure.dynamic.epic(flow["collection"])
    allure.dynamic.feature(flow["flow_id"])
    # allure.dynamic.story(flow["flow_id"])
    ninja.plan_and_run(flow)
