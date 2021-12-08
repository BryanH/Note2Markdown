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


def next_line(view, pt):
    return view.line(pt).b + 1


def prev_line(view, pt):
    return view.line(pt).a - 1


def set_pref(view, name, value):
    view.settings().set(name, value)


def check_syntax(synt):
    a = synt.get('syntax')
    # TODO - assign-syntax(syntax)
    sublime.message_dialog("Le syntax is [" + a + "]")
    # TODO - if current syntax is text, then go for it


def save_handler(results):

    # view = sublime.View().view
    view = self.view
    if results is None:
        a = 0
        sublime.message_dialog("Looks like they didn't save")
        view.set_status("save", "Didn't save")
    else:
        try:
            view.set_status("save", "Saved to " + results)
            f = open(results, 'w')

            # This isn't working:
            f.write(view.substr(sublime.Region(0, view.size())))
            f.close()
            # sublime.status("They saved! [" + results + "]")
        except Exception as error:
            sublime.error_message('Unable to save file: [{0}]'.format(error))
            return None


def saveit(fname, extension):
    sublime.save_dialog(save_handler,
                        None,
                        None,
                        fname,
                        extension)


def filenameify(title, settings):
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


def get_settings(view):
    settings_vals = {}
    settings = sublime.load_settings("note_to_markdown.sublime-settings")
    for key in SETTINGS_KEYS:
        settings_vals[key] = settings.get(key)

    # sublime.message_dialog("Extention is [{extension}]"
    #                        .format(**settings_vals))

    return settings_vals


class Note2mdCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.set_status("A", "Note2MD started")
        sublime.log_result_regex(True)
        sublime.log_commands(True)
        settings = get_settings(self.view)
        # check_syntax(self.view.settings())

        # Get the contents of the first line
        point = self.view.text_point(0, 0)
        firstLineRegion = self.view.line(point)
        firstLine = self.view.substr(firstLineRegion)
        saveit(filenameify(firstLine, settings), settings['extension'])
        self.view.erase_status("A")
        # self.view.insert(edit, point, filenameify(firstLine))
