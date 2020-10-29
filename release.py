import pathlib
import subprocess
import shutil
import os
import os.path as path

introduction = {
    "name": "ExR_Introduction",
    "header": {
        "title": "System",
        "page_type": "introduction"
    }
}

summary = {
    "name": "ExR_Summary",
    "header": {
        "title": "Summary",
        "page_type": "core"
    }    
}
ccreation = {
    "name": "ExR_CharacterCreation",
    "header": {
        "title": "System",
        "page_type": "Character Creation"
    }
}

system = {
    "name": "ExR_System",
    "header": {
        "title": "System",
        "page_type": "core"
    }
}
charms = {
    "name": "ExR_Charms",
    "header": {
        "title": "Charms",
        "page_type": "core"
    }
}
sorcery = {
    "name": "ExR_Sorcery",
    "header": {
        "title": "Sorcery and Necromancy",
        "page_type": "core"
    }
}
m_arts = {
    "name": "ExR_Martial_Arts",
    "header": {
        "title": "Martial Arts",
        "page_type": "core"
    }
}



solars = {
    "name": "ExR_Solars",
    "header": {
        "title": "Solars [WIP]",
        "page_type": "exalt"
    }
}
lunars = {
    "name": "ExR_Lunars",
    "header": {
        "title": "Lunars [Stub]",
        "page_type": "exalt"
    }
}
sidereals = {
    "name": "ExR_Sidereals",
    "header": {
        "title": "Sidereals [Stub]",
        "page_type": "exalt"
    }
}
nocturnals = {
    "name": "ExR_Nocturnals",
    "header": {
        "title": "Nocturnals [Stub]",
        "page_type": "exalt"
    }
}

file_list = [ summary, ccreation, system, charms, sorcery, m_arts, solars, lunars, sidereals, nocturnals]

def main():
    script_dir = os.path.dirname(__file__)
    src_dir = path.join(script_dir, "src")
    page_dir = path.join(script_dir, "docs")
    # media_dir = path.join(page_dir, "media")
    # soffice = "C:\\Program Files\\LibreOffice\\program\\soffice"
    # Make sure the temporary file doesn't exist 
    temp_name = "temp.md"
    temp_file = path.join(script_dir, temp_name)

    order_num = 1
    for file_dict in file_list:
        if path.exists(temp_file):
            os.remove(temp_file)

        # There's a bug in pandoc that it doesn't grab the Sections of odt correctly, so we have to save the file as a docx first.
        # soffice_cmd = soffice + " --convert-to docx " + path.join(src_dir, file_dict["name"]) + ".odt"
        # subprocess.Popen(soffice_cmd).wait()

        # Temporarily disable. This could bloat the repo.
        # also create a pdf.
        #  soffice_cmd = soffice + " --convert-to pdf " + path.join(src_dir, file_dict["name"]) + ".odt --outdir " + media_dir
        #  subprocess.Popen(soffice_cmd).wait()

        bash_cmd = "pandoc " + path.join(src_dir, file_dict["name"]) + ".docx -f docx -t gfm -o temp.md --strip-comments"
        subprocess.Popen(bash_cmd).wait()
        

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

    # Add in the introduction to the System
    bash_cmd = "pandoc " + path.join(src_dir, introduction["name"]) + ".docx -f docx -t gfm -o temp.md --strip-comments"
    subprocess.Popen(bash_cmd).wait()

    combined_cmd = "pandoc temp.md " + path.join(page_dir, system["name"] + ".md") + " -t gfm -o " + path.join(page_dir, system["name"] + ".md")
    subprocess.Popen(combined_cmd).wait()

    if path.exists(temp_file):
        os.remove(temp_file)


if __name__ == "__main__":
    main()
