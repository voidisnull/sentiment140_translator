import asyncio
from source import translate, vc

if __name__ == "__main__":
    count: int = -1

    # Loading completed count from the file
    with open("counter.txt", "r") as fin:
        line = fin.readline().strip()
        if line:
            count = int(line)
        count += 1

    # Aborting if counter value can't be initialized
    if count == -1:
        print("Error loading the counter value")
        exit(1)

    # Rebasing
    print("Rebasing\n")
    vc.rebase_from_upstream()

    print(f"Translating {count}th chunk\n")

    # First pushing the counter value to main
    vc.update_counter_and_commit("counter.txt")
    vc.push_origin()

    # Starting the translating function
    asyncio.run(
        translate.main(f"dataset/train_en/{count}.csv", f"dataset/train_hi/{count}.csv")
    )

    # Pushing the translated dataset to main
    print("\nPushing the changes to upstream")
    vc.add_dataset_chunk(count)
    vc.push_origin()

    print("\nProcess Finished!!")
