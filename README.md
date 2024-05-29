# aipiping_recommendation
Recommendation using OpenAI

# FastAPI Travel Recommendations

## Setup

1. Clone the repository:
    ```sh
    git clone <repo_url>
    cd aipiping_recommendations
    ```

2. Create a `.env` file and set your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

3. Build and run the application with Docker Compose:
    ```sh
    docker-compose up --build
    ```

## Endpoints

- **POST /api/v1/recommendations**: Request recommendations
    - Query Parameters: `country`, `season`
    - Response: `{"uid": "unique_id"}`

- **GET /api/v1/recommendations/{uid}**: Retrieve recommendations by UID
    - Response:
        - If completed: `{"uid": "unique_id", "country": "...", "season": "...", "recommendations": ["..."], "status": "completed"}`
        - If pending: `{"uid": "unique_id", "status": "pending", "message": "The recommendations are not yet available. Please try again later."}`
        - If not found: `{"error": "UID not found", "message": "The provided UID does not exist. Please check the UID and try again."}`