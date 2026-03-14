import os
import json
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

# Azure Vision
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# Azure OpenAI
from openai import AzureOpenAI

# -------------------------------------------------
# App setup
# -------------------------------------------------
load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-secret-key"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------------------------------
# Azure Clients
# -------------------------------------------------
vision_client = ComputerVisionClient(
    os.environ["VISION_ENDPOINT"],
    CognitiveServicesCredentials(os.environ["VISION_KEY"])
)

openai_client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"]
)

# -------------------------------------------------
# PROMPTS
# -------------------------------------------------

SYSTEM_PROMPT = """
You are a professional dermatology and skincare analysis assistant.

Your responsibilities:
- Analyze provided visual skin observations
- Infer the MOST LIKELY skin type using dermatological reasoning
- Identify visible or probable skin concerns, even if mild
- NEVER respond with "unknown" unless the face is not visible
- Do not provide medical diagnoses
- Confidence reflects image clarity, not hesitation

Allowed skin types:
oily, dry, combination, normal

Allowed concerns (multi-label):
acne, pigmentation, redness, texture, dark_circles, dehydration, dullness

Rules:
- Choose the most probable skin type and reduce confidence if uncertain
- Mild concerns should still be included
- Base conclusions strictly on visual cues
- Output VALID JSON ONLY
- No markdown, no explanations outside JSON

This is cosmetic skincare guidance, not medical advice.
"""

USER_PROMPT_TEMPLATE = """
Visual skin observations:
{vision_summary}

Analyze the skin and return the result in the following JSON format:

{{
  "skin_type": "",
  "confidence": "low | medium | high",
  "skin_type_reason": "",
  "concerns": [
    {{
      "name": "",
      "severity": "mild | moderate",
      "reason": ""
    }}
  ],
  "am_routine": [
    {{
      "step": "",
      "why": ""
    }}
  ],
  "pm_routine": [
    {{
      "step": "",
      "why": ""
    }}
  ]
}}
"""

# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------------------------------------
# FACE SCAN
# -------------------------------------------------
@app.route("/scan-face", methods=["POST"])
def scan_face():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    # 1️⃣ Azure Vision (basic observations)
    with open(image_path, "rb") as img:
        vision_result = vision_client.analyze_image_in_stream(
            img,
            visual_features=["Description", "Color", "Faces"]
        )

    vision_summary = {
        "faces_detected": len(vision_result.faces) if vision_result.faces else 0,
        "image_description": (
            vision_result.description.captions[0].text
            if vision_result.description.captions else "No description"
        ),
        "dominant_colors": vision_result.color.dominant_colors,
        "is_black_white": vision_result.color.is_bw_img
    }

    # 2️⃣ OpenAI Skin Analysis
    user_prompt = USER_PROMPT_TEMPLATE.format(
        vision_summary=json.dumps(vision_summary, indent=2)
    )

    response = openai_client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )

    analysis = json.loads(response.choices[0].message.content)

    # 3️⃣ Store in session
    session["skin_type"] = analysis["skin_type"]
    session["concerns"] = analysis["concerns"]

    return render_template(
        "scan_result.html",
        skin_type=analysis["skin_type"],
        skin_type_reason=analysis["skin_type_reason"],
        concerns=analysis["concerns"],
        confidence=analysis["confidence"],
        am_routine=analysis["am_routine"],
        pm_routine=analysis["pm_routine"]
    )

# -------------------------------------------------
# INGREDIENT INPUT PAGE
# -------------------------------------------------
@app.route("/ingredients", methods=["GET"])
def ingredients_page():
    return render_template("ingredients.html")

# -------------------------------------------------
# INGREDIENT ANALYSIS
# -------------------------------------------------
@app.route("/analyze-ingredients", methods=["POST"])
def analyze_ingredients():

    ingredients = request.form.get("ingredients")
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    skin_type = session.get("skin_type", "normal")
    concerns = session.get("concerns", [])

    prompt = f"""
User skin type: {skin_type}
User concerns: {concerns}

Analyze the following cosmetic ingredients.

Return JSON ONLY:
{{
  "safe": [],
  "avoid": [],
  "verdict": "Suitable | Use with caution | Avoid"
}}

Ingredients:
{ingredients}
"""

    response = openai_client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "You analyze skincare ingredient safety."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    result = json.loads(response.choices[0].message.content)

    return render_template(
        "ingredient_result.html",
        result=result
    )

# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
