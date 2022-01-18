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

power_categories = r"(Lesser|Greater|Capstone|Emerald|Sapphire|Adamant|Lesser Techniques|Greater Techniques|Capstone Technique)"

# Define some local paths (may need to change this later)
script_dir = os.path.dirname(__file__)
src_dir = path.join(script_dir, "src")
page_dir = path.join(script_dir, "docs")
downloads_dir = path.join(page_dir, "assets", "downloads")
soffice = "\"C:\\Program Files\\LibreOffice\\program\\soffice\""
zip_name = "Exalted_Reincarnated.zip"

macro_name = "Standard.Exalted.export_to_pdf"

def clean_name(name):
    name = re.sub(r"[\s`~/{}]", '-', name).strip()
    # make the filename safe
    return re.sub(r' ', '_', name)

header_dict = {}
url_dict = {}
# Start a new Header Linkage replacement.
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

def procces_dir(src_dir):
    with tempfile.TemporaryDirectory() as temp_dir:

        file_list = [f for f in  os.listdir(src_dir) if (f.endswith('.odt') and re.match(r"^\d\d_", f))] 
       
        for f in file_list:
            print("------------------------")
            print("Processing", f)

            # Export all to docx
            # For some reason, pandoc doesn't work well with odt. So we have to go to docx first using libreoffice
            print("Exporting", f, "to docx...")
            soffice_cmd = soffice + " --headless --convert-to docx \"" + path.join(src_dir, f) + "\" --outdir " + temp_dir
            subprocess.Popen(soffice_cmd).wait()

            # Export out the base markdown to the temporary files
            print("Exporting", f, "to md...")
            bare_name = os.path.splitext(f)[0]
            bash_cmd = "pandoc \"" + path.join(temp_dir, bare_name + ".docx") + "\" -f docx -t gfm -o " + path.join(temp_dir, clean_name(bare_name) + ".md") + " -s --strip-comments --toc --toc-depth=6" 
            subprocess.Popen(bash_cmd).wait() 
                    
        md_list = [f for f in  os.listdir(temp_dir) if f.endswith('.md')]
        for file_name in md_list:
            url_list = []
            # Consume the table of Contents
            with open(path.join(temp_dir, file_name), "r+", encoding="utf8") as f:
                file_name, file_ext = os.path.splitext(file_name)
                file_num, file_name = file_name.split("_", maxsplit=1)

                data_arr = f.readlines()
                header1_name = "test"
                
                for line in data_arr:
                    if not line.strip():
                        break
                    else:
                        # Consume the table of contents
                        match = re.search(r'(\[.*\])?\(#(.*)\)', line)
                        if match:
                            # Create a link to include the file name.
                            link_name = match.group(2)
                            if (line[0] == "-"):
                                header1_name = match.group(1)[1:-1]
                                url_list.append(header1_name)
                            elif link_name not in header_dict:
                                header_dict[link_name] = "/" + file_name + "/" + header1_name + "/#" + link_name
            
            url_dict[file_name] = url_list
        
        # Chunk out the document into smaller pieces
        for file_name in md_list:
            with open(path.join(temp_dir, file_name), "r+", encoding="utf8") as f:
                file_name, file_ext = os.path.splitext(file_name)
                file_num, file_name = file_name.split("_", maxsplit=1)

                data_arr = f.readlines()
                arr_size = len(data_arr)

                start_index = -1
                for index in range(arr_size):
                    line = data_arr[index]
                    if re.match(r'===*', line):
                        if start_index >= 0:
                            create_split(file_name, file_num, data_arr[start_index:(index-1)])
                        start_index = index -1
                # final split
                create_split(file_name, file_num, data_arr[start_index:])

                    
