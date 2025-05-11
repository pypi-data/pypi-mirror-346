from eBonsParser import Rewe

pdf_file_path = "#FULL_PATH_HERE/eBonsParser/examples/rewe_bar.pdf"
rewe = Rewe()
receipt = rewe.parse_ebon(pdf_file_path)
print(receipt.model_dump_json(indent=4))