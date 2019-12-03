from django.shortcuts import render
from ibm_watson import DiscoveryV1, AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

#Reference: https://github.com/watson-developer-cloud/python-sdk

WATSON_API_KEY = 'j9qfIjlWczzRcwE6f-mB4WeJPZle4Y_Dy0HP2l-ssPNA'
WATSON_WORKSPACE_ID = 'a4fde77e-8dbd-4f3f-a3d3-9315bb4b9452'
#WATSON_WORKSPACE_ID ='55eae879-4e24-4973-9184-0e1988f8900a'
#cGwu6EjRDqifDY1DFuEYRgYB5nuyiRQN5AEUvK6DFtlQ
#To find out workspace_id:
#j9qfIjlWczzRcwE6f-mB4WeJPZle4Y_Dy0HP2l-ssPNA
#a4fde77e-8dbd-4f3f-a3d3-9315bb4b9452
#ee320c1e-2b8b-4d2f-83d2-4d12daaddf14


'''
print(assistant.list_workspaces(headers={'Custom-Header': 'custom_value'}).get_result())
{
    'workspaces': [{
                    'name': 'Customer Care Sample Skill', 'language': 'en',
                    'metadata': {'api_version': {'major_version': 'v1', 'minor_version': '2018-07-10'}},
                    'description': 'Sample simple customer service skill to get you started.',
                    'workspace_id': '55eae879-4e24-4973-9184-0e1988f8900a',
                    'system_settings': {'tooling': {'store_generic_responses': True},
                    'off_topic': {'enabled': True},
                    'disambiguation': {'prompt': 'Did you mean:', 'enabled': True, 'randomize': True, 'max_suggestions': 5,
                                        'suggestion_text_policy': 'title', 'none_of_the_above_prompt': ''},
                    'spelling_auto_correct': True}, 'learning_opt_out': True
                    }],
    'pagination': {'refresh_url': '/v1/workspaces?version=2018-07-10'}
}
'''
def setup_watson():
    print('Starting Watson Connection...')
    authenticator = IAMAuthenticator(WATSON_API_KEY)
    discovery = DiscoveryV1(version='2018-08-01',
                        authenticator=authenticator)
    discovery.set_service_url('https://gateway-wdc.watsonplatform.net/assistant/api')
    assistant = AssistantV1(
        version='2018-07-10',
        authenticator=authenticator)
    assistant.set_service_url('https://gateway-wdc.watsonplatform.net/assistant/api')
    assistant.set_http_config({'timeout': 100})
    return assistant

assistant = setup_watson()
def ask_watson(msg_txt):
    return(assistant.message(workspace_id=WATSON_WORKSPACE_ID, input={'text': msg_txt}).get_result())
#WATSON_WORKSPACE_ID
'''
Response example:
{
  "intents": [
    {
      "intent": "ibm-action-Customer_Care_Store_Location",
      "confidence": 0.3875014901094005
    }
  ],
  "entities": [],
  "input": {
    "text": "Directions"
  },
  "output": {
    "generic": [
      {
        "response_type": "text",
        "text": "We're located by Union Square on the corner of 13th and Broadway"
      }
    ],
    "text": [
      "We're located by Union Square on the corner of 13th and Broadway"
    ],
    "nodes_visited": [
      "Directions",
      "node_3_1522439390442"
    ],
    "log_messages": []
  },
  "context": {
    "conversation_id": "ef69ed3c-0321-4800-948d-75f0a5d0df5d",
    "system": {
      "initialized": true,
      "dialog_stack": [
        {
          "dialog_node": "root"
        }
      ],
      "dialog_turn_counter": 1,
      "dialog_request_counter": 1,
      "last_suggestions_created_event_id": "fdd9475e-3226-4a30-88d1-4a381f05024c",
      "_node_output_map": {
        "node_3_1522439390442": [
          0
        ]
      },
      "branch_exited": true,
      "branch_exited_reason": "completed"
    }
  }
}
'''
