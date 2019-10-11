# Serverless

# Use Case: 
  API endpoint will take an IAM Access key as query parameter and will check for the user associated with that key. If the key is valid it will create a new key pair and display it. You need to have additional lambda functions for IAM key rotation.
  
  
# Example: 
curl -X GET https://hy2hed7a39.execute-api.us-east-1.amazonaws.com/dev/iam?currentKey=AKIAAHGRBARAKA
