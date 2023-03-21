# GPTextEdit - A ChatGPT-enabled Text Editor

I wanted a text editor with ChatGPT built in because why tf not! GPTextEdit is a OpenAI API enabled text editor with Python syntax highlighting. The text editor is in its early alpha and is being actively developed on. Current functionality is pretty barebones at the moment with just the basic keyboard shortcuts, which are copy, cut, paste, and select all. 

The OpenAI feature is set to use ChatGPT3.5-turbo. You'll need to add your api key to the sample_conf.txt; replace the placeholder and be sure to remove the white space before and after the key, and rename the file to conf.txt. The system promp is pretty good overall and  the explanations the AI produces are pretty excellent.

## Project Status & Plans
...on the way!

## Installation
Installation should be pretty easy, but let me know if you run into issues! GPTextEditor is built with Python 3.10.

### Requirements:

| package | version |
|---------|---------|
| Python | v3.10 |
| tkinter | v8.6 |
| os | Python 3.10 |
| openai | latest |

**Note:** tkinter comes packaged with the 'full' version of Python, which is not in the OS default Python installs (Mac & Lin). You'll have to install it.

## Usage

Once you have GPTextEditor installed, the interface should look familiar if you've used a TE before.

The **top bar** menus have the following functions:
- **File** menu
  - New: Create a new text file
  - Open: Open a Python or text file
  - Save: saves the current file
  - Save as: save the file under a new name
- **Edit** menu
  - Copy: copies the selected text or whole doc to the clipboard
  - Cut: copies the text to the clipboard and removes the source
  - Paste: appends the clipboard contents to the document at the cursor or end of file
  - Select All: select everything in the document
- **AI** menu
  - Chat Completion: Sends the text in the document to the OpenAI API ChatGPT3.5-turbo completion endpoint. The response is appended to the end of the text editor document
