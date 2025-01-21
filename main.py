import asyncio
from source import translate, vc

if __name__ == "__main__":
    count: int = 0

    # Loading completed count from the file
    with open("counter.txt", "r") as fin:
        count = int(fin.readline())
        count += 1
    
    # First pushing the counter value to main
    vc.update_counter_and_commit("counter.txt")
    vc.push_origin()

    # Starting the translating function
    asyncio.run(translate.main(f"dataset/train_en/{count}.csv", f"dataset/train_hi/{count}.csv"))

    # Pushing the translated dataset to main
    vc.add_dataset_chunk(count)
    vc.push_origin()