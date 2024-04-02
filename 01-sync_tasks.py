from time import sleep


def worker(job):
    for i in range(5):
        print(f"'{job}' in progress...")
        sleep(1)
    print(f"'{job}' done.")


def main():
    jobs = ["order milk", "order bread", "order eggs"]
    for job in jobs:
        worker(job)


if __name__ == "__main__":
    main()
