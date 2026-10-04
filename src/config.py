from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración central, leída desde variables de entorno o el archivo .env."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Scraping
    base_url: str = "https://www.bbva.com.co"
    max_pages: int = 150
    request_delay: float = 1.0
    request_timeout: int = 15
    raw_dir: str = "data/raw"
    clean_dir: str = "data/clean"

    # Indexación
    chunk_size: int = 800
    chunk_overlap: int = 120
    embedding_model: str = "intfloat/multilingual-e5-base"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "bbva_docs"

    # RAG
    top_k: int = 8
    rerank_top_n: int = 4
    n_history: int = 6

    # LLM
    llm_provider: str = "groq"
    llm_model: str = "llama-3.1-8b-instant"
    groq_api_key: str = ""

    # Historial
    history_db_path: str = "data/history.db"


settings = Settings()