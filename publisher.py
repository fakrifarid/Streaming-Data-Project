import os
import time
import json
import faker

from google.cloud import pubsub_v1

# Create a Faker object
fake = faker.Faker()

# Credential for pub/sub and bigquery
credential = 'you-service-account.json'

# Generate fake data
def generate_data():

    data = {
        "Name": fake.name(),
        "DateOfBirth": fake.date_of_birth().strftime('%Y-%m-%d'),
        "PhoneNumber": fake.phone_number(),
        "Email": fake.email(),
        "Job": fake.job(),
        "Company": fake.company(),
        "CreditCardNo": fake.credit_card_number(),
        "CreditCardExp": fake.credit_card_expire(),
        "DtmUpd": fake.date_time().strftime('%Y-%m-%d %H:%M:%S')
    }
    return data

# Publish the data to Pub/Sub
def publish_data(data, topic_path):
    publisher = pubsub_v1.PublisherClient.from_service_account_json(credential)
    topic_path = publisher.topic_path("streaming-data-project-396608", topic_path)

    json_data = json.dumps(data)

    future = publisher.publish(topic_path, data=json_data.encode("utf-8"))
    future.result()

    print("Published message:\n", data)

# Start looping
if __name__ == "__main__":
    topic_path = "customer"

    while True:
        # Generate fake data
        data = generate_data()

        # Publish the data to Pub/Sub
        publish_data(data, topic_path)

        # Sleep for 1 second
        time.sleep(1)
