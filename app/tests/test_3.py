def process(msg, data_array):
    # splits the elements and transform them into floats
    message_nbr = [float(i) for i in msg.split(",")]
    # appends the list to the data_array
    data_array.append(message_nbr)

data_array = []

message1 = "1,20,30,50"
message2 = "2,20,30,50"

process(message1, data_array)
process(message2, data_array)

# prints the first element of the first list of the data_array
print(data_array)
# prints the type of the first element of the first list of the data_array
print(type(data_array[0][0]))
# prints the first element of the message_nbr list


