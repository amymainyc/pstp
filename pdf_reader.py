import PyPDF2
import json

file_names = ["AD", "NM", "OHLAY", "SW"]

for f in file_names:

    with open(f"line_sheets/{f}.pdf", "rb") as file:
        file = PyPDF2.PdfReader(file)

        ad_data = {}
        for i in range(4, len(file.pages)):
            page = file.pages[i]
            text = page.extract_text()
            text = text.replace(" ", "")
            text = text.replace("Qty:", "\nQty:")
            text = text.replace("Qty:\n", "Qty:")
            text = text.split("\n")

            good_words = ["Size", "Price", "Qty"]

            code = ""
            for i in range(len(text)-1):
                if "Size" in text[i+1]:
                    code = text[i]
                    ad_data[code] = {}
                else:
                    for w in good_words:
                        if w in text[i]:
                            ad_data[code][w] = text[i].split(":")[-1]
                            break
                
        with open(f"line_sheet_data/{f}.json", "w") as f:
            json.dump(ad_data, f, indent=4)
            
# 30m