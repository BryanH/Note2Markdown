import re
import sublime
import sublime_plugin

# from datetime import date
from datetime import datetime


def next_line(view, pt):
    return view.line(pt).b + 1


def prev_line(view, pt):
    return view.line(pt).a - 1


def filenameify(title):
    todays = datetime.now()
    nospace = re.compile(r'\s+')

    fixed = nospace.sub("_", title.lower().strip(' #\t\n\r'))

    # TODO - use preferences for suffix string
    # TODO - use preferences for date/time string
    return "foo" #todays.strftime("%Y%m%d_%H%M-") + fixed + ".md_bonus" + "\n"

class Note2mdCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        sublime.log_result_regex(True)
        sublime.log_commands(True)

        topline = "the quick brown fox"

        # view = self.view
        point = self.view.text_point(1, 0)  # second line point
        self.view.insert(edit, point, filenameify(topline) )

        # cursor = view.sel()[0].a
        # line_start = cur_line.a

        # line1 = sublime.Region(0,0)
        # line2 = sublime.Region(1,0)
        # allstuff = sublime.Region(0, self.view.size())
        # myline1 = self.view.line(line1)
        # myline2 = self.view.line(line2)
        # tp = self.view.text_point(0, 0)
        # myline1 = self.view.rowcol( tp )
        # mylineo = text_point(1, 1, True)

        # myline2 = self.view.rowcol(2, 0)

        # self.view.insert(edit, myline2, today.strftime("%Y%m%d @ %H:%M"))
        # self.view.insert(edit, 0, today.strftime("%Y%m%d @ %H:%M\n"))

        # p = re.compile("\s*#?\s*(.*)")

        # juicy = myline
        # self.view.replace(edit, myline, 'Cheese and crackers!')
        # self.view.insert(edit, 0, "Hello, World!")
