"""Description: This file contains the code to retrieve and generate
use the Amazon Bedrock retrieveAndGenerate API  to retrieve
and generate responses from the knowledge base"""
import os
import boto3
import boto3.session
from botocore.client import Config


def invoke_retrieve_generate(user_input, kb_id, model_id, max_tokens,
                             temperature, top_p, max_results,
                             session_id=None, region_id='us-west-2'):
    """Invokes the retrieve and generate operation using the Bedrock client."""
    kb_id = os.getenv("KB_ID")
    print('kb_id:', kb_id)

    bedrock_config = Config(connect_timeout=120,
                            read_timeout=120,
                            retries={'max_attempts': 0})
    bedrock_agent_client = boto3.client("bedrock-agent-runtime",
                                        config=bedrock_config,
                                        region_name=region_id)
    model_arn = f'arn:aws:bedrock:{region_id}::foundation-model/{model_id}'
    if session_id:
        return bedrock_agent_client.retrieve_and_generate(
            input={
                'text': user_input
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': kb_id,
                    'modelArn': model_arn,
                    'generationConfiguration': {
                        'inferenceConfig': {
                            'textInferenceConfig': {
                                'maxTokens': max_tokens,
                                'temperature': temperature,
                                'topP': top_p
                            }
                        }
                    },
                    'retrievalConfiguration': {
                        'vectorSearchConfiguration': {
                            'numberOfResults': max_results
                        }
                    }
                }
            },
            session_id=session_id
        )
    else:
        return bedrock_agent_client.retrieve_and_generate(
            input={
                'text': user_input
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': kb_id,
                    'modelArn': model_arn,
                    'generationConfiguration': {
                        'inferenceConfig': {
                            'textInferenceConfig': {
                                'maxTokens': max_tokens,
                                'temperature': temperature,
                                'topP': top_p
                            }
                        }
                    },
                    'retrievalConfiguration': {
                        'vectorSearchConfiguration': {
                            'numberOfResults': max_results
                        }
                    }
                }
            }
        )
