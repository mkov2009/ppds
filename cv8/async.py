import time
import asyncio


async def check_ping(hostname):
    proc = await asyncio.create_subprocess_shell(
        'ping -n 2 ' + hostname, stdout=asyncio.subprocess.PIPE)
    line = await proc.stdout.readline()
    if line != b"":
        ping_status = hostname + " Network Active"
    else:
        ping_status = hostname + " Network Error"
    print(ping_status)
    return


async def main():
    start = time.time()
    websites = ["google.sk", "stuba.sk", "linkedin.com", "discord.com"]
    tasks = []
    for i in websites:
        tasks.append(asyncio.ensure_future(check_ping(i)))

    await asyncio.gather(*tasks)

    end = time.time()
    print("This task took " + str(end - start) + " seconds to complete.")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
