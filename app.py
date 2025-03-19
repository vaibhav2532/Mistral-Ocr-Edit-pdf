import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import markdown

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        if "pdf_file" not in request.files or "md_file" not in request.files:
            return "Both PDF and Markdown files are required", 400

        pdf_file = request.files["pdf_file"]
        md_file = request.files["md_file"]

        if pdf_file.filename == "" or md_file.filename == "":
            return "No selected file", 400

        # Save PDF file
        pdf_filename = secure_filename(pdf_file.filename)
        pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)
        pdf_file.save(pdf_path)

        # Save Markdown file
        md_filename = secure_filename(md_file.filename)
        md_path = os.path.join(app.config["UPLOAD_FOLDER"], md_filename)
        md_file.save(md_path)

        return redirect(url_for("preview_files", pdf_filename=pdf_filename, md_filename=md_filename))

    return render_template("upload.html")


@app.route("/preview/<pdf_filename>/<md_filename>")
def preview_files(pdf_filename, md_filename):
    md_path = os.path.join(app.config["UPLOAD_FOLDER"], md_filename)

    with open(md_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()
        html_content = markdown.markdown(md_content)

    return render_template("preview.html", pdf_filename=pdf_filename, md_filename=md_filename, html_content=html_content)


@app.route("/edit/<md_filename>", methods=["GET", "POST"])
def edit_markdown(md_filename):
    md_path = os.path.join(app.config["UPLOAD_FOLDER"], md_filename)

    if request.method == "POST":
        new_content = request.form["markdown_content"]
        with open(md_path, "w", encoding="utf-8") as md_file:
            md_file.write(new_content)
        return redirect(url_for("preview_files", pdf_filename=request.args.get("pdf_filename"), md_filename=md_filename))

    with open(md_path, "r", encoding="utf-8") as md_file:
        content = md_file.read()

    return render_template("edit.html", md_filename=md_filename, content=content)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
