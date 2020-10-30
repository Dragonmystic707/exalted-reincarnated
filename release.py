import pathlib
import subprocess
import shutil
import os
import os.path as path

introduction = {
    "name": "Introduction",
    "folder": "Core",
    "header": {
        "title": "System",
        "type": "core"
    }
}

summary = {
    "name": "Summary",
    "folder": "Tools",
    "header": {
        "title": "Summary",
        "type": "tools"
    }    
}
ccreation = {
    "name": "CharacterCreation",
    "folder": "Core",
    "header": {
        "title": "System",
        "type": "core"
    }
}

system = {
    "name": "System",
    "folder": "Core",
    "header": {
        "title": "System",
        "type": "core"
    }
}
charms = {
    "name": "Charms",
    "folder": "Core",
    "header": {
        "title": "Universal Charms",
        "type": "core"
    }
}
sorcery = {
    "name": "Sorcery",
    "folder": "Core",
    "header": {
        "title": "Sorcery and Necromancy",
        "type": "core"
    }
}
m_arts = {
    "name": "Martial_Arts",
    "folder": "Core",
    "header": {
        "title": "Martial Arts",
        "type": "core"
    }
}



solars = {
    "name": "Solars",
    "folder": "Exaltations",
    "header": {
        "title": "Solars [WIP]",
        "type": "exalt"
    }
}
lunars = {
    "name": "Lunars",
    "folder": "Exaltations",
    "header": {
        "title": "Lunars [Stub]",
        "type": "exalt"
    }
}
sidereals = {
    "name": "Sidereals",
    "folder": "Exaltations",
    "header": {
        "title": "Sidereals [Stub]",
        "type": "exalt"
    }
}
nocturnals = {
    "name": "Nocturnals",
    "folder": "Exaltations",
    "header": {
        "title": "Nocturnals [Stub]",
        "type": "exalt"
    }
}

exalt_list = [ solars, lunars, sidereals, nocturnals]
file_list = [ system, charms, sorcery, m_arts] + exalt_list


def main():
    script_dir = os.path.dirname(__file__)
    src_dir = path.join(script_dir, "src")
    page_dir = path.join(script_dir, "docs")
    # media_dir = path.join(page_dir, "media")

    
    # Make sure the temporary file doesn't exist 
    temp_name = "temp.md"
    temp_file = path.join(script_dir, temp_name)

    order_num = 1

    # Create the Markdown release
    for file_dict in file_list:
        if path.exists(temp_file):
            os.remove(temp_file)

        # Export out the base markdown, without the needed header
        bash_cmd = "pandoc " + path.join(src_dir, file_dict["folder"], file_dict["name"]) + ".docx -f docx -t gfm -o temp.md --strip-comments"
        subprocess.Popen(bash_cmd).wait()

        # Construct the header
        header = "---\n"
        header += "layout: page\n"
        for key, value in file_dict["header"].items():
            header += key + ": " + value + "\n"
        header += "order: " + str(order_num) + "\n"
        header += "---\n\n"

        order_num += 1

        # Add in the introduction to the ExR_System
        if file_dict["name"] == system["name"]:
            bash_cmd = "pandoc " + path.join(src_dir, "core", introduction["name"]) + ".docx -f docx -t gfm -o temp_int.md --strip-comments"
            subprocess.Popen(bash_cmd).wait()

            combined_cmd = "pandoc temp_int.md temp.md -t gfm -o temp.md"
            subprocess.Popen(combined_cmd).wait()

            os.remove("temp_int.md")

        # Add in the header data to the file
        with open(path.join(script_dir, "temp.md"), "r+", encoding="utf8") as f:
            data = f.read()
            with open(path.join(page_dir, file_dict["name"] + ".md"), "w", encoding="utf8") as w:
                w.write(header + data) 

    if path.exists(temp_file):
        os.remove(temp_file)

    # Export the PDF Versions
    # Create a pdf versions

    # Export out the Core book
    # This doesn't work. It has to be done manually.

    # I think I'm going to require pdf exports to be manual. Git updates to .md is easily compressible, To pdf? Not so much.
    # soffice_cmd = soffice + " --convert-to pdf " + path.join(src_dir, file_dict["name"]) + ".odt --outdir " + media_dir
    # subprocess.Popen(soffice_cmd).wait()


if __name__ == "__main__":
    main()
