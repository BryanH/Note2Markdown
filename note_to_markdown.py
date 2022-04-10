import os
import re
import sublime
import sublime_plugin

from datetime import datetime
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
# TODO: date format from preferences
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
                  "substitution-punt"
                ]

class GenerateUserSettingsCommand(sublime_plugin.WindowCommand):
    def run(self, package_name, settings_name):
        fpath = os.path.join(sublime.packages_path(), "User", settings_name)
        if not os.path.exists(fpath):
            try:
                content = sublime.load_resource("Packages/{0}/{1}".format(
                    package_name, settings_name))
                print("Content: " + content)
                with open(fpath, "w") as f:
                    f.write(content)
            except:
                print("Error setting up default settings.")
        else:
            print(settings_name + " already exists, no action")
        self.window.open_file(fpath)


class Note2MdCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        view.set_status("A", "Note2MD started")
        sublime.log_result_regex(True)
        sublime.log_commands(True)
        settings = self.get_settings(view)
        self.check_syntax(self.view.settings())

        # Get the contents of the first line
        point = view.text_point(0, 0)
        firstLineRegion = view.line(point)
        firstLine = view.substr(firstLineRegion)
        self.saveit(self.filenameify(firstLine, settings), settings['extension'])
        view.erase_status("A")
        # self.view.insert(edit, point, filenameify(firstLine))

    def next_line(view, pt):
        return view.line(pt).b + 1


    def prev_line(view, pt):
        return view.line(pt).a - 1


    def set_pref(view, name, value):
        view.settings().set(name, value)


    def check_syntax(self, synt):
        a = synt.get('syntax')
        # TODO - assign-syntax(syntax)
        view.set_status
        # sublime.message_dialog("Le syntax is [" + a + "]")
        # TODO - if current syntax is text, then go for it


    def save_handler(self, results):

        # view = sublime.View().view
        view = self.view
        if results is None:
            a = 0
            view.set_status("save", "Didn't save")
        else:
            try:

                view.set_status("save", "Saving...")
                f = open(results, 'w')

                # This isn't working:
                f.write(view.substr(sublime.Region(0, view.size())))
                f.close()

                view.set_status("save", "Saved to " + results)
            except Exception as error:
                sublime.error_message('Unable to save file: [{0}]'.format(error))
                return None


    def saveit(self, fname, extension):
        sublime.save_dialog(self.save_handler,
                            None,
                            None,
                            fname,
                            extension)


    def filenameify(self, title, settings):
        todays = datetime.now()
        nopunct = re.compile(r'[\.\"\'\\\/\$\%\#\@=+\^]+')
        nospace = re.compile(r'\s+')
        extension = settings['extension']
        time_format = settings['prefix-format']
        delimiter_space = settings['substitution-space']

        # delimiter_punct = settings['substitution-punct']
        fixed = nospace.sub(delimiter_space, title.lower().strip(' #.\t\n\r'))
        fixed1 = nopunct.sub(r'+', fixed)
        return todays.strftime(time_format) + fixed1 + r'.' + extension


    def get_settings(self, view):
        settings_vals = {}
        settings = sublime.load_settings("Note2Md.sublime-settings")
        for key in SETTINGS_KEYS:
            settings_vals[key] = settings.get(key)

        # sublime.message_dialog("Extention is [{extension}], prefix format [{prefix-format}], sub-space [{substitution-space}]"
        #                        .format(**settings_vals))

        return settings_vals
