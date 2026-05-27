# WriteIt CLI

A distraction-free CLI text editor for writers with minimal features.

## About this Project

There exist many tools out there that are made with the objective of giving writers every tool imaginable to help them in their writing process. This, however, can sometimes be overwhelming to people who are looking to get started. Am I using the correct tool? Does this have all the features that I need? These types of questions can very easily lead someone down a path of analysis-paralysis, and take them away from what they should actually be doing: just writing it. This project aims to provide the user with a very minimal interface with none of the fancy-dos.

At the very core, this tool is just vim-like text editor with a couple of extra features. It is my honest belief that writers don't need anything more than that. A tool that helps them write, the option to look at their word count and a timer, and a manager to organize their many notes.

### Built With

- Python
- Textual

## Getting Started

In case you want to use this tool, feel free to follow the instructions below.

### Prerequisites

- Python 3.9 or higher.
- A terminal that supports colors + other modern features.

### Installation

- Download the repository.
- Sync the environment with `uv sync`
- Run the tool with `uv run -m src.main` or with the provided `main.sh` file.

## Usage

Once you're in the program, you'll find yourself staring at one of the Editor screens. These are the quick commands you need to know:

### Normal Mode

- `i`: Enter Insert mode.
- `[h | j | k | l]`: vim-like movement of the cursor.
- `a`: Create a new Editor screen.
- `ctrl + [h | j | k | l]`: Move between Editors.
- `alt + [h | j | k | l]`: Switch position of Editors.
- `:`: Enter command mode.
- `d`: Toggle directory folder ($HOME/.writeit/content)
- `s`: Switch between directory folder (if open) and Editor.

### Insert Mode

- `escape`: Go back to Normal mode.

### Command Mode

For the command mode, you'll input the command you desire and then press Enter to submit it:

- `q`: Quit the current Editor. If there are no open Editors, this closes the application.
- `qa`: Quits all.
- `w`: Writes the current buffer to a file. If the buffer has no filename associated, it creates the file from the current date + time in the `$HOME/.writeit/content/` directory. After that, it will associate that filename to that buffer.
- `w filename`: Writes the current buffer to the specified filename, and associates that buffer to the filename.

### Directory

- `enter`: Either opens the given folder or opens the file as a buffer (with its filename associated).
- `a`: Create a new file (confirm window asks for filename).
- `r`: Deletes file or folder (asks for confirmation beforehand).

## Roadmap

- [x] Simple note editor.
- [x] Multi-note management.
- [x] File directory + confirm window.
- [x] Complete README.md once base is done (License, etc.)
- [ ] Add more useful commands (zoom, replace content in buffer, Markdown preview...)
- [ ] Utilities for the directory view (create folders, easy organization, tags...)
- [ ] Make header and command global instead of being tied to the Editor, add more useful commands.
- [ ] Customizeable Layouts.
- [ ] Custom Widget support.
- [ ] Different types of editors.

## Contact

ZILNULL - @zilnull.bsky.social - <zilnullart@gmail.com>

## Acknowledgement

Thank you to the following resources for helping make this project a reality.

- <https://www.boot.dev/> for helping me get off my ass and make a project.
- <https://github.com/othneildrew/Best-README-Template> for the minimal README template.
- <https://github.com/textualize/textual> for the awesome Python TUI toolset.

## License

This software is distributed under the GNU GPLv3 license. Look at [LICENSE](./LICENSE) for more information.
