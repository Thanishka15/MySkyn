# MySkyn

MySkyn is an AI-powered skincare platform that helps users understand their skin better and make informed skincare decisions. By combining AI-driven skin analysis, personalized skincare recommendations, and ingredient scanning, MySkyn acts as a smart skincare assistant that is accessible anytime.

## Features

### AI Skin Analysis
- Upload a photo of your face for AI-based skin assessment.
- Detect common skin concerns such as:
  - Acne
  - Pimples
  - Dark spots
  - Pigmentation
  - Redness
  - Uneven skin tone
- Receive an overall skin health evaluation.

### Personalized Skincare Routine
- Generate customized skincare routines based on detected skin concerns.
- Get recommendations for:
  - Morning routines
  - Night routines
  - Cleansers
  - Moisturizers
  - Sunscreens
  - Treatment products
- Tailored suggestions based on individual skin needs.

### Ingredient Scanner
- Analyze skincare product ingredient lists.
- Identify beneficial ingredients and their skincare benefits.
- Highlight potentially irritating or harmful ingredients.
- Explain ingredient functions in simple, easy-to-understand language.

### Smart Product Insights
- Understand what each ingredient does.
- Learn whether a product is suitable for your skin concerns.
- Make more informed purchasing decisions.

### User-Friendly Experience
- Clean and intuitive interface.
- Simple image upload workflow.
- Fast AI-powered results.
- Beginner-friendly skincare guidance.

## Tech Stack

### Backend
- Python
- Flask

### Frontend
- HTML
- CSS
- JavaScript

### AI & Image Processing
- AI-based skin analysis models
- Ingredient analysis engine

### Project Structure

```
MySkyn/
│
├── templates/
│   ├── index.html
│   ├── ingredients.html
│   ├── ingredient_result.html
│   └── scan_result.html
│
├── uploads/
│
├── app.py
├── upload.html
└── .gitignore
```

## How It Works

### Skin Analysis
1. Upload a facial image.
2. AI analyzes visible skin conditions.
3. Skin concerns are identified.
4. Personalized recommendations are generated.

### Ingredient Analysis
1. Enter or upload a skincare product's ingredient list.
2. MySkyn scans and evaluates each ingredient.
3. The platform explains ingredient benefits and potential concerns.
4. Users receive a simplified ingredient breakdown.

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/myskyn.git
cd myskyn
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Environment

#### macOS/Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

The application will start locally and can be accessed through your browser.

## Future Enhancements

- Skin progress tracking over time
- Product recommendation system
- AI chatbot for skincare queries
- User accounts and saved reports
- Routine reminders and notifications
- Mobile application support
- Advanced skin condition detection

## Use Cases

- Understanding personal skin concerns
- Building an effective skincare routine
- Evaluating skincare products before purchase
- Learning about skincare ingredients
- Making evidence-based skincare decisions

## Disclaimer

MySkyn is intended for educational and informational purposes only. The platform does not provide medical diagnoses and should not replace professional dermatological advice.

## License

This project is available for educational and personal use. You may modify and extend it according to your needs.
