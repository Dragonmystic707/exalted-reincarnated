import pathlib
import subprocess
import shutil
import os
import os.path as path

core = {
    "name": "ExR_Core",
    "header": {
        "title": "Core",
    }
}
solars = {
    "name": "ExR_Solars",
    "header": {
        "title": "Solars [WIP]",
    }
}
lunars = {
    "name": "ExR_Lunars",
    "header": {
        "title": "Lunars [Stub]",
    }
}
sidereals = {
    "name": "ExR_Sidereals",
    "header": {
        "title": "Sidereals [Stub]",
    }
}
nocturnals = {
    "name": "ExR_Nocturnals",
    "header": {
        "title": "Nocturnals [Stub]",
    }
}


file_list = [core, solars, lunars, sidereals, nocturnals]

def main():
    script_dir = os.path.dirname(__file__)
    src_dir = path.join(script_dir, "src")
    page_dir = path.join(script_dir, "docs")
    media_dir = path.join(page_dir, "media")
    soffice = "C:\\Program Files\\LibreOffice\\program\\soffice"
    # Make sure the temporary file doesn't exist 
    temp_name = "temp.md"
    temp_file = path.join(script_dir, temp_name)

    order_num = 2
    for file_dict in file_list:
        if path.exists(temp_file):
            os.remove(temp_file)

        # There's a bug in pandoc that it doesn't grab the Sections of odt correctly, so we have to save the file as a docx first.
        soffice_cmd = soffice + " --convert-to docx " + path.join(src_dir, file_dict["name"]) + ".odt"
        subprocess.Popen(soffice_cmd).wait()

        # Temporarily disable. This could bloat the repo.
        # also create a pdf.
        #  soffice_cmd = soffice + " --convert-to pdf " + path.join(src_dir, file_dict["name"]) + ".odt --outdir " + media_dir
        #  subprocess.Popen(soffice_cmd).wait()

        bash_cmd = "pandoc " + file_dict["name"] + ".docx -f docx -t gfm -o temp.md --strip-comments"
        subprocess.Popen(bash_cmd).wait()
        
        # Remove the temporary docx
        os.remove(file_dict["name"] + ".docx")

        # Construct the header
        header = "---\n"
        header += "layout: page\n"
        for key, value in file_dict["header"].items():
            header += key + ": " + value + "\n"
        header += "order: " + str(order_num) + "\n"
        header += "---\n\n"

        order_num += 1

        # Add in the header data to the file
        with open(path.join(script_dir, "temp.md"), "r+", encoding="utf8") as f:
            data = f.read()
            with open(path.join(page_dir, file_dict["name"] + ".md"), "w", encoding="utf8") as w:
                w.write(header + data) 

    if path.exists(temp_file):
        os.remove(temp_file)


if __name__ == "__main__":
    main()
