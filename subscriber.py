import os
import json
from google.cloud import pubsub_v1
from google.cloud import bigquery

# Credential for pub/sub and bigquery
credential = '/Users/fakrifarid/Documents/Streaming-Data/Pub-Sub/streaming-data-project-396608-8de21c2f0b74.json'

# Create a BigQuery client
client = bigquery.Client.from_service_account_json(credential)

def callback(message):
    try:
        # Assuming the message data is in JSON format
        data = json.loads(message.data.decode("utf-8"))

        print(f"Received message: {data}")

        # Insert data into BigQuery
        insert_into_bigquery(data)

        # Acknowledge the message
        message.ack()  # Mark the message as acknowledged

    except Exception as e:
        print(f"Error processing message: {e}")
        # Nacknowledge the message to retry or handle the error

def insert_into_bigquery(data):
    dataset_id = "dataset_example_stg"
    table_id = "customers"

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)

    row = [(data["Name"], data["DateOfBirth"], data["PhoneNumber"], data["Email"], data["Job"], data["Company"], data["CreditCardNo"], data["CreditCardExp"], data["DtmUpd"])]
    errors = client.insert_rows(table, row)

    if row:
        print("Data successfully inserted into BigQuery:\n", row)

if __name__ == "__main__":
    # Create a SubscriberClient
    subscriber = pubsub_v1.SubscriberClient.from_service_account_json(credential)

    # Define the subscription path
    project_id = "streaming-data-project-396608"
    subscription_id = "customer-sub"
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # Subscribe to the subscription and start listening for messages, only for new messages
    subscriber.subscribe(subscription_path, callback=callback)

    # Keep the script running to consume messages
    print("Listening for messages...")
    while True:
        pass
