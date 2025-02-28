In forms.py:

The DownloadForm class provides a simple form with just a download button


In views.py:

Static file download using send_from_directory() - serves an existing file from the server's filesystem
Dynamic file download using send_file() with in-memory file generation:

Creates a file in memory using StringIO
Uses CSV writer to populate it with data from the application
Converts to bytes and sends directly to the user without saving to disk





These two download methods demonstrate different approaches to providing files to users:

Static: Pre-existing files on the server
Dynamic: Files generated on-the-fly based on current application data
