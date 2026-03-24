import time


def get_milk():
    print("Servant is going to get milk...")
    time.sleep(1)
    print("Servant got the milk.")


def get_coffee():
    print("Servant is going to get coffee...")
    time.sleep(1.5)
    print('Servant got the coffee.')


def prepare_drink():
    print("Servant is going to prepare the drink.")
    time.sleep(0.5)
    print("Servant prepared the drink.")


def serve():
    start_time = time.time()
    get_milk()
    get_coffee()
    prepare_drink()

    total_time = time.time() - start_time
    print(f'Total time taken: {total_time:.2f} seconds')


if __name__ == '__main__':
    serve()