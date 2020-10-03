# citation_extractor

This was my final university project during my MSc Software Development. This project was forked from an existing command line tool, and the main focus was porting it to a webapp using Flask; alongside adding some additional functionality.

This web app allows a user to upload .pdf, .docx, and .txt files (or files containing DBLP or bibtex formatted content) which follow the IEEE citation format. The system will then mine the extracted text for citations by using a regex, ouputting any results to a file which is served to the user for download. 

# Functionality

The software will, ideally, be hosted on a web server soon. 

A video showing off the functionality of the system, created for the purposes of university assessment, can be seen below in the mean time:
[![Demo video](https://img.youtube.com/vi/sNZslxp69iQ/0.jpg)](https://www.youtube.com/watch?v=sNZslxp69iQ "Project demo")


00:00 - System start up
01:15 - Showing of UI
02:12 - Show of system processing files and results file
04:52 - Showing file validation
07:23 - Routine system processes (session/file management)

# Future Development

Always welcome. Feel free to use the [issues page](https://github.com/0x4A42/citation_extractor/issues) or to fork it and have a go yourself!
