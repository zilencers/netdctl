import os
import pandas
import re
import sys
import shutil
import subprocess
from utils.file_io import FileIO


class Helpers:

    @staticmethod
    def gen_filename(search: list, prefix: int, ext: str, iface: str):
        """Generate a valid systemd-networkd filename
           Args:
                param: search    path to search
                param: ext       file extension
                param: iface     interface name

            Return:
                str
        """
        # get a list of configuration files
        file_lists = [FileIO.get_files(x) for x in search]

        # flatten out file_lists
        files = [x for x in file_lists for file in x]

        # if no config exists, return with a filename
        if len(str(files)) <= 2:
            return "{}-{}.{}".format(prefix, iface, ext)

        # flatten and filter by the specified iface
        iface_cfg_files = []
        cfg_files = []
        for ls in file_lists:
            for file in ls:
                cfg_files.append(file)
                if re.search(iface, file):
                    iface_cfg_files.append(file)

        # check for config file with the specified extension
        cfg_exists = [x for x in iface_cfg_files if re.search(ext, x)]

        if cfg_exists:
            print("Error: confguration already exists for this interface", 
                file=sys.stderr)
            sys.exit(1)
        
        # Use the same prefix if config exist for the interface
        iface_cfg_exists = [x for x in iface_cfg_files if re.search(iface, x)]

        if iface_cfg_exists:
            iface_prefix = iface_cfg_files[0][:2]
            return "{}-{}.{}".format(iface_prefix, iface, ext)

        # Sort cfg_files and determine the next prefix
        cfg_files.sort()
        next_prefix = int(cfg_files[-1][:2]) + 5

        return "{}-{}.{}".format(next_prefix, iface, ext)


    @staticmethod
    def delete_config(file_paths: list, iface: str, ext=None):
        """Delete the specified systemd-networkd config file 
        
           Args:
               param: file_path     list of file paths to search
               param: iface         name of network interface
               param: type          file extension (.link, .netdev, .network)

            Return:
               None
        """
        if ext is None:
            raise ValueError('type cannot be None')

        files = []
        for p in file_paths:
            cfg_files = FileIO.files_by_type(p, ext)
            for f in cfg_files:
                files.append(os.path.join(p,f))

        for file in files:
            pattern = "{}.{}".format(iface, ext)
            if re.search(pattern, file):
                try:
                    os.remove(file)
                except OSError as e:
                    print(e, file=sys.stderr)


    @staticmethod
    def update_config(paths: list, ext: str, net_map: dict, **kwargs):
        """Update the specified config file 
        
           Args:
               param: paths         list of file paths to search
               param: ext           file extension (.link, .netdev, .network)
               param: net_map       mapping of arguments to config field names
               param: **kwargs      dict of args          

            Return:
               None
        """
        # Get all files of the specified ext type
        results = [FileIO.files_by_type(x, True, ext) for x in paths]
        
        # Flatten out results
        files = [x for file in results for x in file]
        
        # Determine the correct file to modify 
        pattern = re.compile(r"\d{2}-" + kwargs['iface'] + "." + ext)
        cfg_file = [x for x in files if re.match(pattern, os.path.basename(x))]

        # Determine what value to modify
        mod = {}
        key = None
        for k, v in kwargs.items():
            if k in net_map.keys() and v is not None:
                key = k
                mod.update({k: net_map[k]})
        
        # Read file and replace
        lines = []
        data = FileIO.readlines("".join(cfg_file))
        for line in data:
            if re.search(mod[key], line):
                lines.append("{}={}\n".format(mod[key], kwargs[key]))
            else:
                lines.append(line)

        # Write out new config
        with open("".join(cfg_file), 'w+') as f:
            f.writelines(lines)


    @staticmethod
    def get_mac_addr(file_path: str, iface: str):
        """Retrieve mac address for the specified interface 
        
           Args:
              param: file_path      path to search for the mac address
              param: iface          network interface 

            Return:
               str
        """
        return FileIO.read(file_path.replace('{iface}', iface))


    @staticmethod
    def write_config(file_path: str, filename: str, template_path: str, 
                    template_name: str, **kwargs: dict):

        if not os.path.exists(os.path.dirname(file_path)):
            raise OSError('Path not found')

        template_file = os.path.join(template_path, template_name)
        if not FileIO.file_exists(template_file):
            raise OSError("File Not Found")

        # Read the template file and convert to it to a string
        template = FileIO.readlines(template_file)
        template = "".join(template)

        # Create a new variable from kwargs without any None values
        args = {key:value for (key,value) in kwargs.items() if value is not None}

        # Loop through args dict; search the template for matching keys; replace if found
        for key, value in args.items():                    
            pattern = "{" + key + "}"
            if re.search(key, template):
                template = template.replace(pattern, str(value))

        # Remove lines from the template that were not replaced
        pattern = re.compile(r'\w+={\w+}')

        while True:
            search_result = re.search(pattern, template)
            if search_result is None:
                break

            template = template.replace(search_result.group(),'')
            template = template.rstrip()

        FileIO.write(os.path.join(file_path, filename), template)


    @staticmethod
    def parse(path: str, fields: list, ext=None):
        """ Parse the specified file type

           Args:
              param: path      file path
              param: fields    search fields 
              param: ext       file type 

            Return:
               list
        """ 
        # Get network files from /etc/systemd/network
        cfg_files = []
        for file in FileIO.files_by_type(path, True, ext):
            cfg_files.append(FileIO.readlines(file))

        data = []
        for file in cfg_files:
            file_data = []
            for elem in file:
                for field in fields:
                    if re.search(field, elem):
                        file_data.append(elem.split('=')[1].replace('\n', ''))
            data.append(file_data)

        return data


    @staticmethod
    def display(data: list, headers: list):
        if data:
            df = pandas.DataFrame(data)
            df.columns = headers
            print("\n {} \n".format(df))


    @staticmethod
    def move_config(src: str, dest: str): 
        files = FileIO.files_by_type(src)

        for file in files:
            shutil.move(os.path.join(src, file), os.path.join(dest, file))


    @staticmethod
    def run(cmd: list, shell=False, text=True, cap_output=True, check=True):
        result = subprocess.run(
            cmd, 
            shell=shell, 
            text=text, 
            capture_output=cap_output, 
            check=check
        )
        return result

