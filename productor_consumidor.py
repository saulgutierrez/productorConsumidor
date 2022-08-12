import threading
import random
import time
import keyboard

# Variables de memoria compartida
MAX_BUFFER_SIZE = 20
buffer = [-1 for i in range(MAX_BUFFER_SIZE)]
in_index = 0
out_index = 0

# Semaforos
mutex = threading.Semaphore()
empty = threading.Semaphore(MAX_BUFFER_SIZE)
full = threading.Semaphore(0)

# Producer Thread
class Producer(threading.Thread):
    def run(self):

        global MAX_BUFFER_SIZE, buffer, in_index, out_index
        global mutex, empty, full

        produced_objects = 0
        count = 0

        while produced_objects < 20:
            sleeptime = random.uniform(1.2, 3.5)
            empty.acquire()
            mutex.acquire()
            print("\nProductor se acerca a la mesa.")

            count += 1
            buffer[in_index] = count
            in_index = (in_index + 1) % MAX_BUFFER_SIZE
            print("\nProductor produjo galleta: ", count)

            mutex.release()
            full.release()
            print("\nProductor regresa a la cocina")

            time.sleep(sleeptime)
            print("\nProductor se fue a dormir por ", sleeptime, "segundos.")

            produced_objects += 1

# Consumer Thread
class Consumer(threading.Thread):
    def run(self):

        global MAX_BUFFER_SIZE, buffer, in_index, out_index, count
        global mutex, empty, full

        consumed_objects = 0

        while consumed_objects < 20:
            sleeptime = random.uniform(1.2, 3.5)
            full.acquire()
            mutex.acquire()
            print("\nConsumidor se acerca a la mesa.")

            produced_object = buffer[out_index]
            out_index = (out_index + 1) % MAX_BUFFER_SIZE
            print("\nConsumidor consumio galleta: ", produced_object)

            mutex.release()
            empty.release()
            print("\nConsumidor regresa a su silla")

            time.sleep(sleeptime)
            print("\nConsumidor se fue a dormir por ", sleeptime, "segundos")

            consumed_objects += 1

# Making thread
producer = Producer()
consumer = Consumer()

# Initializing threads
consumer.start()
producer.start()

# Wait for thread termination 
producer.join()
consumer.join()

keyboard.wait("esc")