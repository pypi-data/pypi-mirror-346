"""
Top level module for dynaddrmgr application.

Classes:
    TemplateManager
"""

import filecmp
from os import R_OK, W_OK, access
from pathlib import Path
from shutil import copy2
from tempfile import NamedTemporaryFile
from typing import Optional

from jinja2 import Template

from wtforglib.commander import Commander
from wtforglib.dirs import verify_directory
from wtforglib.fstats import set_owner_group_perms
from wtforglib.kinds import StrAnyDict
from wtforglib.options import OptionsDict
from wtforglib.versioned import unlink_path
from wtforglib.versionfile import version_file

KDEST: str = "dest"


class TemplateWriter(Commander):  # noqa: WPS214
    """
    Template generator.

    This class is responsible for managing the templates specified
    in the configuration file.
    """

    changed: bool

    def __init__(
        self,
        opts: Optional[OptionsDict] = None,
    ) -> None:
        """Constructs a new instance of TemplateWriter.

        Parameters
        ----------
        opts : Optional[OptionsDict], optional
            Options dictionary, by default None
        """
        super().__init__(opts)
        self.changed = False

    def generate(
        self,
        tmpl_name: str,
        tmpl_value: StrAnyDict,
        tmpl_var: StrAnyDict,
    ) -> int:
        """Generates the template if needed.

        Parameters
        ----------
        tmpl_name : str
            Template name
        tmpl_value : StrAnyDict
            Template information
        tmpl_var : StrAnyDict
            Template variable data

        Returns
        -------
        int
            Exit code
        """
        self.changed = False
        if self._verify_config_data(tmpl_name, tmpl_value):
            return self._update_template(tmpl_value, tmpl_var)
        return 1

    def _update_template(self, tmpl_value: StrAnyDict, tmpl_var: StrAnyDict) -> int:
        """Update the template if necessary.

        Parameters
        ----------
        tmpl_value : StrAnyDict
            Data describing the target file requirements
        tmpl_var : StrAnyDict
            Variables used by the template

        Returns
        -------
        int
            exit status
        """
        dest: str = tmpl_value.get(KDEST, "")
        self.changed = self._render_template(
            tmpl_value,
            tmpl_var,
        )
        if self.changed:
            self.info("Updated: {0}".format(dest))
            if not self.istest():
                set_owner_group_perms(
                    dest,
                    tmpl_value.get("owner", ""),
                    tmpl_value.get("group", ""),
                    tmpl_value.get("mode", ""),
                )
                return self._on_changed(tmpl_value)
        else:
            self.debug("Unchanged dest: {0}".format(dest))
        return 0

    def _on_changed(self, tmpl_value: StrAnyDict) -> int:
        """Execute the args specified in config .

        Parameters
        ----------
        tmpl_value : StrAnyDict
            Config values

        Returns
        -------
        int
            Exit code
        """
        cargs = tmpl_value.get("on_changed", [])
        if cargs:
            cmdres = self.run_command(tuple(cargs), check=False)
            if cmdres.returncode != 0:
                self.error("command: {0}".format(" ".join(cargs)))  # noqa: WPS421
                self.error("returncode: {0}".format(cmdres.returncode))  # noqa: WPS421
                self.error("stderr: {0}".format(cmdres.stderr))  # noqa: WPS421
            return cmdres.returncode
        return 0

    def _verify_config_data(self, tmpl_name: str, tmpl_value: StrAnyDict) -> bool:
        """Verifies the configuration.

        Parameters
        ----------
        tmpl_name : str
            Name of the template
        tmpl_value : StrAnyDict
            Template values

        Returns
        -------
        bool
            True if the configuration is valid
        """
        if self._verify_template_required_keys(tmpl_name, tmpl_value):
            if self._verify_template_source(tmpl_value.get("src", "")):
                if self._verify_target(tmpl_value.get(KDEST, "")):
                    return True
        return False

    def _render_template(
        self,
        tmpl_value: StrAnyDict,
        tmpl_var: StrAnyDict,
    ) -> bool:
        """Render the template to the file system.

        Parameters
        ----------
        tmpl_value : StrAnyDict
            Data describing the target file requirements
        tmpl_var : StrAnyDict
            Variables used by the template

        Returns
        -------
        int
            exit_code
        """
        # Environment(keep_trailing_newline=True)
        dest = tmpl_value.get(KDEST, "")
        bnbr = tmpl_value.get("backup", 0)
        bpath = tmpl_value.get("backup_dir")
        template = Template(self._read_template_source(tmpl_value.get("src", "")))
        tfile = NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=None,
            delete=False,
        )
        tfile.write(template.render(template_dict=tmpl_var))
        tfile.close()
        return self._write_output(Path(dest), Path(tfile.name), bnbr, bpath)

    def _write_output(
        self,
        dpath: Path,
        tpath: Path,
        bnbr: int,
        bpath: Optional[Path] = None,
    ) -> bool:
        """Write output to output file, unlink temporary file.

        Parameters
        ----------
        dpath : Path
            Path to the output file
        tpath : Path
            Path to the temporary generated template file
        bnbr : int
            Number of backups to keep if any
        bpath : Optional[Path]
            Directory to store the backups in

        Returns
        -------
        bool : True if target file replaced
        """
        retval = False
        if dpath.exists():
            diff = filecmp.cmp(dpath, tpath)
            exists = True
        else:
            exists = False
            diff = False
        self.debug(
            "dest: {0} exists: {1} diff: {2}".format(str(dpath), exists, diff),
        )
        if not diff:
            if not self.options.get("noop", False):
                if exists:
                    self._backup_file(str(dpath), bnbr, bpath)
                copy2(tpath, dpath)
                self.info("Updated file: {0}".format(str(dpath)))
                retval = True
        if not self.isdebug():
            unlink_path(tpath, missing_ok=True)
        return retval

    def _backup_file(self, dest: str, bnbr: int, bpath: Optional[Path] = None) -> None:
        """Backup the output before replacing.

        Parameters
        ----------
        dest : str
            Path to output file.
        bnbr : int
            Number of backup files to keep (if any)
        bpath : Optional[Path]
            Directory to store the backups in
        """
        if bnbr:
            if bpath is None:
                version_file(dest, "rename", bnbr, self.isdebug())
            else:
                version_file(dest, "rename", bnbr, self.isdebug(), str(bpath))

    def _read_template_source(self, source: str) -> str:
        """Return the template data from the given source.

        Parameters
        ----------
        source : str
            Path to the template source

        Returns
        -------
        str
            The template data
        """
        with open(source, "r") as jinja_file:
            return jinja_file.read()

    def _verify_template_required_keys(
        self,
        tmpl_name: str,
        tmpl_value: StrAnyDict,
    ) -> bool:
        """Verify that the template required keys exist."""
        for key in ("src", KDEST):
            kv = tmpl_value.get(key)
            if kv is None:
                self.error(
                    "Template {0} does not have a {1} key!!".format(tmpl_name, key),
                )
                return False
        return True

    def _verify_target(self, dest: str) -> bool:
        """Verifies the output file.

        Parameters
        ----------
        dest : str
            Path to the output file

        Returns
        -------
        bool
            True if target directory exists and writable and file does not exist
            True if target exists, is a file, and writable
        """
        dspec = Path(dest)
        if dspec.exists():
            if not dspec.is_file():
                self.error("Template dest '{0}' not a file!!".format(dest))
                return False
            if not access(dspec, W_OK):
                self.error("Template dest '{0}' not writable!!".format(dest))
                return False
        else:
            return self._verify_target_directory(dspec.parent)
        return True

    def _verify_target_directory(self, pspec: Path) -> bool:
        """Verifies the target directory.

        Parameters
        ----------
        pspec : Path
            Path to the target directory

        Returns
        -------
        bool
            True if exists, is directory and is writable.
        """
        retval, error_message = verify_directory(pspec)
        if not retval:
            self.error(error_message)
        return retval

    def _verify_template_source(self, source: str) -> bool:
        """Verifies the template source.

        Parameters
        ----------
        source : str
            Path to the template source

        Returns
        -------
        bool
            True if source exists, is a file, is readable
        """
        spec = Path(source)
        if not spec.exists():
            self.error("Template src '{0}' not found!!".format(source))
            return False
        if not spec.is_file():
            self.error("Template src '{0}' not a file!!".format(source))
            return False
        if not access(spec, R_OK):
            self.error("Template src '{0}' not readable!!".format(source))
            return False
        return True
