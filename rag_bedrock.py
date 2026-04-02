import os
import streamlit as st
import boto3
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Knowledge Base Chat", page_icon="💬")
st.title("Asian Paints POSH Policy Knowledge Base Chat")

client = boto3.client(
    "bedrock-agent-runtime",
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
knowledge_base_id = 'RUNDKIAWXF' 
model_arn = "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"

st.write("Ask a question to your Amazon Bedrock Knowledge Base.")

question = st.text_input("Enter your question")

if st.button("Ask"):
    if not knowledge_base_id:
        st.error("Set KNOWLEDGE_BASE_ID as an environment variable.")
    elif not model_arn:
        st.error("Set MODEL_ARN as an environment variable.")
    elif not question.strip():
        st.error("Please enter a question.")
    else:
        client = boto3.client("bedrock-agent-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))

        response = client.retrieve_and_generate(
            input={"text": question},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": knowledge_base_id,
                    "modelArn": model_arn,
                },
            },
        )

        answer = response["output"]["text"]
        st.subheader("Answer")
        st.write(answer)


print("ENV KEY:", os.getenv("AWS_ACCESS_KEY_ID"))
print("ENV SECRET:", os.getenv("AWS_SECRET_ACCESS_KEY"))
print("ENV REGION:", os.getenv("AWS_REGION"))