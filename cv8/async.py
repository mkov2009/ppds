import time
import os
import asyncio


async def check_ping(hostname):
    response = os.system("ping -n 2 " + hostname)
    if response == 0:
        ping_status = hostname + " Network Active"
    else:
        ping_status = hostname + " Network Error"
    print(ping_status)


async def main():
    start = time.time()
    websites = ["google.sk", "stuba.sk", "linkedin.com", "discord.com"]
    for i in websites:
        asyncio.ensure_future(check_ping(i))

    end = time.time()
    print("This task took " + str(end - start) + " seconds to complete.")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
