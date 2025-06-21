from google.auth import default
import vertexai
from vertexai.preview import rag
import os
from dotenv import load_dotenv, set_key

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
CORPUS_DISPLAY_NAME = "Symtoms_Corpus_2025"
CORPUS_DESCRIPTION = "Corpus containing Symtoms 2025 document"

def initialize_vertex_ai():
  credentials, _ = default()
  vertexai.init(
      project=PROJECT_ID, location=LOCATION, credentials=credentials
  )
  
def list_corpus_files(corpus_name):
  """Lists files in the specified corpus."""
  files = list(rag.list_files(corpus_name=corpus_name))
  print(f"Total files in corpus: {len(files)}")
  for file in files:
    print(f"File: {file.display_name} - {file.name}")

def create_or_get_corpus():
  """Creates a new corpus or retrieves an existing one."""
  embedding_model_config = rag.EmbeddingModelConfig(
      publisher_model="publishers/google/models/text-embedding-005"
  )
  existing_corpora = rag.list_corpora()
  corpus = None
  for existing_corpus in existing_corpora:
    if existing_corpus.display_name == CORPUS_DISPLAY_NAME:
      corpus = existing_corpus
      print(f"Found existing corpus with display name '{CORPUS_DISPLAY_NAME}'")
      break
  if corpus is None:
    corpus = rag.create_corpus(
        display_name=CORPUS_DISPLAY_NAME,
        description=CORPUS_DESCRIPTION,
        embedding_model_config=embedding_model_config,
    )
    print(f"Created new corpus with display name '{CORPUS_DISPLAY_NAME}'")
  return corpus

def upload_file_to_corpus(corpus_name, pdf_path, display_name, description):
  """Uploads a txt/pdf file to the specified corpus."""
  print(f"Uploading {display_name} to corpus...")
  try:
    rag_file = rag.upload_file(
        corpus_name=corpus_name,
        path=pdf_path,
        display_name=display_name,
        description=description,
    )
    print(f"Successfully uploaded {display_name} to corpus")
    return rag_file
  except Exception as e:
    print(f"Error uploading file {display_name}: {e}")
    return None

def main():
    initialize_vertex_ai()
    corpus = create_or_get_corpus()

    # Update the .env file with the corpus name
    local_file_path = "C:/Users/phamt/Downloads/data_ask_answer_11.txt" # Set the correct path
    display_name = "data_ask_answer_11.txt" # Set the desired display name
    description = "Ask and answer about disease" # Set the description

    if os.path.exists(local_file_path):
        upload_file_to_corpus(
            corpus_name=corpus.name,
            pdf_path=local_file_path,
            display_name=display_name,
            description=description
        )
    # List all files in the corpus
    list_corpus_files(corpus_name=corpus.name)

if __name__ == "__main__":
  main()