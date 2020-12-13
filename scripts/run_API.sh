set -e
docker-compose -f API.docker-compose.yml up -d --build
echo ""
echo "API is up and listening in http://localhost:5000/"
echo "POST call /predict endpoint with json body format:"
echo '{
 "form_id": integer,
 "form_features": list of features in string format
}'
echo ""