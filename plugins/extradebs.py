import snapcraft
import os
import subprocess
from typing import List
import collections
import logging
from snapcraft.internal import errors

logger = logging.getLogger(__name__)

class ExtraDebs(snapcraft.BasePlugin):

    @classmethod
    def schema(cls):
        schema = super().schema()

        # Add a new property called "my-property"
        schema['properties']['extra-debs'] = {
            "type": "array",
            "uniqueItems": True,
            "items": {"type": "string"},
        }

        # The "my-option" property is now required
        #schema['required'].append('extra-debs')

        return schema

    def pull(self):
        super().pull()

        print ('Start pulling extra debs')
        deb_files = ["%s/../../project/snap/%s" % (self.partdir, file) for file in self.options.extra_debs]
        self._install_extra_debs(deb_files)

    #def build(self):
    #    super().build()
    #    print('Look ma, I built!')

    @classmethod
    def _install_extra_debs(cls, deb_files: List[str]) -> None:
        deb_files.sort()
        logger.info("Installing extra deb files: %s", " ".join(deb_files))
        env = os.environ.copy()
        env.update(
            {
                "DEBIAN_FRONTEND": "noninteractive",
                "DEBCONF_NONINTERACTIVE_SEEN": "true",
                "DEBIAN_PRIORITY": "critical",
            }
        )

        dpkg_command = [
            "sudo",
            "--preserve-env",
            "dpkg",
            "-i",
        ]

        try:
            subprocess.check_call(dpkg_command + deb_files, env=env)
        except subprocess.CalledProcessError:
            raise errors.BuildPackagesNotInstalledError(packages=deb_files)

        package_names = [deb.split("/")[-1].split('_')[0] for deb in deb_files]
        try:
            subprocess.check_call(["sudo", "apt-mark", "auto"] + package_names, env=env)
        except subprocess.CalledProcessError as e:
            logger.warning(
                "Impossible to mark packages as auto-installed: {}".format(e)
            )

