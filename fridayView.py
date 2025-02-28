# Import io for in-memory file operations (used for dynamic file generation)
import io

# Import Flask functions including send_file for dynamic downloads
from flask import render_template, redirect, url_for, request, flash, send_from_directory, send_file
# Import secure_filename to sanitize uploaded filenames
from werkzeug.utils import secure_filename

# Import the Flask app instance
from app import app
# Import form classes including the new DownloadForm
from app.forms import RegistrationForm, CSVUploadForm, ItemForm, DownloadForm
# Import UUID for generating unique filenames
from uuid import uuid4
# Import OS for file operations
import os
# Import CSV for handling CSV files
import csv

@app.route('/')
def home():
    # Home page route
    return render_template('home.html', title='Home Page')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Registration page with form processing
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'You have registered correctly {form.username.data}', 'success')
        return redirect(url_for('reg_complete', username=form.username.data, email=form.email.data, level=form.level.data))
    return render_template('register.html', form=form)


@app.route('/register2', methods=['GET', 'POST'])
def register2():
    # Alternative registration page
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'You have registered correctly {form.username.data}', 'success')
        return redirect(url_for('reg_complete', username=form.username.data, email=form.email.data, level=form.level.data))
    return render_template('register2.html', form=form)


@app.route('/register3', methods=['GET', 'POST'])
def register3():
    # Another alternative registration page
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'You have registered correctly {form.username.data}', 'success')
        return redirect(url_for('reg_complete', username=form.username.data, email=form.email.data, level=form.level.data))
    return render_template('register3.html', form=form)

@app.route('/register_complete')
def reg_complete():
    # Registration completion page
    username = request.args.get('username')
    email = request.args.get('email')
    level = request.args.get('level')
    return render_template('reg_complete.html', username=username, email=email, level=level)

# In-memory data store for fruit entries
fruit = [['Banana', 'Yellow'], ['Apple', 'Red']]

@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    # Form for uploading and processing CSV files
    form = CSVUploadForm()
    if form.validate_on_submit():
        # Generate unique filename
        unique_str = str(uuid4())
        filename = secure_filename(f'{unique_str}-{form.file.data.filename}')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Save uploaded file
        form.file.data.save(filepath)
        try:
            # Open and process CSV file
            with open(filepath, newline='') as csvFile:
                reader = csv.reader(csvFile)
                # Validate header row
                header_row = next(reader)
                if header_row != ['FruitName', 'Colour']:
                    form.file.errors.append('Your header row is wrong')
                    raise ValueError('The header row is wrong')
                
                error_count = 0
                temp_fruit = []
                # Process each row with validation
                for index, row in enumerate(reader, start=2):
                    if error_count >= 3:
                        raise ValueError('Checking stopped: Too many errors in file')
                    if len(row) != 2:
                        form.file.errors.append(f'Row {index} has the wrong number of fields')
                        error_count += 1
                        continue
                    if row[1] not in ['Red', 'Orange', 'Yellow']:
                        form.file.errors.append(f'Row {index} has an invalid colour')
                        error_count += 1
                        continue
                    temp_fruit.append(row)
                
                # Only add to fruit list if no errors
                if error_count == 0:
                    fruit.extend(temp_fruit)
                else:
                    raise ValueError('Errors found: file not uploaded')
            
            return render_template('upload_complete.html', fruit=fruit)
        except ValueError as e:
            # Handle validation errors
            flash(e, 'danger')
            print(f"There was an error: {e}")
        finally:
            # Clean up uploaded file
            silent_remove(filepath)
    
    return render_template('upload_csv.html', form=form)

# Helper function to silently remove files
def silent_remove(filepath):
    try:
        os.remove(filepath)
    except:
        pass

@app.route('/show_list')
def show_list():
    # Display the fruit list
    form = ItemForm()
    return render_template('list.html', fruit=fruit, form=form)

@app.route('/delete', methods=['POST'])
def delete():
    # Delete an item from the fruit list
    form = ItemForm()
    if form.validate_on_submit():
        fruit_choice = int(form.fruit_choice.data)
        fruit.pop(fruit_choice)
        flash(f'Item {fruit_choice} deleted', 'warning')
    return redirect(url_for('show_list'))

# STATIC FILE DOWNLOAD
@app.route('/download')
def download():
    # Route to download a static CSV file that already exists on the server
    form = DownloadForm()
    if form.validate_on_submit:
        # send_from_directory serves an existing file from the server's filesystem
        # The file is located in the 'static' folder and named 'MyFile.csv'
        # as_attachment=True forces browser to download rather than display
        # download_name sets the filename shown to the user
        # mimetype specifies the file type
        return send_from_directory('static', 'MyFile.csv', as_attachment=True, download_name='MyFile.csv', mimetype='text/csv')
    return render_template('download.html', form=form)

# DYNAMIC FILE DOWNLOAD
@app.route('/download-dynamic')
def download_dynamic():
    # Route to generate and download a CSV file dynamically from the fruit data
    form = DownloadForm()
    if form.validate_on_submit:
        # Create an in-memory string buffer
        with io.StringIO() as mem:
            # Create a CSV writer that writes to the in-memory buffer
            writer = csv.writer(mem)
            # Write header row
            writer.writerow(['FruitName', 'Colour'])
            # Write each fruit item as a row
            for item in fruit:
                writer.writerow(item)
            # Reset buffer position to beginning
            mem.seek(0)
            # Convert string buffer to bytes buffer
            # send_file sends the in-memory generated file to the client
            # The contents are taken directly from memory, not from disk
            return send_file(io.BytesIO(mem.getvalue().encode(encoding='utf-8')), 
                            as_attachment=True, 
                            download_name='MyFruit.csv', 
                            mimetype='text/csv')
    return render_template('download.html', form=form)
