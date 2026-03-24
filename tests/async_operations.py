import asyncio
import time


async def get_milk():
    print("Servant is going to get milk...")
    time.sleep(1)
    print("Servant got the milk.")


async def get_coffee():
    print("Servant is going to get coffee...")
    time.sleep(1.5)
    print('Servant got the coffee.')


async def prepare_drink():
    print("Servant is going to prepare the drink.")
    time.sleep(0.5)
    print("Servant prepared the drink.")


async def serve():
    start_time = time.time()
    await asyncio.gather(get_milk(), get_coffee())

    await prepare_drink()

    total_time = time.time() - start_time
    print(f'Total time taken: {total_time:.2f} seconds')


async def main():
    await asyncio.gather(*[serve() for i in range(10)])


if __name__ == '__main__':
    asyncio.run(main())
