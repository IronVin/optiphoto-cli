from pathlib import Path
from PIL import Image
import pytest
from src.exif_handler import extract_exif_data


@pytest.fixture
def dummy_image_without_exif(tmp_path: Path) -> Path:
    """Fixture per un'immagine sintetica priva di metadati EXIF."""
    img_path = tmp_path / "no_exif.jpg"
    image = Image.new("RGB", (100, 100), color="blue")
    image.save(img_path)
    return img_path


def test_extract_exif_data_defaults(dummy_image_without_exif: Path):
    """Verifica che la funzione gestisca correttamente immagini senza EXIF restituendo i default."""
    data = extract_exif_data(dummy_image_without_exif)

    assert data["filename"] == "no_exif.jpg"
    assert data["camera_make"] == "sconosciuto"
    assert data["iso"] == "N/D"


def test_extract_exif_file_not_found(tmp_path: Path):
    """Verifica la gestione dell'errore su file inesistenti."""
    fake_path = tmp_path / "missing.jpg"
    with pytest.raises(FileNotFoundError):
        extract_exif_data(fake_path)