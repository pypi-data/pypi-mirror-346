import polars as pl
from .base_settings import BaseSettings

class HAILLOT(BaseSettings):
    """Gestion des paramètres de l'import du fichier de ventes d'HAILLOT ROLAND."""
    def name(self):
        return "HAILLOT ROLAND"
    
    def get_allowed_import(self) -> list[str]:
        return ["QUADRA (ASCII)"]
    
    def process_file(self):
        df = self.entries
        df = self.empty_col(df, ["JournalLib", "CompteLib"])
        df = df.with_columns(
            pl.when(~pl.col("CompAuxNum").str.starts_with("08"))
              .then(None)
              .otherwise(pl.col("CompAuxLib"))
              .alias("CompAuxLib")
        )
        return df