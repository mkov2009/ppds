import time
import os


def check_ping(hostname):
    response = os.system("ping -n 2 " + hostname)
    if response == 0:
        ping_status = hostname + " Network Active"
    else:
        ping_status = hostname + " Network Error"
    print(ping_status)


def main():
    start = time.time()
    websites = ["google.sk", "stuba.sk", "linkedin.com", "discord.com"]
    for i in websites:
        check_ping(i)

    end = time.time()
    print("This task took " + str(end - start) + " seconds to complete.")


main()
