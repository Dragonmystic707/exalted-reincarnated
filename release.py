import pathlib
import argparse
import subprocess
import shutil
import tempfile
from zipfile import ZipFile
import re
import os
import os.path as path

start_index = 2

core = {
    "folder": "System",
    "base_url": "System",
    "header": {
    }
}

solars = {
    "folder": "Solars",
    "base_url": "Solars",
    "header": {
    }
}

lunars = {
    "folder": "Lunars",
    "base_url": "Lunars",
    "header": {
    }
}

sidereals = {
    "folder": "Sidereals",
    "base_url": "Sidereals",
    "header": {
    }
}

infernals = {
    "folder": "Infernals",
    "base_url": "Infernals",
    "header": {
    }
}

nocturnals = {
    "folder": "Nocturnals",
    "base_url": "Nocturnals",
    "header": {
    }
}


src_list = [ core, solars, lunars, sidereals, infernals, nocturnals]

# Define some local paths (may need to change this later)
script_dir = os.path.dirname(__file__)
src_dir = path.join(script_dir, "src")
page_dir = path.join(script_dir, "docs")
downloads_dir = path.join(page_dir, "assets", "downloads")
soffice = "\"C:\\Program Files\\LibreOffice\\program\\soffice\""
zip_name = "Exalted_Reincarnated.zip"

macro_name = "Standard.Exalted.export_to_pdf"


def procces_dir(dir_dict, group_order):
    with tempfile.TemporaryDirectory() as temp_dir:
        folder_name = dir_dict["folder"]
        file_dir = path.join(src_dir, folder_name)
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

        
        print("------------------------")
        print("Processing", folder_name)
        

        # Load all the docx's, in numerical order.
        file_list = [f for f in  os.listdir(file_dir) if f.endswith('.odt')]
        for f0 in file_list:
            print("Exporting", f0, "to docx...")
            # For some reason, pandoc doesn't work well with odt. So we have to go to docx first using libreoffice
            soffice_cmd = soffice + " --headless --convert-to docx \"" + path.join(file_dir, f0) + "\" --outdir " + temp_dir
            subprocess.Popen(soffice_cmd).wait()
        
        odt_list = [f for f in  os.listdir(temp_dir) if f.endswith('.docx')]
        # URL List for previous/next
        # Oversize the array it in case we have missing chapters
        print("Converting", folder_name, "to Markdown...")
        url_list = [None] * 99
        for f0 in odt_list:
            file_name, file_ext = os.path.splitext(f0)
            file_num, file_name = file_name.split("_", maxsplit=1)
            # make the filename safe
            title_name = file_name
            file_name = re.sub(r' ', '_', file_name)
            url_list[int(file_num)] = {"url": file_name, "title": title_name}


            # Export out the base markdown to the temporary files
            bash_cmd = "pandoc \"" + path.join(temp_dir, f0) + "\" -f docx -t gfm -o " + path.join(temp_dir, file_name + ".md") + " -s --strip-comments --toc --toc-depth=6" 
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
                            header_dict[link_name] = "/" + folder_name + "/" + file_name + "/#" + link_name
                    # See if we've reached the first header.
                    elif re.match(r'==*', line):
                        # The header is on the previous line
                        break

        # Now that we've gathered all the header links, we can replace them.
        print("Post-Processing", file_dir, "...")
        for f0 in file_list:
            file_name, file_ext = os.path.splitext(f0)
            file_num, file_name = file_name.split("_", maxsplit=1)

            title_name = file_name
            # make the filename safe
            file_name = re.sub(r' ', '_', file_name)

            # Make sure the number is a number, and not a string
            file_num = int(file_num)

            # Construct the Markdown header
            header = "---\n"
            header += "layout: page\n"
            header += "base_url: " + dir_dict['base_url'] + '\n'
            header += "title: " + title_name + '\n'
            for key, value in dir_dict["header"].items():
                header += key + ": " + value + "\n"
            header += "group_order: " + str(group_order) + "\n"
            header += "order: " + str(file_num) + "\n"
            if file_num > 0 and url_list[file_num - 1]:
                header += "prev_url: " + url_list[file_num - 1]["url"] + "\n"
                header += "prev_title: " + url_list[file_num - 1]["title"] + "\n"
            if url_list[file_num + 1]:
                header += "next_url: " + url_list[file_num + 1]["url"] + "\n"
                header += "next_title: " + url_list[file_num + 1]["title"] + "\n"
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
              
                # Replace any Header 10 (Greater Charms) with the class
                # Github cannot process anything above Header 6
                header_str = r"##########\s*(.*)"
                header_replace = r"""<div class="greater_charm">\1</div>"""
                data = re.sub(header_str, header_replace, data)

                # Replace any Header 9 (Examples) with the "indent" figure
                header_str = r"#########\s(.*)"
                header_replace = r"""> \1"""
                data = re.sub(header_str, header_replace, data)

                # Make sure any blank spaces between example paragraphs get that indentation too
                header_str = r"(> .*\n)\n(> .*)"
                header_replace = r"""\1> \n\2"""
                data = re.sub(header_str, header_replace, data)

                with open(path.join(new_dir, file_name + ".md"), "w", encoding="utf8") as w:
                    w.write(header + data) 

def zip_downloads():
    print("------------------------")
    print("Zipping up...")
    zip_file = os.path.join(downloads_dir, zip_name)
    if os.path.exists(zip_file):
        os.remove(zip_file)
    
    with ZipFile(zip_file, 'w') as zip_obj:
        pdf_list = [pdf for pdf in os.listdir(downloads_dir) if pdf.endswith('.pdf')]
        
        for pdf_file in pdf_list:
            print("-",pdf_file)
            zip_obj.write( os.path.join(downloads_dir, pdf_file), arcname=pdf_file)

def export_pdf(folder_name):
    folder_dir = path.join(src_dir, folder_name)
    master_file_list = [f for f in  os.listdir(folder_dir) if f.endswith('.odm')]
    for master_file in master_file_list:
        # Create the pdf
        print("Converting", master_file, "to pdf...")
        soffice_cmd = soffice + " --headless \"" + os.path.join(folder_dir, master_file) + "\" \"macro:///" + macro_name +"\""
        subprocess.Popen(soffice_cmd).wait()

        # Move it to the downloads folder
        file_name, file_ext = os.path.splitext(master_file)
        src_file = os.path.join(folder_dir, file_name + ".pdf")
        dest_file = os.path.join(downloads_dir, file_name + ".pdf")
        if os.path.exists(dest_file):
            os.remove(dest_file)
        shutil.move(src_file, dest_file)

def main(args):
    print("------------------------")
    print("Starting Release!")

    # Export out the Summary document
    if (args.file.lower() == "all" or args.file.lower() == "summary"):
        soffice_cmd = soffice + " --convert-to pdf " + path.join(src_dir, "tools","Summary.odt") + " --outdir " + downloads_dir
        print("------------------------")
        print("Converting Summary to pdf...")
        subprocess.Popen(soffice_cmd).wait()

    group_order = start_index
    # Create the release
    for dir_dict in src_list:
        folder_name = dir_dict["folder"]
        if (args.file.lower() == "all" or args.file.lower() == folder_name.lower()):
            # Export out to Markdown
            procces_dir(dir_dict, group_order)

            # Export out to pdf
            export_pdf(folder_name)
        group_order += 1
    # Zip all the downloads
    zip_downloads()
    print("------------------------")
    print("Done!")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='?', default="all")
    args = parser.parse_args()
    main(args)
