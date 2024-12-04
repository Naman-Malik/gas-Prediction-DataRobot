#!/usr/bin/env bash
echo "Starting App"

# export token="$DATAROBOT_API_TOKEN"
# export endpoint="$DATAROBOT_ENDPOINT"
# export app_base_url_path="$STREAMLIT_SERVER_BASE_URL_PATH"


export token="Njc0ZTk3NzkwMmZlZWJhZmRjNzk2YTA3OkNvOTNUR3Nsek9RaGxwUllHZVJ6QlMxSjVCeFE5TFg4b2lmdURyQU1CWDg9"
export endpoint="https://app.datarobot.com/api/v2"
export app_base_url_path="https://app.datarobot.com/custom_applications/674e977902feebafdc7969fb/"

# If you have configured runtime params via DataRobots application source, the following 2 values should be set automatically.
# Otherwise you will need to set DEPLOYMENT_ID (required) and CUSTOM_METRIC_ID (optional) manually
# if [ -n "$MLOPS_RUNTIME_PARAM_DEPLOYMENT_ID" ]; then
# export deployment_id="673700885c597769d4023037"
# else
#   export deployment_id="$DEPLOYMENT_ID"
# fi
# if [ -n "$MLOPS_RUNTIME_PARAM_CUSTOM_METRIC_ID" ]; then
# export custom_metric_id="6734321c377d29bce4d76c19"

streamlit run --server.port=8090 streamlit_app.py