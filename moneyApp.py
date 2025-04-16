from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

CSV_FILE = 'records.csv'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form.get('date')
        item = request.form.get('item')
        type_ = request.form.get('type')
        amount = request.form.get('amount')

        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([date, item, type_, amount])

        # フォーム送信後にページをリダイレクトしてリストを更新
        return redirect('/')

    records = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            records = list(reader)
    except FileNotFoundError:
        pass

    return render_template('index.html', records=records)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    records = []

    # CSVファイルを検索
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                # 各行のデータに検索キーワードが含まれるか確認
                if query in row[0] or query in row[1] or query in row[2] or query in row[3]:
                    records.append(row)

    except FileNotFoundError:
        pass

    return render_template('index.html', records=records, query=query)

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # 🔹 ポート番号を明示的に指定！