from pathlib import Path
from PIL import Image
import pytest
from src.processor import process_single_image


@pytest.fixture
def sample_image(tmp_path: Path) -> Path:
    """Fixture che crea un'immagine temporanea (2000x1000 px) per i test."""
    img_path = tmp_path / "test_input.png"
    # Creiamo un'immagine rossa in modalità RGB
    image = Image.new("RGB", (2000, 1000), color="red")
    image.save(img_path)
    return img_path


def test_process_single_image_resize_and_conversion(
    sample_image: Path, tmp_path: Path
):
    """Verifica che l'immagine venga ridimensionata (mantenendo l'aspect ratio) e convertita."""
    output_dir = tmp_path / "output"

    # Eseguiamo la funzione impostando larghezza max a 1000 e formato webp
    output_path = process_single_image(
        input_path=sample_image,
        output_dir=output_dir,
        target_format="webp",
        max_width=1000,
    )

    # 1. Verifichiamo che il file esista e sia in formato .webp
    assert output_path.exists()
    assert output_path.suffix == ".webp"

    # 2. Verifichiamo le dimensioni effettive dell'immagine generata
    with Image.open(output_path) as img:
        assert img.width == 1000
        # Aspect ratio 2:1 mantenuto: 2000x1000 -> 1000x500
        assert img.height == 500


def test_process_file_not_found(tmp_path: Path):
    """Verifica che venga sollevata l'eccezione FileNotFoundError se il file non esiste."""
    non_existent_file = tmp_path / "ghost.jpg"
    output_dir = tmp_path / "output"

    with pytest.raises(FileNotFoundError):
        process_single_image(non_existent_file, output_dir)