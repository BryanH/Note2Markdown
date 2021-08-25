import sublime
import sublime_plugin

from datetime import date
from slugify import slugify


def next_line(view, pt):
    return view.line(pt).b + 1


def prev_line(view, pt):
    return view.line(pt).a - 1


class Note2mdCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        sublime.log_result_regex(True)
        sublime.log_commands(True)
        today = date.today()
        today_s = today.strftime("%Y%m%d-")

        view = self.view
        cursor = view.sel()[0].a
        line_start = cur_line.a

        topline = slugify("the quick brown fox" + ".md")

        # line1 = sublime.Region(0,0)
        # line2 = sublime.Region(1,0)
        # allstuff = sublime.Region(0, self.view.size())
        # myline1 = self.view.line(line1)
        # myline2 = self.view.line(line2)
        # tp = self.view.text_point(0, 0)
        # myline1 = self.view.rowcol( tp )
        # mylineo = text_point(1, 1, True)

        myline2 = self.view.rowcol(2, 0)

        self.view.insert(edit, myline2, today.strftime("%Y%m%d @ %H:%M"))
        # self.view.insert(edit, 0, today.strftime("%Y%m%d @ %H:%M\n"))

        # p = re.compile("\s*#?\s*(.*)")

        # juicy = myline
        # self.view.replace(edit, myline, 'Cheese and crackers!')
        # self.view.insert(edit, 0, "Hello, World!")
