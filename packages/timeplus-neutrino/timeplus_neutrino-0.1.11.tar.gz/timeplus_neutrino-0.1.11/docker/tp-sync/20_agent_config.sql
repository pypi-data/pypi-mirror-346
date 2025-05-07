CREATE OR REPLACE FUNCTION agent_config(agent string, base_url string, api_key string, model string) RETURNS string LANGUAGE PYTHON AS 
$$
import traceback
from neutrino.conf import TimeplusAgentConfig


def agent_config(agent, base_url, api_key, model):
    results = []
    for (agent, base_url, api_key, model) in zip(agent, base_url, api_key, model):
        try:
            agent_config = TimeplusAgentConfig()
            agent_config.config(agent, base_url, api_key, model)
            results.append("OK")
        except Exception as e:
            trace = traceback.format_exc()
            results.append(f"failed to update agent config: {e}, {trace}")

    return results

$$;

CREATE OR REPLACE FUNCTION get_agent_config(agent string) RETURNS string LANGUAGE PYTHON AS 
$$
import traceback
import json
from neutrino.conf import TimeplusAgentConfig


def get_agent_config(agent):
    results = []
    for agent in agent:
        try:
            agent_config = TimeplusAgentConfig()
            config = agent_config._get_config(agent)
            del config["api_key"]
            results.append(json.dumps(config))
        except Exception as e:
            trace = traceback.format_exc()
            results.append(f"failed to update agent config: {e}, {trace}")

    return results

$$;
