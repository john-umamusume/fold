
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageOps
from zipfile import ZipFile, ZIP_DEFLATED
import time

BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR.parent / "images"
ZIP_FILE = BASE_DIR / "images.zip"

QUALITY = 65
METHOD = 4

if not SOURCE_DIR.is_dir():
    raise FileNotFoundError(
        f"Source directory not found: {SOURCE_DIR}\n"
        "Place the original images in the expected directory."
    )

start_time = time.time()

total_original = 0
total_webp = 0
converted_files = 0
failed_files = 0
archived_files = 0

# Step 1: Convert all images to WebP and write them to the ZIP.
print("Starting image compression...")

used_paths = set()

with ZipFile(
    ZIP_FILE,
    mode="w",
    compression=ZIP_DEFLATED,
    compresslevel=9
) as archive:

    for source_file in sorted(SOURCE_DIR.rglob("*")):
        if not source_file.is_file():
            continue

        relative_path = source_file.relative_to(SOURCE_DIR)
        original_size = source_file.stat().st_size

        try:
            # Open the source image and correct its orientation.
            with Image.open(source_file) as image:
                image = ImageOps.exif_transpose(image)

                # Preserve transparency when converting to WebP.
                if (
                    "A" in image.getbands()
                    or "transparency" in image.info
                ):
                    image = image.convert("RGBA")
                else:
                    image = image.convert("RGB")

                # Convert the image in memory.
                buffer = BytesIO()
                image.save(
                    buffer,
                    format="WEBP",
                    quality=QUALITY,
                    method=METHOD
                )
                webp_data = buffer.getvalue()

            # Remove the original extension from the output name.
            output_path = relative_path.with_suffix(".webp")

            # Prevent duplicate names within the same directory.
            counter = 2
            while output_path.as_posix().lower() in used_paths:
                output_path = (
                    relative_path.parent
                    / f"{relative_path.stem}_{counter}.webp"
                )
                counter += 1

            used_paths.add(output_path.as_posix().lower())

            # Write the converted image directly to the ZIP.
            archive.writestr(output_path.as_posix(), webp_data)

            total_original += original_size
            total_webp += len(webp_data)
            converted_files += 1
            archived_files += 1

            reduction = (
                (1 - len(webp_data) / original_size) * 100
                if original_size else 0
            )

            print(
                f"Processed: {relative_path} | "
                f"{original_size / 1024:.1f} KB -> "
                f"{len(webp_data) / 1024:.1f} KB | "
                f"{reduction:.1f}% reduction"
            )

        except Exception as error:
            failed_files += 1
            print(f"Failed: {relative_path} | {error}")

# Step 2: Verify the generated ZIP archive.
print("\nVerifying ZIP archive...")

with ZipFile(ZIP_FILE, "r") as archive:
    bad_file = archive.testzip()
    archive_count = len(archive.namelist())

if bad_file:
    raise RuntimeError(f"Archive validation failed: {bad_file}")

zip_size = ZIP_FILE.stat().st_size

total_reduction = (
    (1 - zip_size / total_original) * 100
    if total_original else 0
)

elapsed_time = time.time() - start_time

# Step 3: Display the final results.
print("\nCompression completed.")
print(f"Files converted: {converted_files}")
print(f"Files failed: {failed_files}")
print(f"Files archived: {archived_files}")
print(f"Files in ZIP: {archive_count}")
print(f"Original total size: {total_original / (1024 ** 2):.2f} MB")
print(f"WebP total size: {total_webp / (1024 ** 2):.2f} MB")
print(f"Final ZIP size: {zip_size / (1024 ** 2):.2f} MB")
print(f"Total size reduction: {total_reduction:.2f}%")
print(f"Archive: {ZIP_FILE}")
print(f"Elapsed time: {elapsed_time:.2f} seconds")
