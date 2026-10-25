
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from PIL import Image
import time

BASE_DIR = Path(__file__).resolve().parent
ZIP_FILE = BASE_DIR / "images.zip"
OUTPUT_DIR = BASE_DIR / "decompressed"

# Extensions that can be restored from WebP.
SUPPORTED_FORMATS = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "bmp": "BMP",
    "tif": "TIFF",
    "tiff": "TIFF",
    "gif": "GIF",
}

def main():
    if not ZIP_FILE.is_file():
        raise FileNotFoundError(f"ZIP archive not found: {ZIP_FILE}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    restored = 0
    skipped = 0
    start_time = time.time()

    with ZipFile(ZIP_FILE, "r") as archive:
        for entry in archive.infolist():
            if entry.is_dir():
                continue

            archive_path = Path(entry.filename)
            filename = archive_path.name
            extension = archive_path.suffix.lower()

            # Existing WebP files were preserved by compress.py.
            if extension == ".webp":
                stem = archive_path.stem
                original_extension = stem.rsplit("_", 1)[-1].lower()
                original_stem = stem.rsplit("_", 1)[0]

                if original_extension not in SUPPORTED_FORMATS:
                    # This was likely an original WebP file.
                    output_path = OUTPUT_DIR / archive_path
                    output_path.parent.mkdir(
                        parents=True, exist_ok=True
                    )
                    output_path.write_bytes(archive.read(entry))
                    restored += 1
                    continue

                output_path = (
                    OUTPUT_DIR
                    / archive_path.parent
                    / f"{original_stem}.{original_extension}"
                )
                image_format = SUPPORTED_FORMATS[original_extension]
            else:
                skipped += 1
                print(f"Skipped unsupported entry: {entry.filename}")
                continue

            output_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                with Image.open(BytesIO(archive.read(entry))) as image:
                    # JPEG does not support transparency.
                    if image_format == "JPEG":
                        if image.mode in ("RGBA", "LA") or (
                            "transparency" in image.info
                        ):
                            rgba = image.convert("RGBA")
                            background = Image.new(
                                "RGB", rgba.size, (255, 255, 255)
                            )
                            background.paste(
                                rgba, mask=rgba.getchannel("A")
                            )
                            image_to_save = background
                        else:
                            image_to_save = image.convert("RGB")
                    else:
                        image_to_save = image

                    image_to_save.save(
                        output_path,
                        format=image_format
                    )

                restored += 1
                print(f"Restored: {output_path.relative_to(OUTPUT_DIR)}")

            except Exception as error:
                skipped += 1
                print(f"Failed: {entry.filename} | {error}")

    elapsed = time.time() - start_time

    print("\nRestoration completed.")
    print(f"Files restored: {restored}")
    print(f"Files skipped or failed: {skipped}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Elapsed time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()
