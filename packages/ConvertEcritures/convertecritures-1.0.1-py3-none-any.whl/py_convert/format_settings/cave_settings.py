import polars as pl
from pathlib import Path
from .base_settings import BaseSettings
from ..error import run_error

class CAVE(BaseSettings):
    """Gestion des paramètres de l'import du FEC de la CAVE DE SAINT TROPEZ."""
    def name(self):
        return "CAVE DE SAINT TROPEZ"
    
    def get_allowed_import(self) -> list[str]:
        return ["FEC"]
    
    def process_file(self):
        df = self.entries
        
        client_list = df.filter(
            (pl.col("CompteNum").is_between(
                pl.lit("41100000"), 
                pl.lit("41400000"),
                closed="both"
                ) |
            (pl.col("CompteNum") == pl.lit("41900000"))
        )).select("CompteNum").unique()

        supplier_list = df.filter(
            (pl.col("CompteNum").is_between(
                pl.lit("40100000"), 
                pl.lit("40200000"),
                closed="both"
                )
        )).select("CompteNum").unique()

        # Remplace les comptes auxiliaires des clients
        df = df.with_columns(
            pl.when(
                (pl.col("CompAuxNum").str.contains(r'^[1-9][0-9]{2}')) &
                (pl.col("CompteNum").is_in(client_list))
                )
              .then(pl.concat_str([
                  pl.lit("C1"), 
                  pl.col("CompAuxNum").str.slice(0, 1), 
                  pl.col("CompAuxNum").str.slice(3)
                  ]))
              .otherwise(pl.col("CompAuxNum"))
              .alias("CompAuxNum")
        )

        # Remplace les comptes auxiliaires des fournisseurs
        df = df.with_columns(
            pl.when(
                (pl.col("CompAuxNum").str.contains(r'^[1-9][0-9]{2}')) &
                (pl.col("CompteNum").is_in(supplier_list))
                )
              .then(pl.concat_str([
                  pl.lit("F8"), 
                  pl.col("CompAuxNum").str.slice(0, 1), 
                  pl.col("CompAuxNum").str.slice(3)
                  ]))
              .otherwise(pl.col("CompAuxNum"))
              .alias("CompAuxNum")
        )

        # Supprime le compte auxiliaire si le compte général n'est pas client ou fournisseur
        df = df.with_columns(
            pl.when(~(
                pl.col("CompteNum").is_in(client_list) |
                pl.col("CompteNum").is_in(supplier_list)
                ))
              .then(None)
              .otherwise(pl.col("CompAuxNum"))
              .alias("CompAuxNum"),
            pl.when(~(
                pl.col("CompteNum").is_in(client_list) |
                pl.col("CompteNum").is_in(supplier_list)
                ))
              .then(None)
              .otherwise(pl.col("CompAuxLib"))
              .alias("CompAuxLib")
        )

        # Contrôle si tous les comptes auxiliaires ont été renumérotés
        invalid_entries = df.filter(~(
            pl.col("CompAuxNum").str.starts_with("F") | 
            pl.col("CompAuxNum").str.starts_with("C")
            ))

        # Si ce n'est pas le cas, affiche un message d'erreur
        if invalid_entries.height > 0:
            invalid_entries = invalid_entries.select(
                "JournalCode",
                "JournalLib",
                "EcritureDate",
                "PieceRef",
                "CompteNum",
                "CompAuxNum",
                "CompAuxLib",
                "EcritureLib",
                "Debit",
                "Credit"
                )

            dict_col = {
                "JournalCode": {"align": "center"},
                "JournalLib": {"align": "center"},
                "EcritureDate": {"align": "center"},
                "PieceRef": {"align": "center"},
                "CompteNum": {"align": "center"},
                "CompAuxNum": {"align": "center"},
                "CompAuxLib": {"align": "left"},
                "EcritureLib": {"align": "left"},
                "Debit": {"align": "center"},
                "Credit": {"align": "center"}
            }

            invalid_file = Path.home() / "Desktop" / "InvalidAccounts.xlsx"
            invalid_entries.write_excel(
                workbook=invalid_file,
                table_style="TableStyleMedium2",
                dtype_formats={pl.Date:"dd/mm/yyyy"},
                header_format={"bold":True, "align":"center"},
                column_formats=dict_col,
                float_precision=2,
                include_header=True,
                autofit=True
            )

            msg = "L'export contient des comptes auxiliaires qui ne commencent pas par 'F' ou 'C'.\n\n"
            msg += "Veuillez consulter le fichier 'InvalidAccounts.xlsx',\n"
            msg += f"dans votre dossier {Path.home()}\Desktop"
            run_error(msg)

        return df
