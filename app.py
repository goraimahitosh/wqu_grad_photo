from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

WALL_IMAGE_PATH = "./static/wall.png"
LOGO_IMAGE_PATH = "./static/logo.png"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        if "file" not in request.files:
            return "No file uploaded", 400

        file = request.files["file"]


        if file.filename == "":
            return "No file selected", 400

        if file:

            human_image = file.read()
            human_no_bg = remove(human_image)


            human_no_bg_image = Image.open(io.BytesIO(human_no_bg)).convert("RGBA")


            wall_image = Image.open(WALL_IMAGE_PATH).convert("RGBA")


            human_no_bg_image = human_no_bg_image.resize(wall_image.size, Image.Resampling.LANCZOS)


            final_image = Image.alpha_composite(wall_image, human_no_bg_image)


            logo_image = Image.open(LOGO_IMAGE_PATH).convert("RGBA")


            final_image = Image.alpha_composite(final_image, logo_image)


            output_buffer = io.BytesIO()
            final_image.save(output_buffer, format="PNG")
            output_buffer.seek(0)


            return send_file(
                output_buffer,
                mimetype="image/png",
                as_attachment=True,
                download_name="final_image.png",
            )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)