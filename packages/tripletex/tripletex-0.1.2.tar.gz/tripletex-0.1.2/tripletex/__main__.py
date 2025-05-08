import logging

from tripletex.core.api import TripletexAPI

# Configure root logger
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

crud_logger = logging.getLogger("crudclient")  # Adjust based on module names
crud_logger.setLevel(logging.DEBUG)


def main():
    api = TripletexAPI()
    print(api.countries.list())


if __name__ == "__main__":
    main()
