import os
import logging
from pathlib import Path
import frontmatter
from dotenv import load_dotenv

# Use the logger we know works in your Docker setup
logger = logging.getLogger("orchestrator.loader")
logging.basicConfig(level=logging.INFO)

def initialize_agents() -> dict:
    logger.info("🚀 CEO CORE: STARTING AGENT DISCOVERY")

    # --- 1. Environment Loading ---
    found_env = False
    current_search = Path(__file__).resolve()
    for _ in range(5):
        potential_env = current_search.parent / ".env.local"
        if potential_env.exists():
            load_dotenv(potential_env)
            logger.info(f"🏠 LOCAL: Loaded config from {potential_env}")
            found_env = True
            break
        current_search = current_search.parent
    
    if not found_env:
        logger.warning("⚠️ No .env.local detected. Using system environment variables.")

    # --- 2. The Path Probe ---
    # Standard Docker path is /agents
    agent_env_path = os.getenv("PYTHON_AGENT_PATH", "/agents")
    agents_dir = Path(agent_env_path)

    logger.info(f"📍 Checking directory: {agents_dir.absolute()}")
    
    if not agents_dir.exists():
        logger.error(f"❌ ERROR: {agents_dir} DOES NOT EXIST.")
        return {}

    # --- 3. The Folder Scan ---
    try:
        contents = list(agents_dir.iterdir())
        logger.info(f"📂 FOLDER SCAN: Found {len(contents)} items in {agents_dir}")
        for item in contents:
            logger.info(f"  - Item: {item.name} | Type: {'DIR' if item.is_dir() else 'FILE'}")
    except Exception as e:
        logger.error(f"🚨 Could not list directory {agents_dir}: {e}")
        return {}

    registry = {}
    for md_file in agents_dir.glob("*.md"):
        try:
            agent_data = frontmatter.load(md_file)
            agent_id = md_file.stem
            registry[agent_id] = {
                "config": agent_data.metadata,
                "prompt": agent_data.content,
                "file_path": str(md_file.resolve())
            }
            logger.info(f"🤖 AGENT LOADED: {agent_id}")
        except Exception as e:
            logger.error(f"🚨 FAILED TO PARSE {md_file.name}: {e}")

    logger.info(f"✅ REGISTRY COMPLETE: {len(registry)} agents active.")
    return registry