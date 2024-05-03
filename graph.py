import csv

from matplotlib import pyplot as plt


def scaling_plot(data):
    plt.clf()

    fig, ax1 = plt.subplots()
    fig.suptitle("No of replicas vs Total number of successfull requests vs Time in seconds")

    ax2 = ax1.twinx()

    x_points = [int(i[0])*4 for i in data]
    y_points_replicas = [int(i[1])-4 for i in data]
    y_points_reqs = [int(i[2]) for i in data]

    ax1.plot(x_points, y_points_replicas, color="blue", label="Total number of replicas")
    ax2.plot(x_points, y_points_reqs, color="hotpink", label="Total number of successfull requests")

    ax1.set_xlabel("Time in seconds")
    ax1.set_ylabel("No of replicas.")
    ax2.set_ylabel("No of requests.")

    ax1.legend(loc='upper left')
    ax2.legend(loc='lower left')
    plt.savefig(f"scaling.png")


def total_resp_time(lblc_data, lbrr_data, ss_data):
    plt.clf()
    plt.title("Total response time in seconds vs No of clients")
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

with open('scaling_data.csv') as f:
    data = csv.reader(f)
    s_data = list(data)
    print(s_data)

total_resp_time(lblc_data, lbrr_data, ss_data)
number_of_replicas(lblc_data, lbrr_data)
scaling_plot(s_data)


