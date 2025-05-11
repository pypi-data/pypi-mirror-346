from .base_settings import BaseSettings

class MGECOBAT(BaseSettings):
    """Gestion des paramètres de l'import FEC de MG ECO BAT."""
    def name(self):
        return "MG ECO BAT"
    
    def get_allowed_import(self) -> list[str]:
        return ["FEC"]
    
    def process_file(self):
        filter = {"EcritureLib": "MAD IN EVENT"}
        df = self.entries
        df = self.empty_col(df, ["JournalLib", "CompteLib", "CompAuxLib"])
        df = self.replace_str(df, "CompteNum", "706600", "70830100", filter=filter)
        df = self.replace_str(df, "CompteNum", "706600", "70400000")
        df = self.replace_str(df, "CompteNum", "706500", "70410000")
        df = self.replace_str(df, "CompteNum", "445716", "44571020")
        df = self.replace_str(df, "CompteNum", "445715", "44571010")
        df = self.replace_str(df, "CompAuxNum", "^411", "C")
        return df