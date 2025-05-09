import aiofiles
import asyncio
import humanize
import pathlib
from pkg.atomics import atomic_counter
import timeit
import argparse

async def process_chunks(file_path, chunk_size=8192):
    """Let's asynchronously read the content of a file and process it in chunks."""
    try:
        # Metrics
        counter = atomic_counter.AtomicCounter()
        total_bytes = atomic_counter.AtomicCounter()

        # Process the content of a file as chunked data.
        async with aiofiles.open(file_path, 'rb') as f:
            while True:
                chunk = await f.read(chunk_size)
                if not chunk:
                    break

                # Process the chunk of data from the file.
                chunk_len = len(chunk)
                await process_chunk(chunk, chunk_len)

                # Update and report processing metrics.
                total_bytes.increment(chunk_len)
                counter.increment()
                print(f"Processed[{humanize.intcomma(counter.get()):>4}]:{humanize.intcomma(chunk_len):>6}B / {humanize.intcomma(total_bytes.get()):>10}B")

    except Exception as e:
        print(f"ERROR: {e}")

async def process_chunk(chunk, chunk_len):
    """Let's simulate some asynchronous manipulation of the chunk's data."""
    await asyncio.sleep(0.1)

async def input_validation(args):
    try:
        args.file_path.exists()
    except FileNotFoundError:
        print(f"File '{args.file_path}' does not exist")
    try:
        args.file_path.is_file()
    except FileNotFoundError:
        print(f"'{args.file_path}' is not a file")


################################################################################
#                             M  A  I  N  L  I  N  E                           #
################################################################################
async def main():

    parser = argparse.ArgumentParser(description="CHUNKER: File processing in BITES!")
    parser.add_argument("file_path", type=pathlib.Path, help="The file to process")
    args = parser.parse_args()
    await input_validation(args)

    started = timeit.default_timer()
    await process_chunks(args.file_path)
    ended = timeit.default_timer()

    print(f"Elapsed: {humanize.scientific(round((ended - started) * 1e6, 3))} µs")

# Launch the app.
if __name__ == "__main__":
    asyncio.run(main())
