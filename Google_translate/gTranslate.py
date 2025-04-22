import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QComboBox, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QClipboard
from PyQt6.QtCore import Qt
from google.cloud import translate_v3

LANGUAGES = {
    "Abkhaz": "ab",
    "Acehnese": "ace",
    "Acholi": "ach",
    "Afrikaans": "af",
    "Albanian": "sq",
    "Alur": "alz",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Assamese": "as",
    "Awadhi": "awa",
    "Aymara": "ay",
    "Azerbaijani": "az",
    "Balinese": "ban",
    "Bambara": "bm",
    "Bashkir": "ba",
    "Basque": "eu",
    "Batak Karo": "btx",
    "Batak Simalungun": "bts",
    "Batak Toba": "bbc",
    "Belarusian": "be",
    "Bemba": "bem",
    "Bengali": "bn",
    "Betawi": "bew",
    "Bhojpuri": "bho",
    "Bikol": "bik",
    "Bosnian": "bs",
    "Breton": "br",
    "Bulgarian": "bg",
    "Buryat": "bua",
    "Cantonese": "yue",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chichewa (Nyanja)": "ny",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Chuvash": "cv",
    "Corsican": "co",
    "Crimean Tatar": "crh",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dinka": "din",
    "Divehi": "dv",
    "Dogri": "doi",
    "Dombe": "dov",
    "Dutch": "nl",
    "Dzongkha": "dz",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Ewe": "ee",
    "Fijian": "fj",
    "Filipino (Tagalog)": "fil",
    "Finnish": "fi",
    "French": "fr",
    "French (French)": "fr-FR",
    "French (Canadian)": "fr-CA",
    "Frisian": "fy",
    "Fulfulde": "ff",
    "Ga": "gaa",
    "Galician": "gl",
    "Ganda (Luganda)": "lg",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Guarani": "gn",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hakha Chin": "cnh",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hiligaynon": "hil",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Hunsrik": "hrx",
    "Icelandic": "is",
    "Igbo": "ig",
    "Iloko": "ilo",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kannada": "kn",
    "Kapampangan": "pam",
    "Kazakh": "kk",
    "Khmer": "km",
    "Kiga": "cgg",
    "Kinyarwanda": "rw",
    "Kituba": "ktu",
    "Konkani": "gom",
    "Korean": "ko",
    "Krio": "kri",
    "Kurdish (Kurmanji)": "ku",
    "Kurdish (Sorani)": "ckb",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latgalian": "ltg",
    "Latin": "la",
    "Latvian": "lv",
    "Ligurian": "lij",
    "Limburgan": "li",
    "Lingala": "ln",
    "Lithuanian": "lt",
    "Lombard": "lmo",
    "Luo": "luo",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Maithili": "mai",
    "Makassar": "mak",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malay (Jawi)": "ms-Arab",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Meadow Mari": "chm",
    "Meiteilon (Manipuri)": "mni-Mtei",
    "Minang": "min",
    "Mizo": "lus",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Ndebele (South)": "nr",
    "Nepalbhasa (Newari)": "new",
    "Nepali": "ne",
    "Northern Sotho (Sepedi)": "nso",
    "Norwegian": "no",
    "Nuer": "nus",
    "Occitan": "oc",
    "Odia (Oriya)": "or",
    "Oromo": "om",
    "Pangasinan": "pag",
    "Papiamento": "pap",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Portuguese (Portugal)": "pt-PT",
    "Portuguese (Brazil)": "pt-BR",
    "Punjabi": "pa",
    "Punjabi (Shahmukhi)": "pa-Arab",
    "Quechua": "qu",
    "Romani": "rom",
    "Romanian": "ro",
    "Rundi": "rn",
    "Russian": "ru",
    "Samoan": "sm",
    "Sango": "sg",
    "Sanskrit": "sa",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Seychellois Creole": "crs",
    "Shan": "shn",
    "Shona": "sn",
    "Sicilian": "scn",
    "Silesian": "szl",
    "Sindhi": "sd",
    "Sinhala (Sinhalese)": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swati": "ss",
    "Swedish": "sv",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Tetum": "tet",
    "Thai": "th",
    "Tigrinya": "ti",
    "Tsonga": "ts",
    "Tswana": "tn",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Twi (Akan)": "ak",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Yucatec Maya": "yua",
    "Zulu": "zu"
}


class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Google Translate GUI")
        self.resize(600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.project_id_input = QLineEdit()
        self.project_id_input.setPlaceholderText("Enter Google Cloud Project ID")

        self.source_lang_combo = QComboBox()
        self.target_lang_combo = QComboBox()
        for lang in LANGUAGES:
            self.source_lang_combo.addItem(lang)
            self.target_lang_combo.addItem(lang)

        self.input_text = QTextEdit()
        self.result_label = QLabel("Translated text will appear here.")
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_translate = QPushButton("Translate")
        self.btn_paste = QPushButton("Paste from Clipboard")
        self.btn_read_file = QPushButton("Read from File")
        self.btn_copy_result = QPushButton("Copy Result")
        self.btn_save_result = QPushButton("Save Result")

        self.btn_translate.clicked.connect(self.translate_text)
        self.btn_paste.clicked.connect(self.paste_from_clipboard)
        self.btn_read_file.clicked.connect(self.read_from_file)
        self.btn_copy_result.clicked.connect(self.copy_result_to_clipboard)
        self.btn_save_result.clicked.connect(self.save_result_to_file)

        for btn in [self.btn_translate, self.btn_paste, self.btn_read_file, self.btn_copy_result, self.btn_save_result]:
            btn_layout.addWidget(btn)

        layout.addWidget(QLabel("Project ID:"))
        layout.addWidget(self.project_id_input)
        layout.addWidget(QLabel("Source Language:"))
        layout.addWidget(self.source_lang_combo)
        layout.addWidget(QLabel("Target Language:"))
        layout.addWidget(self.target_lang_combo)
        layout.addWidget(QLabel("Input Text:"))
        layout.addWidget(self.input_text)
        layout.addLayout(btn_layout)
        layout.addWidget(QLabel("Translated Text:"))
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def paste_from_clipboard(self):
        clipboard = QApplication.clipboard()
        self.input_text.setPlainText(clipboard.text())

    def read_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Text File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.input_text.setPlainText(f.read())

    def copy_result_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_label.text())

    def save_result_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Translated Text", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.result_label.text())

    def translate_text(self):
        text = self.input_text.toPlainText()
        source_lang = LANGUAGES[self.source_lang_combo.currentText()]
        target_lang = LANGUAGES[self.target_lang_combo.currentText()]
        project_id = self.project_id_input.text().strip()

        if not text or not project_id:
            QMessageBox.warning(self, "Missing Input", "Please enter Project ID and text to translate.")
            return

        try:
            client = translate_v3.TranslationServiceClient()
            parent = f"projects/{project_id}/locations/global"
            response = client.translate_text(
                contents=[text],
                mime_type="text/plain",
                source_language_code=source_lang,
                target_language_code=target_lang,
                parent=parent
            )
            translated_text = " ".join([t.translated_text for t in response.translations])
            self.result_label.setText(translated_text)
        except Exception as e:
            QMessageBox.critical(self, "Translation Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec())
