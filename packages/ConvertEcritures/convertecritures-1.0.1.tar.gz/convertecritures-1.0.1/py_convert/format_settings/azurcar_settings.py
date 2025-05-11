import polars as pl
from .base_settings import BaseSettings
from ..error import run_error

class AZURCAR(BaseSettings):
    """Gestion des paramètres de l'import du fichier de ventes d'AZUR CAR SERVICES."""
    def name(self):
        return "AZUR CAR SERVICES"
    
    def get_allowed_import(self) -> list[str]:
        return ["QUADRA (ASCII)"]
    
    def replace_jrn(self, df: pl.DataFrame) -> pl.DataFrame:
        """Effectue des modifications sur les journaux."""
        
        # Remplace le code journal des ventes VO par VVO
        df = df.with_columns(
            pl.when(
                (df['PieceRef'].is_in(df.filter(pl.col('CompteNum') == '70710000')['PieceRef'])) |
                (df['PieceRef'].is_in(df.filter(pl.col('CompteNum') == '70711010')['PieceRef']))
                )
              .then(pl.lit("VVO"))
              .otherwise(pl.col("JournalCode"))
              .alias("JournalCode")
        )

        # Remplace le code journal par "TV"
        df = df.with_columns(
            pl.when(
                (pl.col("JournalCode") == "15") |
                (pl.col("JournalCode") == "16")
              )
              .then(pl.lit("TV"))
              .otherwise(pl.col("JournalCode"))
              .alias("JournalCode")
        )
        
        return df
    
    def replace_account_4(self, df: pl.DataFrame) -> pl.DataFrame:
        """Effectue des modifications sur les comptes de tiers."""
        
        # Le nom du fournisseur démarre au 7ème caractère dans le libellé
        # Fact. = 6 caractères avec l'espace
        # Avoir = 6 caractères avec l'espace
        nb = 7 - 1 # début = 0
        
        client_list = [
            {"entity": "AZUR CAR SERVICES", "account": "CASS"},
            {"entity": "AZUR AUTO", "account": "CAZUR"},
            {"entity": "DIAT", "account": "CDIAT"},
            {"entity": "DIRECT GARANTIE", "account": "CDIRECT"},
            {"entity": "GEMY", "account": "CGEMY"},
            {"entity": "OPCO MOBILITE", "account": "COPCO"},
            {"entity": "SNE CMA", "account": "CSNE"},
            {"entity": "PARASCANDOLA", "account": "CPARASCANDOLA"},
            {"entity": "AB LOCATION", "account": "CAB"},
            {"entity": "ARVAL FLEET SERVICES", "account": "CARVAL"},
            {"entity": "ARVAL SERVICE LEASE", "account": "CARVAL"},
            {"entity": "ALPHABET FRANCE FLEET", "account": "CALPHABET"},
            {"entity": "EMIS TRANSPORT", "account": "CEMIS"},
            {"entity": "MAGA AUTO", "account": "CMAGA"},
            {"entity": "SKR TRANSPORT", "account": "CSKR"},
        ]

        # Remplace le compte auxiliaire de certains clients spécifiques
        for client in client_list:
            df = df.with_columns(
                pl.when(
                    (pl.col("CompAuxNum").is_not_null()) &
                    (pl.col("EcritureLib").str.slice(nb, len(client["entity"]))
                     .str.starts_with(client["entity"]))
                  )
                  .then(pl.lit(client["account"]))
                  .otherwise(pl.col("CompAuxNum"))
                  .alias("CompAuxNum")
            )

        # Remplace le compte auxiliaire des ventes VO par CVO sauf pour les clients spécifiques précédents
        df = df.with_columns(
            pl.when(
                (pl.col("CompAuxNum").str.starts_with("01")) &
                (
                    (df["PieceRef"].is_in(df.filter(pl.col("CompteNum") == "70715190")["PieceRef"])) |
                    (df["PieceRef"].is_in(df.filter(pl.col("CompteNum") == "70719190")["PieceRef"]))
                )
              )
              .then(pl.lit("CVO"))
              .otherwise(pl.col("CompAuxNum"))
              .alias("CompAuxNum")
        )

        # Remplace le compte auxiliaire par C suivi du 1er caractère du fournisseur
        df = df.with_columns(
            pl.when((pl.col("CompAuxNum").str.starts_with("01")))
              .then(pl.lit("C") + pl.col("CompAuxNum").str.slice(2,1))
              .otherwise(pl.col("CompAuxNum"))
              .alias("CompAuxNum")
        )

        # Si le 1er caractère du fournisseur n'est pas alphabétique :
        # Va chercher le 1er caractère alphabétique dans le nom du fournisseur
        df = df.with_columns(
            pl.when(
                (pl.col("CompAuxNum").str.slice(1,1).str.contains(r"[^a-zA-Z]")) &
                (pl.col("EcritureLib").str.slice(nb).str.contains(r"[a-zA-Z]"))
                )
              .then(
                  (pl.lit("C")) +
                  (pl.col("EcritureLib").str.slice(
                      pl.col("EcritureLib").str.slice(nb).str.find(r'[a-zA-Z]') + nb,
                      1
                      )
                  )
                )
              .otherwise(pl.col("CompAuxNum"))
              .alias("CompAuxNum")
        )

        # Remplace le compte de débours 4676 par 46712
        df = self.replace_str(df, "CompteNum", "4676", "46712000")

        # Remplace les comptes 471 par le compte 70622190 pour se faire catch plus tard
        df = self.replace_str(df, "CompteNum", "471", "70622190")
        
        # Remplace le compte 44570120 par 44571400
        df = self.replace_str(df, "CompteNum", "44570120", "44571400")
        
        return df
    
    def replace_account_7(self, df: pl.DataFrame, exclusion_list: list[str]) -> pl.DataFrame:
        """Effectue des modifications sur les comptes de produits."""
        
        # Remplace les comptes de ventes de l'OPCO
        df_filtered = df.filter(pl.col("CompAuxNum").eq("COPCO").any().over("PieceRef"))
        df = self.group_accounts(
            df, 
            df_filtered = df_filtered,
            by="79120000",
            exclude=exclusion_list
        )
        
        # Remplace les comptes sans TVA de DIRECT GARANTIE & AZUR CAR SERVICES
        df = self.group_accounts(
            df, 
            group=["70607190", "70621190", "70622190"],
            by="79100000",
            replace=["70607190", "70621190", "70622190", "70715190", "70719190", "70915190", "70919190"],
            exclude=exclusion_list
        )

        # Remplace les comptes avec TVA de DIRECT GARANTIE
        df_filtered = df.filter(
            (pl.col("CompAuxNum").eq("CDIRECT").any().over("PieceRef")) &
            (pl.col("CompteNum").str.starts_with("4457").any().over("PieceRef"))
        )
        df = self.group_accounts(
            df,
            df_filtered = df_filtered,
            by="70601200",
            exclude=exclusion_list
        )
        
        # Remplace les comptes de ventes VO sans TVA
        # doit être placé après DIRECT GARANTIE pour éviter des conflits de produits sans TVA
        df = self.group_accounts(
            df, 
            group=["70715190", "70719190"], 
            by="70710000",
            replace=["70715190", "70719190"],
            exclude=exclusion_list
        )
        
        # Remplace les frais de mise à disposition sur les ventes VO sans TVA
        df = df.with_columns(
            pl.when(
                (pl.col("CompteNum") == "70719120") & 
                (pl.col("CompteNum").eq("70710000").any().over("PieceRef"))
            )
            .then(pl.lit("70601100"))
            .otherwise(pl.col("CompteNum"))
            .alias("CompteNum")
        )
        
        # Regroupe les contrôles techniques dans un seul compte individualisé
        df = self.group_accounts(
            df, 
            group="70451120", 
            by="70620000",
            replace=["70451120", "70951120"],
            exclude=exclusion_list
        )

        accounts_bodywork = ["70622120", "70623120", "70607120"]
        accounts_repair = ["70620120", "70621120", "70626120", "70629120", "70624120", "70625120"]
        # Important : permet de filtrer des faux-positifs détectés en carrosserie
        df_filtered = self.filter_bodywork(df, accounts_bodywork, accounts_repair)

        # Regroupe les comptes de produits de carrosserie
        df = self.group_accounts(
            df, 
            df_filtered=df_filtered,
            group=accounts_bodywork, 
            by="70611100", 
            exclude=exclusion_list,
        )

        # Regroupe les comptes de produits de révision/réparations
        df = self.group_accounts(
            df, 
            group=accounts_repair, 
            by="70601100",
            exclude=exclusion_list
        )
        
        # Remplace les comptes de commission GEMY et PARASCANDOLA
        # Il est important de l'exécuter après la carrosserie/révision 
        # mais avant les ventes de pièces pour éviter les erreurs d'imputation
        df_filtered = df.filter(
            pl.col("PieceRef").is_in(df.filter(
                (pl.col("CompAuxNum") == "CGEMY") |
                (pl.col("CompAuxNum") == "CPARASCANDOLA")
                )["PieceRef"]
            )
        )
        df = self.group_accounts(
                df, 
                df_filtered = df_filtered,
                group=["70715120", "70915120"],
                by="70800001",
                replace=["70715120", "70915120"],
                exclude=exclusion_list
        )

        # Permet d'imputer les commissions même si de nouveaux clients sont ajoutés
        # Cette ligne suffira quand la commission sera correctement imputée en 70840120
        df = self.group_accounts(
                df, 
                group="70840120",
                by="70800001",
                replace="70840120",
                exclude=exclusion_list
        )
        
        # Remplace les comptes de ventes de pieces sans main d'oeuvre
        df = self.group_accounts(
            df, 
            group=["70715120", "70719120", "70728120", "70915120", "70919120", "70928120"], 
            by="70730100",
            exclude=exclusion_list
        )
        
        return df
    
    def filter_bodywork(self, df: pl.DataFrame, accounts_target: list[str], accounts_compared: list[str]) -> pl.DataFrame:
        """
        Filtrer les écritures pour conserver celles dont la MO carrosserie est supérieure à la MO réparation.

        Parameters:
            df (polars.DataFrame): Le DataFrame à filtrer.
            accounts_target (list[str]): La liste des comptes cibles (carrosserie) pour le filtrage.
            accounts_compared (list[str]): La liste des comptes à comparer (réparation) pour le filtrage.
        """
    
        df_filtered = df.filter(
            pl.col("CompteNum").is_in(accounts_target).any().over("PieceRef")
        )
        
        # Calcul la somme de la MO carrosserie des factures
        df_target = df_filtered.with_columns(
            (pl.col("Credit") - pl.col("Debit")).alias("target_sum")
        ).filter(
            pl.col("CompteNum").is_in(accounts_target)
        ).group_by("PieceRef").agg(
            pl.col("target_sum").abs().sum().alias("target_sum")
        )
        
        # Calcul de la somme de la MO réparations des factures
        df_compared = df_filtered.with_columns(
            (pl.col("Credit") - pl.col("Debit")).alias("compared_sum")
        ).filter(
            pl.col("CompteNum").is_in(accounts_compared)
        ).group_by("PieceRef").agg(
            pl.col("compared_sum").abs().sum().alias("compared_sum")
        )
        
        # Filtre pour conserver les factures dont MO carrosserie > MO réparation
        df_result = (
            df
            .join(df_target, on="PieceRef", how="left")
            .join(df_compared, on="PieceRef", how="left")
            .filter(pl.col("target_sum") > pl.col("compared_sum").fill_null(0))
            .drop(["target_sum", "compared_sum"])
        )
        
        return df_result

    def process_file(self):
        df = self.entries
        df = self.empty_col(df, ["JournalLib", "CompteLib", "CompAuxLib"])
    
        # Supprime toutes les factures de garantie
        df = df.filter(pl.col("JournalCode") != "17")

        # Remplace les valeurs négatives par des valeurs positives dans l'autre sens
        df = df.with_columns(
            (pl
            .when(pl.col("Debit") < -1e-3)
            .then(pl.col("Debit").abs())
            .otherwise(pl.col("Credit"))
            .alias("Credit")),
            (pl
            .when(pl.col("Credit") < -1e-3)
            .then(pl.col("Credit").abs())
            .otherwise(pl.col("Debit"))
            .alias("Debit"))
        )

        # Remplace les valeurs négatives par des zéros
        # Nécessaire vu que j'ai inversé le sens des valeurs négatives
        df = df.with_columns(
            (pl
            .when(pl.col("Debit") < -1e-3)
            .then(0)
            .otherwise(pl.col("Debit"))
            .alias("Debit")),
            (pl
            .when(pl.col("Credit") < -1e-3)
            .then(0)
            .otherwise(pl.col("Credit"))
            .alias("Credit"))
        )

        # Plan comptable des comptes de produits d'AZUR CAR SERVICES
        exclusion_list = [
            "70601100", 
            "70601200", 
            "70611100", 
            "70620000", 
            "70710000", 
            "70711010", 
            "70730100", 
            "70800001", 
            "79100000", 
            "79120000"
            ]

        df = self.replace_account_4(df)
        df = self.replace_account_7(df, exclusion_list)
        df = self.replace_jrn(df)

        exclusion_list.append("41100000")
        exclusion_list.append("44571400")
        exclusion_list.append("46712000")

        # Filtrer les lignes dont le CompteNum n'est pas dans la liste d'exclusion
        df_invalid_account = df.filter(~pl.col("CompteNum").is_in(exclusion_list))

        # Afficher un message avec les CompteNum en dehors de la liste d'exclusion
        if df_invalid_account.height > 0:
            # Récupérer les CompteNum exclus
            list_invalid_account = df_invalid_account["CompteNum"].unique().to_list()
            msg = "Des numéros de compte sont en dehors du Plan Comptable du dossier."
            run_error(msg, details=f"{'\n'.join(list_invalid_account)}")

        return df