def create_split(file_name, file_num, data_arr):
    # Create the header
    title_name = data_arr[0].strip()
    url_list = url_dict[file_name]

    index = url_list.index(title_name)
    if index < 0:
        print("help, no index")
        exit()

    # Construct the Markdown header
    header = ["---", 
            "layout: page", 
            "base_url: " + file_name,
            "title: " + title_name,
            "order: " + str(index),
            "group_order: " + str(int(file_num) + start_index)]
    if (index > 0 and url_list[index - 1]):
        header.extend(["prev_url: " + url_list[index - 1],
                    "prev_title: " + url_list[index - 1]])
    if index + 1 < len(url_list):
        header.extend(["next_url: " + url_list[index + 1],
                    "next_title: " + url_list[index + 1]])
    header.extend(["---", ""])
    header_text = "\n".join(header)
    

    # Trim the top off
    data = "".join(data_arr[2:])

    # Replace the intra-document hyperlinks
    link_str = r"\(#[^#\n]*\)"
    data = re.sub(link_str, replace_link, data)
    
    # Find and replace the categories list
    repl_str = r"""\n<div class="power_category">\1</div>\n"""
    data = re.sub("\n"+power_categories+"\n", repl_str, data)

    # # Replace any Header 9 (Examples) with the "indent" figure
    # header_str = r"#########\s(.*)"
    # header_replace = r"""> \1"""
    # data = re.sub(header_str, header_replace, data)

    # # Make sure any blank spaces between example paragraphs get that indentation too
    # header_str = r"(> .*\n)\n(> .*)"
    # header_replace = r"""\1> \n\2"""
    # data = re.sub(header_str, header_replace, data)

     # Create a directory for each subdocument
    new_dir = path.join(page_dir, file_name)
    if not path.exists(new_dir):
        os.makedirs(new_dir)
        

    with open(path.join(page_dir, file_name, title_name + ".md"), "w", encoding="utf8") as w:
        w.write(header_text)
        w.write(data) 

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

def export_pdf(folder_dir):
    master_file_list = [f for f in  os.listdir(folder_dir) if f.endswith('.odm')]
    for master_file in master_file_list:
        file_name, file_ext = os.path.splitext(master_file)
        pdf_file = os.path.join(folder_dir, file_name + ".pdf")
        dest_file = os.path.join(downloads_dir, file_name + ".pdf")

        # Create the pdf
        print("Converting", master_file, "to pdf...")
        soffice_cmd = soffice + " --headless \"" + os.path.join(folder_dir, master_file) + "\" \"macro:///" + macro_name +"\""
        subprocess.Popen(soffice_cmd).wait()

        # Move it to the downloads folder
        if os.path.exists(dest_file):
            os.remove(dest_file)
        shutil.move(pdf_file, dest_file)

def main(args):
    print("------------------------")
    print("Starting Release!")

    # Export out the Summary document
    if (args.file.lower() == "all" or args.file.lower() == "summary"):
        soffice_cmd = soffice + " --convert-to pdf " + path.join(src_dir, "Summary.odt") + " --outdir " + downloads_dir
        print("------------------------")
        print("Converting Summary to pdf...")
        subprocess.Popen(soffice_cmd).wait()
    
    # Export out the Character Creation section seperately
    if (args.file.lower() == "all" or args.file.lower() == "cc"):
        soffice_cmd = soffice + " --convert-to pdf \"" + path.join(src_dir, "01_Character Creation.odt") + "\" --outdir " + downloads_dir
        print("------------------------")
        print("Converting Character Creation to pdf...")
        subprocess.Popen(soffice_cmd).wait()
        print(soffice_cmd)
        shutil.move(os.path.join(downloads_dir, "01_Character Creation.pdf"), os.path.join(downloads_dir, "Character_Creation.pdf"))


    # Create the release
    group_order = start_index
    # Export out to Markdown
    procces_dir(src_dir)
    # Export out to pdf
    export_pdf(src_dir)

    # Zip all the downloads
    zip_downloads()
    print("------------------------")
    print("Done!")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='?', default="all")
    args = parser.parse_args()
    main(args)
