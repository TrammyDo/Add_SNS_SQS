from tkinter import *
import boto3
import json
import time

def clicked():
  global currSum
  num = str(txt.get())

  response = sns.publish (
    TopicArn = topic["TopicArn"],
    Message = num
  )

  time.sleep (10)

  message = sqsClient.receive_message (
    QueueUrl = queueUrl['QueueUrl'],
    MaxNumberOfMessages = 1
  )

  res = json.loads (message["Messages"][0]["Body"])

  currSum += int(res["Message"])
  resGUI = Label(root, text = f'Result: {currSum}')
  resGUI.grid(column=0, row = 2)

  sqsClient.delete_message (
    QueueUrl = queueUrl['QueueUrl'],
    ReceiptHandle= message["Messages"][0]["ReceiptHandle"]
  )


def createTopic (sns, topicName):
  return sns.create_topic (
    Name = topicName
  )

def createQueue (sqs, queueName):
  return sqs.create_queue(
    QueueName=queueName, 
    Attributes={'DelaySeconds': '5'}
  )

currSum = 0

sns = boto3.client('sns')
sqs = boto3. resource('sqs')

topic = createTopic (sns, "Add")
queue = createQueue (sqs, 'AddingQueue')
sqsClient = boto3.client('sqs')

sns.subscribe (
  TopicArn = topic["TopicArn"],
  Protocol = "sqs",
  Endpoint = queue.attributes["QueueArn"]
)

queueUrl = sqsClient.get_queue_url (
  QueueName = "AddingQueue"
)

root = Tk()

root.title("Add numbers using AWS SNS and SQS!")
root.geometry('350x200')

lbl = Label(root, text = "Input a number")
lbl.grid()

txt = Entry(root, width=10)
txt.grid(column =1, row =0)

btn = Button(root, text = "Add" , fg = "red", command=lambda: clicked ())
btn.grid(column=2, row=0)

res = Label(root, text = "Result: 0")
res.grid(column=0, row = 2)

root.mainloop()