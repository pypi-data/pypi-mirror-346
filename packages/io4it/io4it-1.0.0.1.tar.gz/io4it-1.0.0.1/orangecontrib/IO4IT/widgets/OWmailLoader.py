import os
import sys
from Orange.data import Domain, StringVariable, Table
import Orange.data
from AnyQt.QtWidgets import QApplication
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output


if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.utils import thread_management
    from Orange.widgets.orangecontrib.AAIT.utils.import_uic import uic
    from Orange.widgets.orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file
else:
    from orangecontrib.AAIT.utils import thread_management
    from orangecontrib.AAIT.utils.import_uic import uic
    from orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file


@apply_modification_from_python_file(filepath_original_widget=__file__)
class OWMailLoader(widget.OWWidget):
    name = "OWMailLoader"
    description = "Load a mail from AAIT format"
    icon = ""
    #if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    #    icon = "icons_dev/owqueryllm.svg"
    gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/owmailloader.ui")
    want_control_area = True
    priority = 9999

    class Inputs:
        data = Input("Data", Orange.data.Table)

    class Outputs:
        data_out_all_dir = Output("Data Out All Dir", Orange.data.Table)
        data_out_nothing_to_do=Output("Data Out Nothing to Do", Orange.data.Table)

    @Inputs.data
    def set_data(self, in_data):
        self.valid_folders=[]
        input_dir_path=""
        self.error("")
        if in_data is None:
            return
        if not "input_dir" in in_data.domain:
            self.error("need input_dir in input data domain" )
            return
        if len(in_data)!=1:
            self.error("in data need to be exactly 1 line" )
            return
        input_dir_path=str(in_data[0]["input_dir"].value)
        input_dir_path.replace ("\\","/")

        self.valid_folders=self.get_valid_folders(input_dir_path)
        if len(self.valid_folders)==0:
            self.send_nothing_to_do()
            return
        print( self.valid_folders)
        self.run()


    def __init__(self):
        super().__init__()
        # Qt Management
        self.valid_folders=[]
        self.can_run = True
        self.setFixedWidth(700)
        self.setFixedHeight(500)
        uic.loadUi(self.gui, self)




        # # Data Management
        self.thread = None

        # Custom updates
        self.post_initialized()



    def get_valid_folders(self,input_dir_path):
        in_dir = os.path.join(input_dir_path, "in")

        # Étape 1 : Vérifier si le dossier existe
        if not os.path.isdir(in_dir):
            print(f"Dossier introuvable : {in_dir}")
            return []  # ou `return` selon ton besoin

        # Étape 2 : Parcourir les sous-dossiers
        valid_folders = []
        for name in os.listdir(in_dir):
            full_path = os.path.join(in_dir, name)
            if os.path.isdir(full_path):
                mail_ok_path = os.path.join(full_path, "mail.ok")
                if os.path.isfile(mail_ok_path):
                    valid_folders.append(full_path.replace("\\","/"))

        return valid_folders
    def send_nothing_to_do(self):

        # Définir une variable texte comme méta-attribut
        text_meta = StringVariable("nothing to do")

        # Créer un domaine sans variables principales, avec une méta
        domain = Domain([], metas=[text_meta])

        # Créer la table avec Table.from_list
        data_table = Table.from_list(domain, [["nothing"]])
        self.Outputs.data_out_nothing_to_do.send(data_table)

    def run(self):
        # Définir les variables de texte
        var_mail_txt = StringVariable("mail_path")
        var_pj_list = StringVariable("pj_files")

        # Définir le domaine avec deux colonnes texte
        domain = Domain([], metas=[var_mail_txt, var_pj_list])

        # Construire les lignes de données
        rows = []
        for folder in self.valid_folders:
            # Chemin vers mail.txt
            mail_path = os.path.join(folder, "mail.txt")

            # Chemin vers le sous-dossier "pj"
            pj_path = os.path.join(folder, "pj")

            # Lister les fichiers dans pj (ou chaîne vide s'il n'existe pas)
            if os.path.isdir(pj_path):
                files = os.listdir(pj_path)
            else:
                files = []

            # Convertir la liste de fichiers en chaîne (ex : "file1.pdf, file2.docx")
            files_str = ", ".join(files)
            files_str='['+files_str+']'
            # Ajouter la ligne
            rows.append([mail_path, files_str])

        # Créer la table Orange
        data_table = Table.from_list(domain, rows)

        # Afficher la table
        self.Outputs.data_out_all_dir.send(data_table)

    def post_initialized(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    data = Orange.data.Table("C:/toto_ta_ta_titi/input.tab")
    my_widget = OWMailLoader()
    my_widget.show()
    my_widget.set_data(data)
    app.exec_()
