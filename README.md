# Identifying Similar Address Using Fuzzy Matching And Geo-location

This repository contains a Python application for comparing and searching addresses using text-based and geospatial methods. The application is built with Python's fuzzywuzzy and FastAPI.

## Usage:

1. **Installation**:
   - Clone the repository: `git clone https://github.com/your_username/address-matching-app.git`
   - Install dependencies: `pip install -r requirements.txt`

2. **Running the Application**:
   - Navigate to the repository directory: `cd address-matching-app`
   - Run the FastAPI application: `uvicorn main:app --reload`

3. **Endpoints**:
   - `/compare/`: Compare two addresses using both text-based and geospatial methods.
   - `/search/`: Search for similar addresses in the database based on a provided input address.

4. **Documentation**:
   - [Text Matcher Documentation](./docs/text_matcher.md)
   - [Geo Matcher Documentation](./docs/geo_matcher.md)
   - [FastAPI Documentation](./docs/address_search_fastapi.md)
   - [Utility Functions Documentation](./docs/utility_functions.md)

## Contributors:

- [Your Name](https://github.com/your_username)

## License:

This project is licensed under the [MIT License](LICENSE).

