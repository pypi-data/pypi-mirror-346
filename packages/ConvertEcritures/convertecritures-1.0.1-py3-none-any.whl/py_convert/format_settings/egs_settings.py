from .base_settings import BaseSettings

class EGS(BaseSettings):
    """Gestion des paramètres de l'import du fichier Excel d'EGS."""
    def name(self):
        return "EGS"
    
    def get_allowed_import(self) -> list[str]:
        return ["SEKUR"]
    
    def process_file(self):
        df = self.entries
        df = self.empty_col(df, ["JournalLib", "CompteLib", "CompAuxLib"])
        df = self.replace_str(df, "CompteNum", "706000", "70610000")
        df = self.replace_str(df, "CompteNum", "44571000", "44571020")
        return df