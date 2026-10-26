
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from PIL import Image
import time

BASE_DIR = Path(__file__).resolve().parent
ZIP_FILE = BASE_DIR / "images.zip"
OUTPUT_DIR = BASE_DIR / "decompressed"

JPEG_QUALITY = 95

def main():
    if not ZIP_FILE.is_file():
        raise FileNotFoundError(f"ZIP archive not found: {ZIP_FILE}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    restored = 0
    failed = 0
    start_time = time.time()

    print("Starting image decompression...")

    with ZipFile(ZIP_FILE, "r") as archive:
        for entry in archive.infolist():
            if entry.is_dir():
                continue

            archive_path = Path(entry.filename)

            # Convert every image to JPEG.
            output_path = (
                OUTPUT_DIR
                / archive_path.parent
                / f"{archive_path.stem}.jpg"
            )

            output_path.parent.mkdir(
                parents=True, exist_ok=True
            )

            try:
                with Image.open(
                    BytesIO(archive.read(entry))
                ) as image:
                    # JPEG does not support transparency.
                    if (
                        "A" in image.getbands()
                        or "transparency" in image.info
                    ):
                        rgba = image.convert("RGBA")
                        background = Image.new(
                            "RGB", rgba.size, (255, 255, 255)
                        )
                        background.paste(
                            rgba,
                            mask=rgba.getchannel("A")
                        )
                        image_to_save = background
                    else:
                        image_to_save = image.convert("RGB")

                    image_to_save.save(
                        output_path,
                        format="JPEG",
                        quality=JPEG_QUALITY,
                        optimize=True
                    )

                restored += 1
                print(
                    f"Converted: {entry.filename} -> "
                    f"{output_path.relative_to(OUTPUT_DIR)}"
                )

            except Exception as error:
                failed += 1
                print(f"Failed: {entry.filename} | {error}")

    elapsed_time = time.time() - start_time

    print("\nDecompression completed.")
    print(f"Files converted: {restored}")
    print(f"Files failed: {failed}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
