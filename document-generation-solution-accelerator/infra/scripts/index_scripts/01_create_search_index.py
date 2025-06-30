from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

key_vault_name = 'kv_to-be-replaced'
managed_identity_client_id = 'mici_to-be-replaced'
index_name = "pdf_index"


def get_secrets_from_kv(kv_name, secret_name):
    """Retrieve a secret from Azure Key Vault."""
    key_vault_name = kv_name
    credential = DefaultAzureCredential(
        managed_identity_client_id=managed_identity_client_id
    )
    secret_client = SecretClient(
        vault_url=f"https://{key_vault_name}.vault.azure.net/", credential=credential
    )
    return secret_client.get_secret(secret_name).value


search_endpoint = get_secrets_from_kv(key_vault_name, "AZURE-SEARCH-ENDPOINT")
search_key = get_secrets_from_kv(key_vault_name, "AZURE-SEARCH-KEY")


def create_search_index():
    """Create an Azure Search index."""
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents.indexes.models import (
        SimpleField,
        SearchFieldDataType,
        SearchableField,
        SearchField,
        VectorSearch,
        HnswAlgorithmConfiguration,
        VectorSearchProfile,
        SemanticConfiguration,
        SemanticPrioritizedFields,
        SemanticField,
        SemanticSearch,
        SearchIndex,
    )

    search_credential = AzureKeyCredential(search_key)
    index_client = SearchIndexClient(endpoint=search_endpoint, credential=search_credential)

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="chunk_id", type=SearchFieldDataType.String),
        SearchField(name="content", type=SearchFieldDataType.String),
        SearchableField(name="sourceurl", type=SearchFieldDataType.String),
        SearchField(
            name="contentVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            vector_search_dimensions=1536,
            vector_search_profile_name="myHnswProfile",
        ),
    ]

    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(name="myHnsw")
        ],
        profiles=[
            VectorSearchProfile(
                name="myHnswProfile",
                algorithm_configuration_name="myHnsw",
            )
        ],
    )

    semantic_config = SemanticConfiguration(
        name="my-semantic-config",
        prioritized_fields=SemanticPrioritizedFields(
            keywords_fields=[SemanticField(field_name="chunk_id")],
            content_fields=[SemanticField(field_name="content")],
        ),
    )

    semantic_search = SemanticSearch(configurations=[semantic_config])

    index = SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search,
        semantic_search=semantic_search,
    )
    result = index_client.create_or_update_index(index)
    print(f'{result.name} created')


create_search_index()
