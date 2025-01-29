import googletrans
import asyncio
import pandas as pd
from typing import Optional
from tqdm import tqdm
import os


async def translate_row(
    translator: googletrans.Translator,
    tweet: str,
    target_lang: str,
    retries: int = 6,
    retry_delay: int = 10,
) -> Optional[str]:
    """
    Translates a single line of text using the translator provided.

    Args:
        translator: googletrans.Translator instance
        tweet: Text to translate
        target_lang: Target language code
        retries: Number of retry attempts
        retry_delay: Time to wait between retries in seconds

    Returns:
        Translated text or empty string if translation fails
    """

    for attempt in range(retries):
        try:
            translation = await translator.translate(tweet, dest=target_lang, src="en")

            return translation.text

        except Exception as e:
            print(f"Error {e}: Attempt {attempt + 1} failed")

            if attempt < retries - 1:  # Don't sleep on last attempt
                print(f"Retrying in {retry_delay} seconds")
                await asyncio.sleep(retry_delay)

    return ""


async def translate_dataset(
    series: pd.Series, target_lang: str = "hi", delay: float = 0.35
) -> pd.Series:
    """
    Translates a pandas Series to the target language.

    Args:
        series: Pandas Series containing text to translate
        target_lang: Target language code (default: Hindi)
        delay: Time to wait between translations in seconds

    Returns:
        New pandas Series with translated text
    """

    translator = googletrans.Translator()
    translated_series = series.copy()

    # Progess Bar
    pbar = tqdm(total=len(translated_series))

    for index, row in enumerate(series):
        translated_text = await translate_row(translator, row, target_lang)
        translated_series.iloc[index] = translated_text

        pbar.update(1)

        await asyncio.sleep(delay)

    pbar.close()

    return translated_series


async def main(inDir: str, outDir: str, outFolder: str) -> None:
    # Asynchronous main function

    df = pd.read_csv(inDir, header=None)

    # Translating the entires and stroing it back in the dataframe
    df.loc[:, 1] = await translate_dataset(df[1])

    # Testing on 5 rows
    # df_head = df.head()
    # df_head.loc[:, 1] = await translate_dataset(df_head[1])
    # df_head.to_csv(outDir, index=False, header=False)

    os.mkdir(outFolder)
    df.to_csv(outDir, index=False, header=False)


if __name__ == "__main__":
    asyncio.run(main())
