# Wait for kafka to be ready
# sleep 5
sleep 5
# Run the app
uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-3000}"