from azure.core.credentials import AzureKeyCredential
from azure.keyvault.secrets import SecretClient
from openai import AzureOpenAI
import re
import time
import pypdf
from io import BytesIO
from azure.search.documents import SearchClient
from azure.storage.filedatalake import DataLakeServiceClient
from azure.search.documents.indexes import SearchIndexClient
from azure.identity import (DefaultAzureCredential, get_bearer_token_provider)


key_vault_name = 'kv_to-be-replaced'
managed_identity_client_id = 'mici_to-be-replaced'
file_system_client_name = "data"
directory = 'pdf'


def get_secrets_from_kv(kv_name, secret_name):
    # Set the name of the Azure Key Vault
    key_vault_name = kv_name
    credential = DefaultAzureCredential(managed_identity_client_id=managed_identity_client_id)

    # Create a secret client object using the credential and Key Vault name
    secret_client = SecretClient(vault_url=f"https://{key_vault_name}.vault.azure.net/", credential=credential)
    return (secret_client.get_secret(secret_name).value)


search_endpoint = get_secrets_from_kv(key_vault_name, "AZURE-SEARCH-ENDPOINT")
search_key = get_secrets_from_kv(key_vault_name, "AZURE-SEARCH-KEY")
openai_api_base = get_secrets_from_kv(key_vault_name, "AZURE-OPENAI-ENDPOINT")
openai_api_version = get_secrets_from_kv(key_vault_name, "AZURE-OPENAI-PREVIEW-API-VERSION")
deployment = get_secrets_from_kv(key_vault_name, "AZURE-OPEN-AI-DEPLOYMENT-MODEL")


# Function: Get Embeddings
def get_embeddings(text: str, openai_api_base, openai_api_version):
    model_id = "text-embedding-ada-002"
    ad_token_provider = get_bearer_token_provider(
        credential, "https://cognitiveservices.azure.com/.default"
    )
    client = AzureOpenAI(
        api_version=openai_api_version,
        azure_endpoint=openai_api_base,
        azure_ad_token_provider=ad_token_provider
    )

    embedding = client.embeddings.create(input=text, model=model_id).data[0].embedding
    return embedding


# Function: Clean Spaces with Regex -
def clean_spaces_with_regex(text):
    # Use a regular expression to replace multiple spaces with a single space
    cleaned_text = re.sub(r'\s+', ' ', text)
    # Use a regular expression to replace consecutive dots with a single dot
    cleaned_text = re.sub(r'\.{2,}', '.', cleaned_text)
    return cleaned_text


def chunk_data(text):
    tokens_per_chunk = 256  # 1024 # 500
    text = clean_spaces_with_regex(text)

    sentences = text.split('. ')  # Split text into sentences
    chunks = []
    current_chunk = ''
    current_chunk_token_count = 0

    # Iterate through each sentence
    for sentence in sentences:
        # Split sentence into tokens
        tokens = sentence.split()

        # Check if adding the current sentence exceeds tokens_per_chunk
        if current_chunk_token_count + len(tokens) <= tokens_per_chunk:
            # Add the sentence to the current chunk
            if current_chunk:
                current_chunk += '. ' + sentence
            else:
                current_chunk += sentence
            current_chunk_token_count += len(tokens)
        else:
            # Add current chunk to chunks list and start a new chunk
            chunks.append(current_chunk)
            current_chunk = sentence
            current_chunk_token_count = len(tokens)

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


account_name = get_secrets_from_kv(key_vault_name, "ADLS-ACCOUNT-NAME")

account_url = f"https://{account_name}.dfs.core.windows.net"

credential = DefaultAzureCredential()
service_client = DataLakeServiceClient(account_url, credential=credential, api_version='2023-01-03')

file_system_client = service_client.get_file_system_client(file_system_client_name)

directory_name = directory
paths = file_system_client.get_paths(path=directory_name)
print(paths)

index_name = "pdf_index"

search_credential = AzureKeyCredential(search_key)

search_client = SearchClient(search_endpoint, index_name, search_credential)
index_client = SearchIndexClient(endpoint=search_endpoint, credential=search_credential)


def prepare_search_doc(content, document_id):
    chunks = chunk_data(content)
    results = []
    chunk_num = 0
    for chunk in chunks:
        chunk_num += 1
        chunk_id = document_id + '_' + str(chunk_num).zfill(2)

        try:
            v_contentVector = get_embeddings(str(chunk), openai_api_base, openai_api_version)
        except Exception as e:
            print(f"Error occurred: {e}. Retrying after 30 seconds...")
            time.sleep(30)
            try:
                v_contentVector = get_embeddings(str(chunk), openai_api_base, openai_api_version)
            except Exception as e:
                print(f"Retry failed: {e}. Setting v_contentVector to an empty list.")
                v_contentVector = []

        result = {
            "id": chunk_id,
            "chunk_id": chunk_id,
            "content": chunk,
            "sourceurl": path.name.split('/')[-1],
            "contentVector": v_contentVector
        }
        results.append(result)
    return results


# conversationIds = []
docs = []
counter = 0


for path in paths:
    file_client = file_system_client.get_file_client(path.name)
    pdf_file = file_client.download_file()

    stream = BytesIO()
    pdf_file.readinto(stream)
    pdf_reader = pypdf.PdfReader(stream)
    filename = path.name.split('/')[-1]
    document_id = filename.split('_')[1].replace('.pdf', '')

    text = ''
    num_pages = len(pdf_reader.pages)
    for page_num in range(num_pages):

        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    result = prepare_search_doc(text, document_id)
    docs.extend(result)

    counter += 1
    if docs != [] and counter % 10 == 0:
        result = search_client.upload_documents(documents=docs)
        docs = []

if docs != []:
    results = search_client.upload_documents(documents=docs)

print(f'{str(counter)} files processed.')
