import logging

# Configure logging globally
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler("verdict_tool.log", mode="w"),  # Log file
    ],
)

# Create and expose a single logger instance
logger = logging.getLogger("verdict_tool")
