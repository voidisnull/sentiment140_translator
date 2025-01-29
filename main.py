import asyncio
from source import translate

if __name__ == "__main__":
    count: int = -1

    # Load completed count from the file
    with open("counter.txt", "r+") as fin:
        line = fin.readline().strip()
        if line:
            count = int(line)
        count += 1
        fin.seek(0)
        fin.write(str(count))

    # Aborting if counter value can't be initialized
    if count == -1:
        print("Error loading the counter value")
        exit(1)

    print(f"Translating {count}th chunk\n")

    # Starting the translating function
    asyncio.run(
        translate.main(
            f"dataset/train_en/{count}.csv",
            f"dataset/train_hi/{count}.csv",
        )
    )

    print("\nProcess Finished!!")
