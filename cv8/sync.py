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
    check_ping("google.sk")
    end = time.time()
    print("This task took " + str(end - start) + " seconds to complete.")


main()
