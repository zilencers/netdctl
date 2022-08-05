import os
from datetime import datetime
from zipfile import ZipFile

from app.command.icommand import ICommand
from utils.file_io import FileIO
from utils.config import Config


class ArchiveCommand(ICommand):
    def __init__(self, args) -> None:
        super().__init__()

        self._args = args


    def execute(self):
        if self._args.restore:
            self._restore()
        elif self._args.name:
            self._archive(self._args.name)
        else:
            self._archive(self._gen_arcname())


    def _archive(self, arcname: str):
        """ A method for archiving network configuration """

        FileIO.dir_exists(Config.archive_path, True)
        FileIO.dir_exists(Config.tmp_path, True)

        files = [x for x in FileIO.get_files(Config.networkd_path)]

        [FileIO.copy(os.path.join(Config.networkd_path, x), Config.tmp_path) for x in files]
    
        cwd = os.getcwd()
        os.chdir(Config.tmp_path)

        with ZipFile(arcname, 'w') as zip:
            [zip.write(x) for x in files]

        FileIO.copy(arcname, Config.archive_path)

        os.chdir(cwd)

        FileIO.remove_dir(Config.tmp_path)


    # TODO: Should existing configuration be deleted before restore?
    def _restore(self):
        """ A method for restoring archived network configuration """

        print("WARNING: This process will overwite the current configuration")
        print("Proceed with restoring (Y/n): ", end="")
        choice = input()

        if choice.lower() == 'y':
            archive = self._get_archive()
            self._extract(archive, Config.networkd_path)
        
        print("Restore process complete...")
        print("Run 'netdctl reload' to restart the service")


    def _extract(self, arcname: str, path='.'):
        """ A method for extracting archived network configuration """

        zip = ZipFile(os.path.join(Config.archive_path, arcname))
        zip.extractall(path)
        zip.close()

    
    def _get_archive(self):
        """ A method to retrieve the correct archive for restoration """

        archive_files = FileIO.get_files(Config.archive_path)
        
        if len(archive_files) > 1:
            print("Please choose an archive to restore:")
        
            count = 1
            for archive in archive_files:
                print("{}) {}".format(count, archive))
                count += 1

            print("choice: ", end='')
            choice = input()

            return archive_files[int(choice)-1]

        return archive_files


    def _gen_arcname(self):
        """ Generate an archive name """
        
        dt = datetime.now().strftime('%Y%m%d_%H%M%S')
        return Config.arcname.replace('{datetime}', dt)
