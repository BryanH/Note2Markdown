"""note_to_markdown.py"""

import re
from datetime import datetime

import sublime
import sublime_plugin
# from datetime import date

# note_to_markdown.py
#
# Subline Text plugin to convert raw notes in markdown format
# (but classified as text):
#    extract the document title (first header)
#    lower-case & replace spaces with underscores
#    prefix with timestamp
#    suffix it with markdown extension
# Open save dialog with the filename as generated above
#
# TODO: word delimiter from preferences
#
# Check the validity of this script by:
# flake8 note_to_markdown.py

# delimiter_space = "_"
# delimiter_punct = ""
# extension = "md"

SETTINGS_KEYS = [
    "extension",
    "prefix-format",
    "substitution-space",
    "substitution-punct",
    "debug",
]


class Note2MdCommand(sublime_plugin.TextCommand):
    """Plugin Class"""

    def run(self, _):
        """Main Loop"""

        view = self.view
        if not view.is_dirty():
            sublime.message_dialog("File already saved. Aborting.")
            return

        settings = self.get_settings()
        self.check_syntax(self.view.settings())
        if settings["debug"]:
            view.set_status("A", "Note2MD started")

            # Flood the console with everything the user does
            sublime.log_commands(True)
            sublime.log_result_regex(True)

        # Get the contents of the first line
        point = view.text_point(0, 0)
        first_line_region = view.line(point)
        first_line = view.substr(first_line_region)
        self.saveit(self.filenameify(first_line, settings), settings["extension"])
        if settings["debug"]:
            view.erase_status("A")

    def next_line(self, view, pt):
        """return the line number of the line below the current line"""

        return view.line(pt).b + 1

    def prev_line(self, view, pt):
        """return the line number of the line above the current line"""

        return view.line(pt).a - 1

    def set_pref(self, view, name, value):
        """Update (set) the preferences settings"""

        view.settings().set(name, value)

    def check_syntax(self, synt):
        """Not sure what this is for"""

        settings = self.get_settings()

        # TODO: is this trying to see if the file syntax is "Markdown"/"Multimarkdown"?
        a = synt.get("syntax")
        # TODO: assign-syntax(syntax)

        if settings["debug"]:
            self.view.set_status("check", f"Le syntax is [{a}]")

        # TODO: if current syntax is text, then go for it

    def save_handler(self, results):
        """Saves the document into the filename selected"""

        view = self.view
        settings = self.get_settings()
        if results is None:
            view.set_status("save", "Didn't save")
        else:
            view.erase_status("check")
            view.set_status("save", "Saving...")

            content = view.substr(sublime.Region(0, view.size()))
            sublime.message_dialog(content)
            try:
                with open(results, "w", encoding="utf-8") as f:
                    f.write(content)

                # TODO This isn't working:
                # f.write(view.substr(sublime.Region(0, view.size())))
                # f.close()

                if settings["debug"]:
                    view.set_status("save", "Saved to " + results)

            except OSError as error:
                sublime.error_message(f"Unable to save file: [{error}]")

    def saveit(self, fname, extension):
        """Open save dialog, it will call the save_handler"""

        # Stop Flooding the console with all the things
        sublime.log_commands(False)
        sublime.save_dialog(self.save_handler, None, None, fname, extension)

    def filenameify(self, title, settings):
        """Format the filename to save as"""

        todays = datetime.now()
        nopunct = re.compile(r"[\.\"\'\\\/\$\%\#\@=+\^]+")
        nospace = re.compile(r"\s+")
        extension = settings["extension"]
        time_format = settings["prefix-format"]
        delimiter_space = settings["substitution-space"]

        # delimiter_punct = settings['substitution-punct']
        fixed = nospace.sub(delimiter_space, title.lower().strip(" #.\t\n\r"))
        fixed1 = nopunct.sub(r"+", fixed)
        return todays.strftime(time_format) + fixed1 + r"." + extension

    def get_settings(self):
        """Retrieve existing preferences from default and user"""

        settings_vals = {}
        settings = sublime.load_settings("Note2Md.sublime-settings")
        for key in SETTINGS_KEYS:
            settings_vals[key] = settings.get(key)

        if settings["debug"]:
            sublime.message_dialog(
                (
                    f"Extention is [{settings['extension']}],"
                    f" prefix format [{settings['prefix-format']}],"
                    f" sub-space [{settings['substitution-space']}], "
                    f" sub-punct [{settings['substitution-punct']}], "
                    f" debug [{settings['debug']}]"
                )
            )

        return settings_vals
