# FastAPI CRUD Patient Data Project

This project is a learning exercise using FastAPI to perform CRUD (Create, Read, Update, Delete) operations on patient data stored in a JSON file.

## Features

- RESTful API for managing patient records
- Endpoints to create, read, update, and delete patients
- Data stored in `patients.json`
- Built with FastAPI and Pydantic

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd FastApi-project
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install "fastapi[standard]" pydantic uvicorn
   ```

## Running the Application

Start the FastAPI server with:

```bash
source my_env/bin/activate
```

```bash
fastapi dev main.py
'OR'
uvicorn main:app --reload
```

- The API will be available at: `http://127.0.0.1:8000`
- Interactive API docs: `http://127.0.0.1:8000/docs`

## Example Endpoints

- `GET /patients` - List all patients
- `GET /patients/{id}` - Get a patient by ID
- `POST /patients` - Add a new patient
- `PUT /patients/{id}` - Update a patient
- `DELETE /patients/{id}` - Delete a patient

## (optional) Containerization with Docker

1. **Build the Docker Image**
```bash
docker build -t fastapi-patient-api .
```

2. **Run the Container with a Custom Name and Port Mapping**
```bash
docker run --name patient-api-container -p 8000:8000 fastapi-patient-api
```

- --name patient-api-container gives your container a friendly name.
- -p 8000:8000 maps your app’s internal port to your host machine.

**To Stop the Running Container, Run:**
```bash
docker stop patient-api-container
```

**To Remove the Container, Run:**
```bash
docker rm patient-api-container
```

## Notes

- Patient data is stored in `patients.json`.
- This project is for learning and demonstration purposes.
