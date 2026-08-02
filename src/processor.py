from pathlib import Path
from typing import Optional
from PIL import Image

def process_single_image(input_path: Path, output_dir : Path, target_format : str = "webp", max_width: Optional[int] = None,) -> Path:
    """apre un'immagine, la ridimensiona (se richiesto) e la salva ottimizzata.
    mantiene le proporzioni originali."""
    if not input_path.exists():
        raise FileNotFoundError(f"File non trovato: {input_path}")
    #se la cartella di destinazione non esiste la creiamo in automatico
    output_dir.mkdir(parents=True, exist_ok=True)
    #apriamo limmagine usando pillow
    with Image.open(input_path) as img:
        #gestione trasparenze / spazi colore - formati come jpeg non supportano la trasparenza quindi se il file é png lo convertiamo prima in rgb e poi in jpeg
        if target_format.lower() in  ["jpg", "jpeg"] and img.mode in("RGBA", "p"):
            img = img.convert("RGB")
            #ridimensionamento proporzionale
            #se viene specificata una larghezza massima ed é inferiore a quella attuale 
        if max_width and img.width > max_width:
            aspect_ratio = img.height / img.width
            new_height = int(max_width * aspect_ratio)
                
            #lanczos é il filtro di ridimensionamento di pillow di qualitá piú alta
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
            #generazione del nuovo nome file ed esportazione
            new_filename = f"{input_path.stem}.{target_format.lower()}"
            output_path = output_dir / new_filename
                
            #salva con ottimizzazione attiva e qualitá 85%
            img.save(output_path, format = target_format.upper(), optimize = True, quality = 85)
    return output_path