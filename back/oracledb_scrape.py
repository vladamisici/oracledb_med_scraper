from flask import Flask, request, jsonify
import oracledb
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables CORS for dev environment

# Oracle DB connection
conn = oracledb.connect(user="system", password="password", dsn="MISICI-V.datagroup.local:1521/xe")
cursor = conn.cursor()

@app.route('/api/search', methods=['POST'])
def search_and_insert():
    data = request.get_json()
    keywords = data.get('keywords', '')
    rows = data.get('rows', 10)

    if not keywords.strip():
        return jsonify({"error": "Keywords not provided"}), 400

    # Crossref API call
    url = f"https://api.crossref.org/works?query={keywords}&rows={rows}"
    response = requests.get(url)
    cr_data = response.json()

    inserted_count = 0

    for item in cr_data['message']['items']:
        title = item['title'][0] if 'title' in item and len(item['title']) > 0 else 'Untitled'
        year = None
        if 'issued' in item and 'date-parts' in item['issued'] and len(item['issued']['date-parts'])>0 and len(item['issued']['date-parts'][0])>0:
            year = item['issued']['date-parts'][0][0]
        doi = item.get('DOI', None)
        p_type = 'Journal Article' if 'journal' in item.get('type', '').lower() else 'Conference Paper'
        venue_name = item['container-title'][0] if 'container-title' in item and len(item['container-title']) > 0 else 'Unknown Venue'

        # Check if DOI already exists
        if doi:
            cursor.execute("SELECT Paper_ID FROM PAPER WHERE DOI = :doi", doi=doi)
            existing = cursor.fetchone()
            if existing is not None:
                # If paper already exists, skip insertion
                continue

        # Insert VENUE
        var_vid = cursor.var(oracledb.NUMBER)
        cursor.execute("""
            INSERT INTO VENUE (Venue_ID, Venue_Name, Venue_Type) 
            VALUES (seq_venue_id.NEXTVAL, :vname, 'Journal')
            RETURNING Venue_ID INTO :vid
        """, vname=venue_name, vid=var_vid)
        venue_id = var_vid.getvalue()[0]

        # Insert PAPER
        var_pid = cursor.var(oracledb.NUMBER)
        cursor.execute("""
            INSERT INTO PAPER (Paper_ID, Title, Year, DOI, Venue_ID, Type_Publication)
            VALUES (seq_paper_id.NEXTVAL, :title, :year, :doi, :vid, :ptype)
            RETURNING Paper_ID INTO :pid
        """, title=title, year=year, doi=doi, vid=venue_id, ptype=p_type, pid=var_pid)
        paper_id = var_pid.getvalue()[0]

        # Authors
        authors = item.get('author', [])
        if not authors:
            authors = [{'given':'Unknown','family':'Author'}]

        for auth in authors:
            name = (auth.get('given', '') + ' ' + auth.get('family', '')).strip()
            if not name:
                name = 'Unknown Author'
            
            var_aid = cursor.var(oracledb.NUMBER)
            cursor.execute("""
                INSERT INTO AUTHOR (Author_ID, Name) 
                VALUES (seq_author_id.NEXTVAL, :name)
                RETURNING Author_ID INTO :aid
            """, name=name, aid=var_aid)
            author_id = var_aid.getvalue()[0]

            cursor.execute("INSERT INTO PAPERS_AUTHORS (Paper_ID, Author_ID, Order_of_Authorship) VALUES (:pid, :aid, 1)",
                           pid=paper_id, aid=author_id)

        inserted_count += 1

    conn.commit()
    return jsonify({"message": f"{inserted_count} articles inserted."}), 200

@app.route('/api/papers', methods=['GET'])
def get_papers():
    cursor.execute("""
        SELECT p.Paper_ID, p.Title, p.Year, p.DOI, v.Venue_Name 
        FROM PAPER p
        JOIN VENUE v ON p.Venue_ID = v.Venue_ID
        FETCH FIRST 50 ROWS ONLY
    """)
    rows = cursor.fetchall()
    result = []
    for r in rows:
        result.append({
            "Paper_ID": r[0],
            "Title": r[1],
            "Year": r[2],
            "DOI": r[3],
            "Venue_Name": r[4]
        })
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
