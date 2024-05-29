# Wait for kafka to be ready, sleep 5s
sleep 10
# Initialize kafka topics if it does not exist
python -m worker.main