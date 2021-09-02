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


def next_line(view, pt):
    return view.line(pt).b + 1


def prev_line(view, pt):
    return view.line(pt).a - 1


def filenameify(title):
    todays = datetime.now()
    nopunct = re.compile(r'[\"\'\\\/\$\%\#\@=+\^]+')
    nospace = re.compile(r'\s+')

    # TODO - use preferences for space replacement
    fixed = nospace.sub("_", title.lower().strip(' #\t\n\r'))
    # TODO - use preferences for punctuation replacement
    fixed1 = nopunct.sub('', fixed)
    # TODO - use preferences for suffix string
    # TODO - use preferences for date/time string
    return todays.strftime("%Y%m%d_%H%M-") + fixed1 + ".md" + "\n"


class Note2mdCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        sublime.log_result_regex(True)
        sublime.log_commands(True)

        firstLine = "# The Quick Brown Fox"
        # Get the contents of the first line
        point = self.view.text_point(0, 0)
        firstLineRegion = self.view.line(point)
        firstLine = self.view.substr(firstLineRegion)
        self.view.insert(edit, point, filenameify(firstLine))
