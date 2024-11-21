An open-source project in this project we are learn how to use the multiprocces in cpu 

What is CPU Bound and I/O Bound load? Examples

There is a task X that heavily loads the processor. For example, some of the slowest operations modern processors perform are division or trigonometric functions like sin or cos. These complex operations for the processor are called CPU Bound load.

If operations are limited by network speed, the speed of reading or writing a file to disk, or waiting for a database query response — this is I/O Bound load. You send a request to a server and wait for it to come back — the processor is idle, typically 90% of the time.
![MD-179-2-min](https://github.com/user-attachments/assets/677a7472-0b94-445d-8920-ced59e4c3f06)

How are these problems addressed in Python?

You can use the multiprocessing module, which parallelizes computations across multiple processes on multiple real CPU cores. The first overhead is the creation of new processes in the operating system, which is a relatively expensive operation. Their interaction is the second overhead—exchanging data between processes is not a trivial task. At a minimum, to pass an object between them, the object must be serialized and deserialized appropriately. In short, serialization is quite costly.

Multithreading is cheaper, especially at scale, when we plan to create large pools of threads. This is because a thread is a more lightweight entity from the operating system's perspective, compared to a process.

The most important thing is that threads share the same memory space within a single process. This means that data exchange between threads is much simpler to organize.

In Python, there's the Global Interpreter Lock (GIL), which can cause issues. At any given moment, only one locked thread can run, and others have to wait.


![MD-179-4-min](https://github.com/user-attachments/assets/dc757da3-90ed-491b-8857-99f05f49323b)

In this example we used to upload to the google drive and we used for the frontend telegram and we used the benchmarks and also cpython please check the code to learn more 
