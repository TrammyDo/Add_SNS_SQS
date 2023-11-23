from tkinter import *
import boto3

def clicked():
  lbl.configure(text = "I just got clicked")

def createTopic (sns, topicName):
  return sns.create_topic (
    Name = topicName
  )

def createQueue (sqs, queueName):
  return sqs.create_queue(
    QueueName=queueName, 
    Attributes={'DelaySeconds': '5'}
  )

sns = boto3.client('sns')
sqs = boto3. resource('sqs')

topic = createTopic (sns, "Add")
queue = createQueue (sqs, 'AddingQueue')

root = Tk()

root.title("Add numbers using AWS SNS and SQS!")
root.geometry('350x200')

lbl = Label(root, text = "Input a number")
lbl.grid()

txt = Entry(root, width=10)
txt.grid(column =1, row =0)

btn = Button(root, text = "Add" , fg = "red", command=clicked)
btn.grid(column=2, row=0)

res = Label(root, text = "Res: 0")
res.grid(column=0, row = 2)

root.mainloop()