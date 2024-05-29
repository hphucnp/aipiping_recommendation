# aipiping_recommendation
Recommendation using OpenAI

# AI Recommendations

I chose Prefect from the beginning but somehow managing to use it was taking me time. 
So I decided to use Kafka instead. When it comes to API design, I prefect having all POST APIs,
in which we can have request body for all the requests, and add suffixes like /create, /get, /query, /update


## Setup
```lua
  +---------------+            +-----------------+            +---------------+
  |               |            |                 |            |               |
  |    Clients    +----------->+    FastAPI      +----------->+   MongoDB     |
  |               |            |   Backend       |            |   Database    |
  +---------------+            +-----------------+            +---------------+
           ^                             |
           |                             v
           |                   +-----------------+
           |                   |                 |
           +-------------------+    Kafka        |
                               |   Message Queue |
                               +-----------------+
                                       |
                                       v
                               +-----------------+
                               |                 |
                               |   Asyncio       |
                               |    Worker       |
                               |   (Event Loop)  |
                               +-----------------+

```

1. Clone the repository:
    ```sh
    git clone https://github.com/hphucnp/aipiping_recommendation.git
    cd aipiping_recommendations
    ```

2. Create a `.env` file and set your OpenAI API key (if you do not have one, I can share to you my api key privately over email):
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

3. To build and run the application locally on host, you can bring up all the services, except the backend and worker services:
    ```sh
    docker compose -f docker-compose.yml -f local.docker-compose.yml --profile local-dev up --force-recreate -d --build
    ```

    Then start service  `worker`:
    ```sh
    python -m worker.main
    ```
    Then start service `app`:
    
    ```sh
    uvicorn map.main:app --host 0.0.0.0 --port 3000 --reload
    ```


3. OR, Build and run the whole application inside Docker with Docker Compose:
    ```sh
    docker compose -f docker-compose.yml --profile dev up --force-recreate -d --build
    ```

4. Test using curl (or any API tools: Postman, Imsonia ...)
    - ```sh
      curl -s -X POST "http://localhost:3000/recommendations/create?country=USA&season=summer" | jq
      ```
    - ```sh
      curl -s -X POST "http://localhost:3000/recommendations/80176573-a32b-4a80-b8d4-18724269c776/get" | jq
      ```

## Endpoints

- **POST /recommendations**: Request for a recommendation
    - Query Parameters: `country`, `season`
    - Response: `{"id": "unique_id"}`

- **POST /recommendations/{uid}**: Retrieve  a recommendation by UID
    - Response:
        - If completed: `{"id": "unique_id", "country": "...", "season": "...", "recommendations": ["..."], "status": "completed"}`
        - If pending: `{"id": "unique_id", "status": "pending", "message": "The recommendations are not yet available. Please try again later."}`
        - If not found: `{"error": "NOT_FOUND", "message": "The provided UID does not exist. Please check the UID and try again."}`
- **POST /recommendations**: Retrieve all recommendations (For testing only)
    - Response: `[{"id": "unique_id", "country": "...", "season": "...", "recommendations": ["..."], "status": "completed"} `

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc


## Testing

1. Run the tests with Docker Compose:
    ```sh
    docker-compose -f docker-compose.test.yml up --build
    ```
   
2. To run the tests locally, you can use the following command:
    ```sh
    pytest
    ```
