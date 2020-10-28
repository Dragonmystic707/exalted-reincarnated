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
    page_dir = path.join(script_dir, r"docs\pages")
    # Make sure the temporary file doesn't exist 
    temp_name = "temp.md"
    temp_file = path.join(script_dir, temp_name)

    order_num = 1
    for file_dict in file_list:
        if path.exists(temp_file):
            os.remove(temp_file)

        bash_cmd = "pandoc " + path.join(src_dir, file_dict["name"]) + ".docx -t gfm -o temp.md --strip-comments"
        process = subprocess.Popen(bash_cmd)
        process.wait()

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
