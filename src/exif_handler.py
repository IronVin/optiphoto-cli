from pathlib import Path
from typing import Dict, Any 
import exifread

def extract_exif_data(image_path: Path) -> Dict[str, Any]:
    """legge un file immagine ed estrae i princxipali dati EXIF
    ritorna un dizionario pulito con le informazioni dello scatto."""
    #controllo di sicurezza: verifichiamo chje il file esista davvero
    if not image_path.exists():
        raise FileNotFoundError(f"impossibile trovare il file:{image_path}")
    #valori di default nel caso in cui la foto con contenga dati EXIF
    metadata: Dict[str, Any] = {
        "filename" : image_path.name,
        "camera_make" : "sconosciuto",
        "camera_model" : "sconosciuto",
        "iso" : "N/D",
        "exposure_time" : "N/D",
        "f_number" : "N/D",
    }
    #apriamo il file in modalitá lettura binaria 
    with open(image_path, "rb") as f:
        #exifread estrae tutti i tag presenti nel file
        tags = exifread.process_file(f, details = False)
        #mappiamo i tag trovati nel nostro dizionario
        if"image make" in tags:
            metadata["camera_make"] = str(tags["image make"]) 
        if"image model" in tags:
            metadata["camera_model"] = str(tags["image model"])
        if"EXIF ISOSpeedRatings" in tags:
            metadata["iso"] = str(tags["EXIF ISOSpeedRatings"])
        if"EXIF exposureTime" in tags:
            metadata["exposure_time"] = str(tags["EXIF exposureTime"])
        if"EXIF FNumber" in tags:
            metadata["f_number"] = str(tags["EXIF FNumber"])
            
    return metadata                                