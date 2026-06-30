import logging
from pathlib import Path

from PIL import Image, ImageFilter

from .settings import settings

logger = logging.getLogger(__name__)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def process_image(input_path: Path, output_path: Path, settings) -> bool:
    """Process a single image and return success status."""
    try:
        with Image.open(input_path) as img:
            if img.format not in settings.images_accepted_formats:
                logger.warning(f"Skipping {input_path.name}: Format {img.format} not accepted")
                return False

            # Apply transformations
            if settings.images_apply_thumbnail:
                img.thumbnail(settings.images_output_size)

            if settings.images_apply_filter_detail:
                img = img.filter(ImageFilter.DETAIL)

            if settings.images_apply_convert_l:
                img = img.convert("L")

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(
                output_path,
                optimize=settings.images_apply_optimize,
                quality=settings.images_apply_quality,
            )
            logger.info(f"Successfully processed: {input_path.name}")
            return True

    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        return False


def main():
    setup_logging()

    input_dir = Path(settings.images_input_dir)
    output_dir = Path(settings.images_output_dir)

    if not input_dir.exists():
        logger.error(f"Input directory '{input_dir}' does not exist")
        return

    # Get all image files
    files = [f for f in input_dir.iterdir() if f.is_file()]

    if not files:
        logger.info("No files found to process")
        return

    logger.info(f"Found {len(files)} file(s) to process")

    # Process files
    processed = 0
    for file in files:
        output_path = output_dir / file.name.lower()
        if process_image(file, output_path, settings):
            processed += 1

    logger.info(f"Successfully processed {processed}/{len(files)} files")


if __name__ == "__main__":
    main()
