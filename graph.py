import csv

from matplotlib import pyplot as plt


def total_resp_time(lblc_data, lbrr_data, ss_data):
    plt.clf()
    plt.title("Total response time in sec. vs No of clients")
    plt.xlabel("No of clients.")
    plt.ylabel("Total response time")
    x_points = [i[0] for i in lblc_data]
    y_points_lblc = [float(i[3]) for i in lblc_data]
    y_points_lbrr = [float(i[3]) for i in lbrr_data]
    y_points_ss = [float(i[3]) for i in ss_data]

    plt.plot(x_points, y_points_lblc, color="red", label="Load balancer with least connection")

    plt.plot(x_points, y_points_lbrr, color="hotpink", label="Load balancer with round robin")

    plt.plot(x_points, y_points_ss, color="green", label="Single server")

    plt.legend()
    plt.savefig(f"total_resp_time.png")

def number_of_replicas(lblc_data, lbrr_data):
    plt.clf()
    plt.title("Total number of replicas vs No of clients")
    plt.xlabel("No of clients.")
    plt.ylabel("No of replicas")
    x_points = [i[0] for i in lblc_data]
    y_points_lblc = [int(i[2]) - 4 for i in lblc_data]
    y_points_lbrr = [int(i[2]) - 4 for i in lbrr_data]

    plt.plot(x_points, y_points_lblc, color="red", label="Load balancer with least connection")

    plt.plot(x_points, y_points_lbrr, color="hotpink", label="Load balancer with round robin")

    plt.legend()
    plt.savefig(f"number_of_replicas.png")

with open('loadbalancer_least_connection.csv') as f:
    data = csv.reader(f)
    lblc_data = list(data)
    print(lblc_data)


with open('loadbalancer_round_robin.csv') as f:
    data = csv.reader(f)
    lbrr_data = list(data)
    print(lbrr_data)

with open('single_server_data.csv') as f:
    data = csv.reader(f)
    ss_data = list(data)
    print(ss_data)

total_resp_time(lblc_data, lbrr_data, ss_data)
number_of_replicas(lblc_data, lbrr_data)


