import requests
import oracledb

# Configurare conexiune Oracle
conn = oracledb.connect(user="system", password="password", dsn="MISICI-V.datagroup.local:1521/xe")
cursor = conn.cursor()

# Căutăm articole care conțin "machine learning" în Crossref
url = "https://api.crossref.org/works?query=machine+learning&rows=10"

response = requests.get(url)
data = response.json()

for item in data['message']['items']:
    title = item['title'][0] if 'title' in item and len(item['title']) > 0 else 'Untitled'
    year = None
    if 'issued' in item and 'date-parts' in item['issued'] and len(item['issued']['date-parts'])>0 and len(item['issued']['date-parts'][0])>0:
        year = item['issued']['date-parts'][0][0]
    doi = item.get('DOI', None)
    # Simplificăm tipul publicației pe baza câmpului 'type'
    p_type = 'Journal Article' if 'journal' in item.get('type', '').lower() else 'Conference Paper'
    
    # Stabilim numele venue-ului (dacă container-title lipsește, punem 'Unknown Venue')
    venue_name = item['container-title'][0] if 'container-title' in item and len(item['container-title']) > 0 else 'Unknown Venue'
    
    # Creăm variabilele de tip NUMBER pentru RETURNING
    var_vid = cursor.var(oracledb.NUMBER)
    cursor.execute("""
        INSERT INTO VENUE (Venue_ID, Venue_Name, Venue_Type) 
        VALUES (seq_venue_id.NEXTVAL, :vname, 'Journal')
        RETURNING Venue_ID INTO :vid
    """, vname=venue_name, vid=var_vid)
    venue_id = var_vid.getvalue()[0]  # getvalue() returnează un array, luăm primul element

    var_pid = cursor.var(oracledb.NUMBER)
    cursor.execute("""
        INSERT INTO PAPER (Paper_ID, Title, Year, DOI, Venue_ID, Type_Publication)
        VALUES (seq_paper_id.NEXTVAL, :title, :year, :doi, :vid, :ptype)
        RETURNING Paper_ID INTO :pid
    """, title=title, year=year, doi=doi, vid=venue_id, ptype=p_type, pid=var_pid)
    paper_id = var_pid.getvalue()[0]

    # Gestionăm autorii
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

        # Legăm autor <-> paper
        cursor.execute("INSERT INTO PAPERS_AUTHORS (Paper_ID, Author_ID, Order_of_Authorship) VALUES (:pid, :aid, 1)",
                       pid=paper_id, aid=author_id)

conn.commit()

cursor.close()
conn.close()
