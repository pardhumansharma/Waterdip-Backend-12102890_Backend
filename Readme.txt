*~Running Your Application~*
Install Dependencies: Run pip install -r requirements.txt.
Run the Application: Execute python app.py.
Run Tests: In a separate terminal, ensure the server is running and execute python test.py.
*Explanation*
Models: The Task model contains the properties of each task, including an auto-incrementing ID.
Schemas: Pydantic schemas are used for input validation and output formatting.
Endpoints: The application includes all required CRUD operations, bulk add, and bulk delete functionalities.
Testing: Simple tests validate the core functionalities using the requests library.