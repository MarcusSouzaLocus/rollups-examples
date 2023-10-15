# Copyright 2022 Cartesi Pte. Ltd.
#
# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from os import environ
import model
import json
import traceback
import logging
import requests

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

def hex2str(hex):
    """
    Decodes a hex string into a regular string
    """
    return bytes.fromhex(hex[2:]).decode("utf-8")

def str2hex(str):
    """
    Encodes a string as a hex string
    """
    return "0x" + str.encode("utf-8").hex()


def calculate_aqi(concentrations):
    """
       Calculates a simple Air Quality index by calculating the mean of sum of the values predicted for the core pollutants
    """
    aqi = sum(concentrations) / len(concentrations)
    return aqi

def categorize_aqi(aqi):
    """
           Categorizes the AQI Calculated in the Standard Air quality ranges from good to hazardous
    """
    if aqi <= 50:
        return 'Good'
    elif aqi <= 100:
        return 'Moderate'
    elif aqi <= 150:
        return 'Bad for sensible groups!'
    elif aqi <= 200:
        return 'Bad'
    elif aqi <= 300:
        return 'Very Bad'
    else:
        return 'Dangerous'


def format(input):
    """
    Transforms a given input so that it is in the format expected by the model
    """
    output = list(input.values())
    return output

def handle_advance(data):
    logger.info(f"Received advance request data {data}")

    status = "accept"
    try:
        # retrieves input as string
        input = hex2str(data["payload"])
        logger.info(f"Received input: '{input}'")

        # converts input to the format expected by the m2cgen model
        input_json = json.loads(input)
        input_formatted = format(input_json)

        # computes predicted classification for input        
        predicted = categorize_aqi(calculate_aqi(model.score(input_formatted)))
        logger.info(f"Data={input}, Predicted: {predicted}")

        # emits output notice with predicted class name
        output = str2hex(str(predicted))
        logger.info(f"Adding notice with payload: {predicted}")
        response = requests.post(rollup_server + "/notice", json={"payload": output})
        logger.info(f"Received notice status {response.status_code} body {response.content}")

    except Exception as e:
        status = "reject"
        msg = f"Error processing data {data}\n{traceback.format_exc()}"
        logger.error(msg)
        response = requests.post(rollup_server + "/report", json={"payload": str2hex(msg)})
        logger.info(f"Received report status {response.status_code} body {response.content}")

    return status

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    logger.info("Adding report")
    response = requests.post(rollup_server + "/report", json={"payload": data["payload"]})
    logger.info(f"Received report status {response.status_code}")
    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
