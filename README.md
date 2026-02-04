# Note to Markdown

A Sublime Text plugin to easily save a [markdown-formatted][md] text file as a tagged markdown file.

## Version

v0.1.0

## Author

* BryanH <bryan@master-developer.com>

## Installation

### Sublime Package Control
* Open the command palette, either in the tools menu or by using the Command + Shift + P (Alt + Shift + P for Windows) shortcut
* Select _Package Control: Install Package_
* Look for Note2Markdown and install it

## Manually
* Create a `note_to_markdown` directory in the Sublime Packages directory
    * Locate this directory by using the _Settings... -> Browse Packages..._ menu item
* Copy all the files and directories into this directory
* You may need to restart Sublime Text

## Usage
Click on the _Tools -> Note to Markdown_ menu item

A popup box will have the formatted filename pre-filled. Choose the directory where you want to save the file and click _Save_

## Configuration

| Setting            | Default         |
| ------------------ | --------------- |
| extension          | "md"            |
| prefix-format      | "%Y%m%d_%H%M-"  |
| substitution-space | "_" (underline) |
| substitution-punct | "" (nothing)    |
| debug              | false           |

### extension

The extension used for the new filename. Sublime Text recognizes _md_ as a markdown file automatically and will format the file properly.

### prefix-format

The prefix used for the new filename. Can be any text or number (or nothing), and any code that begins with a percent (%) will be automatically replaced with the respective date/time variable. The codes in the default prefix are listed below. The complete list is available on the [Python strftime() documentation page][strf]

|  code  | value                       |
| :----: | --------------------------- |
|  `%Y`  | 4-digit year                |
|  `%m`  | 2-digit month               |
|  `%d`  | 2-digit day                 |
|  `%H`  | 2-digit hour, 24-hour clock |
|  `%M`  | 2-digit minute              |


### Notes
* The first line of the file must be the h1 markdown header (`#`)

* The file type must be "Plain Text" (shown at the bottom of the window)

* This plugin does not validate or format the document. There are [many other plugins][plug] to do that.

## Changelog

**v0.1.0** - Alpha build; debug option
**v0.0.0** - Planck time ⏳ after the Big Bang 💥 - written up from nothing

[md]:https://daringfireball.net/projects/markdown/
[strf]:https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
[plug]:https://packagecontrol.io/search/markdown