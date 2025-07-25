from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def rule_based_discount(category, brand, season, price, stock, rating):
    discount = 10  # base discount
    # Category adjustment
    if category == 'Jacket':
        discount += 10
    elif category == 'T-Shirt':
        discount += 5
    # Brand adjustment
    if brand == 'Adidas':
        discount -= 2
    elif brand == 'Nike':
        discount -= 1
    # Season adjustment
    if season == 'Festive':
        discount += 8
    elif season == 'Winter':
        discount += 3
    # Price adjustment
    if price > 50000:
        discount += 7
    elif price > 20000:
        discount += 3
    # Stock adjustment
    if stock > 300:
        discount += 4
    # Rating adjustment
    if rating > 4.5:
        discount -= 3
    elif rating < 2:
        discount += 2
    # Clamp discount between 5 and 80
    return max(5, min(discount, 80))

@app.route('/predict', methods=['POST'])
def predict_discount():
    data = request.get_json()
    try:
        category = data['Category']
        brand = data['Brand']
        season = data['Season']
        price = float(data['Price'])
        stock = int(data['Stock'])
        rating = float(data['Rating'])
        pred = rule_based_discount(category, brand, season, price, stock, rating)
        return jsonify({'predicted_discount': f"{pred:.2f}%"})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calculate', methods=['POST'])
def calculate_discounted_price():
    data = request.get_json()
    try:
        price = float(data['price'])
        discount_percent = float(data['discount_percent'])
        discounted_price = price * (1 - discount_percent / 100)
        return jsonify({
            'original_price': price,
            'discount_percent': f"{discount_percent:.2f}%",
            'discounted_price': round(discounted_price, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001) 