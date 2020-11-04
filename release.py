import pathlib
import subprocess
import shutil
import tempfile
import re
import os
import os.path as path

core = {
    "folder": "System",
    "base_url": "System",
    "header": {
    }
}


# solars = {
#     "name": "Solars",
#     "folder": "Exaltations",
#     "header": {
#         "title": "Solars [WIP]",
#         "type": "exalt"
#     }
# }
# lunars = {
#     "name": "Lunars",
#     "folder": "Exaltations",
#     "header": {
#         "title": "Lunars [Stub]",
#         "type": "exalt"
#     }
# }
# sidereals = {
#     "name": "Sidereals",
#     "folder": "Exaltations",
#     "header": {
#         "title": "Sidereals [Stub]",
#         "type": "exalt"
#     }
# }
# nocturnals = {
#     "name": "Nocturnals",
#     "folder": "Exaltations",
#     "header": {
#         "title": "Nocturnals [Stub]",
#         "type": "exalt"
#     }
# }

src_list = [ core]


def main():
    script_dir = os.path.dirname(__file__)
    src_dir = path.join(script_dir, "src")
    page_dir = path.join(script_dir, "docs")
    # media_dir = path.join(page_dir, "media")

    
    # Make sure the temporary file doesn't exist 
    temp_name = "temp.md"


    # Create the Markdown release
    for dir_dict in src_list:
        with tempfile.TemporaryDirectory() as temp_dir:

            file_dir = path.join(src_dir, dir_dict["folder"])
            new_dir = path.join(page_dir, dir_dict["base_url"])
            if not path.exists(new_dir):
                os.makedirs(new_dir)

            header_dict = {}

            def replace_link(match):
                # Get rid of any illegal characters
                rtn_str = re.sub(r"[_ \s`~/{}]", '-', match.group()).lower()
                # get the heading name
                match2 = re.match(r"\(#([^|)]*)", rtn_str)
                if match2:
                    header_name = match2.group(1)
                    if header_name in header_dict:
                        header_name = header_dict[header_name]
                    rtn_str = "(" + header_name + ")"
                return rtn_str 



            # Load all the docx's, in numerical order.
            file_list = [f for f in  os.listdir(file_dir) if f.endswith('.docx')]
            for f0 in file_list:
                file_name, file_ext = os.path.splitext(f0)
                file_num, file_name = file_name.split("_", maxsplit=1)
                # Export out the base markdown to the temporary files
                bash_cmd = "pandoc " + path.join(file_dir, f0) + " -f docx -t gfm -o " + path.join(temp_dir, file_name + ".md") + " -s --strip-comments --toc" 
                subprocess.Popen(bash_cmd).wait() 

                
                # Consume the table of Contents
                with open(path.join(temp_dir, file_name + ".md"), "r+", encoding="utf8") as f:
                    data_arr = f.readlines()
                    for line in data_arr:
                        # Consume the table of contents
                        match = re.search(r'\(#(.*)\)', line)
                        if match:
                            # Create a link to include the file name.
                            link_name = match.group(1)
                            if link_name not in header_dict:
                                header_dict[link_name] = "/" + file_name + "/#" + link_name
                        # See if we've reached the first header.
                        elif re.match(r'==*', line):
                            # The header is on the previous line
                            break

            # Now that we've gathered all the header links, we can replace them.
            for f0 in file_list:
                file_name, file_ext = os.path.splitext(f0)
                file_num, file_name = file_name.split("_", maxsplit=1)

                # Make sure the number is a number, and not a string
                file_num = int(file_num)

                # Construct the header
                header = "---\n"
                header += "layout: page\n"
                header += "base_url: " + dir_dict['base_url'] + '\n'
                header += "title: " + file_name + '\n'
                for key, value in dir_dict["header"].items():
                    header += key + ": " + value + "\n"
                header += "order: " + str(file_num) + "\n"
                header += "---\n\n"

                with open(path.join(temp_dir, file_name + ".md"), "r+", encoding="utf8") as f: 
                    first_header_ind = 0
                    data_arr = f.readlines()

                    for line in data_arr:
                        if re.match(r'==*', line):
                            # The header is on the previous line
                            first_header_ind -= 1
                            break
                        first_header_ind += 1

                    # Trim the top off
                    data = "".join(data_arr[first_header_ind:])

                    # Replace the intra-document hyperlinks
                    link_str = r"\(#[^#\n]*\)"
                    data = re.sub(link_str, replace_link, data)

                    with open(path.join(new_dir, file_name + ".md"), "w", encoding="utf8") as w:
                        w.write(header + data) 
    #     temp_dir = 
    #     if path.exists(temp_file):
    #         os.remove(temp_file)

        
        
    #     subprocess.Popen(bash_cmd).wait()

    #     # Construct the header
    #     header = "---\n"
    #     header += "layout: page\n"
    #     for key, value in file_dict["header"].items():
    #         header += key + ": " + value + "\n"
    #     header += "order: " + str(order_num) + "\n"
    #     header += "previous: "
    #     header += "---\n\n"

    #     order_num += 1

    #     # Add in the introduction to the ExR_System
    #     if file_dict["name"] == system["name"]:
    #         bash_cmd = "pandoc " + path.join(src_dir, "core", introduction["name"]) + ".docx -f docx -t gfm -o temp_int.md --strip-comments "
    #         subprocess.Popen(bash_cmd).wait()

    #         combined_cmd = "pandoc temp_int.md temp.md -t gfm -o temp.md"
    #         subprocess.Popen(combined_cmd).wait()

    #         os.remove("temp_int.md")

    #     # Add in the header data to the file
    #     with open(path.join(script_dir, "temp.md"), "r+", encoding="utf8") as f:
    #         # data = f.read()
            
    #         first_header_ind = 0
    #         data_arr = f.readlines()
    #         # For all but System, trim out the Title Card
    #         if file_dict["name"] != system["name"]:
    #             for line in data_arr:
    #                 if re.match(r'==*', line):
    #                     # The header is on the previous line
    #                     first_header_ind -= 1
    #                     break
    #                 first_header_ind += 1
    #         data = "".join(data_arr[first_header_ind:])
    #         with open(path.join(page_dir, file_dict["name"] + ".md"), "w", encoding="utf8") as w:
    #             w.write(header + data) 

    # if path.exists(temp_file):
    #     os.remove(temp_file)

    # Export the PDF Versions
    # Create a pdf versions

    # Export out the Core book
    # This doesn't work. It has to be done manually.

    # I think I'm going to require pdf exports to be manual. Git updates to .md is easily compressible, To pdf? Not so much.
    # soffice_cmd = soffice + " --convert-to pdf " + path.join(src_dir, file_dict["name"]) + ".odt --outdir " + media_dir
    # subprocess.Popen(soffice_cmd).wait()


if __name__ == "__main__":
    main()
