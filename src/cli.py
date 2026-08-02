import json
from pathlib import Path
from typing import Optional
import typer
from src.exif_handler import extract_exif_data
from src.processor import process_single_image

#inizizlizziamo l'app Typer
app = typer.Typer(help="📸 OptiPhoto CLI - Batch Image Processing & Metadata Tool", add_completion = False,)

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

@app.command()
def process(input_dir: Path = typer.Option(..., "--input", "-i", help = "cartella contenente le immagini da elaborare",) ,
            output_dir: Path = typer.Option (..., "--output" , "-o" , help = "cartella dove salvare le immagini elaborate") ,
            fmt: str = typer.Option("webp", "--format", "-f", help = "formato di output desiderato (webp, jpg, png)"),
            width: Optional[int] = typer.Option(None, "--width" , "-w" , help = "LArghezza massima in pixel (opzionale)") ,
            export_json: Optional[Path] = typer.Option(None, "--export-json", "-j" , help="percorso del file JSON dove esportare  i metadati EXIF")):
        """processa e ottimizza in batch tutte le immagini presenti in una cartella."""
        if not input_dir.is_dir():
            typer.secho(f"❌ Errore: {input_dir} non é una cartella valida.", bold = True,) 
            raise typer.exit(code=1)
        images = [f for f in input_dir.iterdir()
             if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
        if not images:
            typer.secho("⚠️ nessuna immagine supportata trovata." , fg = typer.colors.YELLOW)
            return
    
        results = []
        typer.secho(f"\n🔍 Estrazione EXIF da {len(images)} immagini:\n", fg = typer.colors.BRIGHT_BLUE,)
        for img_path in images:
            try:
                data = extract_exif_data(img_path)
                results.append(data)
                typer.echo (f"📸{data['filename']} | fotocamera: {data['camera_make']} {data['camera_model']} | ISO: {data['iso']} | Scatto: {data['exposure_time']}")
            except Exception as e:
                typer.secho(f"❌ Errore su {img_path.name}:  {e}", fg=typer.colors.RED)
        if export_json:
             with open(export_json, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
                typer.secho(f"\n💾 MEtadati esportati con successo in: {export_json}", fg=typer.colors.BRIGHT_GREEN,)
if __name__ == "__main__":
        app()
                           
                            
            
    