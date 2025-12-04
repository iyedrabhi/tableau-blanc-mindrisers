from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from datetime import datetime

# Sprint backlog entries focused on metiers (functional features)
entries = [
    {
        "id_us": "1.1",
        "user_story": "En tant que gérant\nJe veux rechercher/filtrer des clients et livreurs\nAfin de trouver rapidement les bons profils",
        "tasks": [
            ("1.1.1", "Implémenter la recherche par texte (username, nom, email)", 1.0, "Iyed Rabhi"),
            ("1.1.2", "Ajouter filtres par rôle et état (actif/supprimé)", 1.0, "Iyed Rabhi"),
            ("1.1.3", "Tester la recherche et le filtrage", 0.5, "Iyed Rabhi"),
        ],
    },
    {
        "id_us": "1.2",
        "user_story": "En tant que gérant\nJe veux exporter en Excel les listes\nAfin de partager ou analyser les données",
        "tasks": [
            ("1.2.1", "Créer la méthode export Excel (clients)", 1.5, "Iyed Rabhi"),
            ("1.2.2", "Créer la méthode export Excel (livreurs)", 1.5, "Iyed Rabhi"),
            ("1.2.3", "Inclure la colonne 'Deleted' et formatage", 0.5, "Iyed Rabhi"),
            ("1.2.4", "Vérifier l'ordre des routes pour export", 0.5, "Iyed Rabhi"),
        ],
    },
    {
        "id_us": "1.3",
        "user_story": "En tant que gérant\nJe veux effectuer un soft-delete des comptes\nAfin de conserver l'historique tout en les masquant",
        "tasks": [
            ("1.3.1", "Ajouter le champ is_deleted au modèle User", 0.5, "Iyed Rabhi"),
            ("1.3.2", "Adapter les vues de suppression (clients/livreurs)", 1.0, "Iyed Rabhi"),
            ("1.3.3", "Exclure les supprimés des listes et du dashboard", 0.5, "Iyed Rabhi"),
            ("1.3.4", "Inclure les supprimés dans l'export", 0.5, "Iyed Rabhi"),
        ],
    },
    {
        "id_us": "1.4",
        "user_story": "En tant qu'utilisateur\nJe veux activer/désactiver des comptes\nAfin de gérer l'accès sans supprimer",
        "tasks": [
            ("1.4.1", "Ajouter les boutons et routes toggle-active", 1.0, "Iyed Rabhi"),
            ("1.4.2", "Adapter le login pour message compte désactivé", 0.5, "Iyed Rabhi"),
            ("1.4.3", "Tests et vérifications UI 'Active/Inactive'", 0.5, "Iyed Rabhi"),
        ],
    },
]


def add_title(doc: Document, text: str):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.bold = True
    run.font.size = Pt(16)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def add_table_for_entries(doc: Document, entries):
    # Table headers
    table = doc.add_table(rows=1, cols=6)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Id-US'
    hdr_cells[1].text = 'User story'
    hdr_cells[2].text = 'Id-T'
    hdr_cells[3].text = 'Tâches'
    hdr_cells[4].text = 'Estimation (h)'
    hdr_cells[5].text = 'Responsable'

    for entry in entries:
        # Merge initial row to show Id-US and User Story
        row = table.add_row()
        row.cells[0].text = entry["id_us"]
        row.cells[1].text = entry["user_story"]
        # Merge vertically for tasks that follow
        # We'll add one row per task and repeat Id-T/Tâches/Estimation+Responsable
        # Set empty for the first task row cells[0] and cells[1] except first
        first = True
        for (id_t, task, estimate, resp) in entry["tasks"]:
            if first:
                # Fill remaining columns on the same first row
                row.cells[2].text = id_t
                row.cells[3].text = task
                row.cells[4].text = f"{estimate}"
                row.cells[5].text = f"{resp}"
                first = False
            else:
                r = table.add_row()
                # Leave Id-US and User story empty in subsequent rows
                r.cells[0].text = ''
                r.cells[1].text = ''
                r.cells[2].text = id_t
                r.cells[3].text = task
                r.cells[4].text = f"{estimate}"
                r.cells[5].text = f"{resp}"


def main():
    doc = Document()
    add_title(doc, 'Sprint Backlog - Fonctionnalités Métier')
    subtitle = doc.add_paragraph()
    subtitle.add_run(f"Généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    subtitle.style = doc.styles['Normal']

    doc.add_paragraph('\n')
    add_table_for_entries(doc, entries)

    output_path = 'Sprint_Backlog_Metiers_v2.docx'
    doc.save(output_path)
    print(f"Backlog généré: {output_path}")


if __name__ == '__main__':
    main()
