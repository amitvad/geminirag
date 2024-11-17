import streamlit as st
from google.cloud import secretmanager
import toml



# Initialize the Secret Manager client
def get_secret(secret_id, project_id):
    client = secretmanager.SecretManagerServiceClient()
    # Construct the resource name of the secret version
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    # Access the secret version
    response = client.access_secret_version(name=name)
    # Get the secret payload and decode it
    secret_value = response.payload.data.decode("UTF-8")
    return secret_value

st.set_page_config(
    page_title="Issue Sphere - Cluster Finder",
    page_icon="🔍"
)

@st.cache_resource
def load_config():
    try:
        return toml.load("config.toml")
    except Exception as e:
        st.error(f"Failed to load configuration: {str(e)}")
        return None
    


def main():
    # Load configuration
    config = load_config()
    if config is None:
        st.error("Cannot proceed without configuration. Please check config.toml file.")
        return

    # Configure page
    try:
        secret_value = get_secret(config["keys"]["secret_id"], config["keys"]["project_id"])
        secret_mongo_uri = get_secret(config["keys"]["secret_id_mongo_uri"], config["keys"]["project_id"])
        st.title(config["app"]["title"])
        st.write("Retrieved Gemini Secret:", secret_value)
        st.write("Retrieved MongoDB Secret:", secret_mongo_uri)
    except Exception as e:
        st.error(f"Error retrieving secret: {e}")

if __name__ == "__main__":
    main()