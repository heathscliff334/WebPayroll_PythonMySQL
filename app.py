from flask import Flask, render_template, \
  request, redirect, url_for
import mysql.connector
import hashlib

app = Flask(__name__)
app.config['DB_USER'] = 'root'
app.config['DB_PASSWORD'] = ''
app.config['DB_NAME'] = 'flaskdb_buku'
app.config['DB_HOST'] = 'localhost'

conn = cursor = None

def openDb():
   global conn, cursor
   conn = mysql.connector.connect(
      user=app.config['DB_USER'],
      password=app.config['DB_PASSWORD'],
      database=app.config['DB_NAME'],
      host=app.config['DB_HOST'],
   )
   cursor = conn.cursor()	

def closeDb():
   global conn, cursor
   cursor.close()
   conn.close()

@app.route('/')
def index():   
  return render_template('login.html')

@app.route('/home')
def home():
   uriTest = 'Home'
   return render_template('home.html', uriTest=uriTest)

@app.route('/login', methods=['GET','POST'])
def login():
   openDb()
   if request.method == 'POST':
      usr = request.form['username']
      passw = request.form['password']
      cursor.execute("SELECT * FROM users WHERE username ='%s'" %usr)
      container = []
      for user_id,username,password,nama_lengkap,role in cursor.fetchall():
         container.append((user_id,username,password,nama_lengkap,role))
      closeDb()
      if usr == username and passw == password:
         print 'benar'
         return redirect(url_for('karyawan'))
      else :
         print 'salah'
      return render_template('login.html', container=container)

# USERS
@app.route('/users')
def user():
   openDb()
   uriTest = 'User'
   cursor.execute('SELECT * FROM users')
   container = []
   for user_id, username, password, nama_lengkap, role in cursor.fetchall():
      container.append((user_id, username, password, nama_lengkap, role, uriTest))
   closeDb()
   return render_template('user/list_user.html', container=container, uriTest=uriTest)  

@app.route('/tambah_user', methods=['GET','POST'])
def tambah_user():
   uriTest = 'Register User'
   if request.method == 'POST':
      user_id = '';
      username = request.form['username']
      password = request.form['password']
      nama_lengkap = request.form['nama_lengkap']
      role = request.form['role']
      data = (user_id, username, password, nama_lengkap, role)
      openDb()
      cursor.execute('''
        INSERT INTO users VALUES('%s','%s','%s','%s','%s')''' % data)
      conn.commit()
      closeDb()
      return redirect(url_for('user'))
   else:
      return render_template('user/tambah_user.html', uriTest=uriTest)

@app.route('/ubah_user/<id>', methods=['GET','POST'])
def ubah_user(id):
   openDb()
   uriTest = 'Ubah User'
   cursor.execute("SELECT * FROM users WHERE user_id='%s'" % id)
   data = cursor.fetchone()
   if request.method == 'POST':
      password = request.form['password']
      nama_lengkap = request.form['nama_lengkap']
      role = request.form['role']
      cursor.execute('''
         UPDATE users SET password='%s', nama_lengkap='%s' WHERE user_id='%s'
      ''' % (password, nama_lengkap, id))
      conn.commit()
      closeDb()
      return redirect(url_for('user'))
   else:
      closeDb()
      return render_template('user/ubah_user.html', data=data, uriTest=uriTest)

@app.route('/hapus_user/<id>', methods=['GET','POST'])
def hapus_user(id):
   openDb()
   cursor.execute("DELETE FROM users WHERE user_id='%s'" % id)
   conn.commit()
   closeDb()
   return redirect(url_for('user'))

# KARYAWAN
@app.route('/karyawan')
def karyawan():
   openDb()
   uriTest = 'Karyawan'
   cursor.execute('SELECT * FROM karyawan')
   container = []
   for nik,nama,jabatan,email, telp in cursor.fetchall():
      container.append((nik,nama,jabatan,email, telp,uriTest))
   closeDb()
   return render_template('karyawan/list_karyawan.html', container=container, uriTest=uriTest)  

@app.route('/ubah_karyawan/<nik>', methods=['GET','POST'])
def ubah_karyawan(nik):
   openDb()
   uriTest = 'Ubah Karyawan'
   cursor.execute("SELECT * FROM karyawan WHERE nik='%s'" % nik)
   data = cursor.fetchone()
   if request.method == 'POST':
      nik = request.form['nik']
      nama = request.form['nama']
      jabatan = request.form['jabatan']
      email = request.form['email']
      telp = request.form['telp']
      cursor.execute('''
         UPDATE karyawan SET nama='%s', jabatan='%s', email='%s', telp='%s' 
         WHERE nik='%s'
      ''' % (nama, jabatan, email, telp, nik))
      conn.commit()
      closeDb()
      return redirect(url_for('karyawan'))
   else:
      closeDb()
      return render_template('karyawan/ubah_karyawan.html', data=data, uriTest=uriTest)

@app.route('/tambah_karyawan', methods=['GET','POST'])
def tambah_karyawan():
   uriTest = 'Tambah Karyawan'
   if request.method == 'POST':
      nik = request.form['nik']
      nama = request.form['nama']
      jabatan = request.form['jabatan']
      email = request.form['email']
      telp = request.form['telp']
      data = (nik, nama, jabatan, email, telp)
      openDb()
      cursor.execute('''
        INSERT INTO karyawan VALUES('%s','%s','%s','%s', '%s')''' % data)
      conn.commit()
      closeDb()
      return redirect(url_for('karyawan'))
   else:
      return render_template('karyawan/tambah_karyawan.html', uriTest=uriTest)

@app.route('/hapus_karyawan/<nik>', methods=['GET','POST'])
def hapus_karyawan(nik):
   openDb()
   cursor.execute("DELETE FROM karyawan WHERE nik='%s'" % nik)
   conn.commit()
   closeDb()
   return redirect(url_for('karyawan'))

@app.route('/dashboard')
def dashboard():
   openDb()
   uriTest = 'dashboard'
   cursor.execute('SELECT * FROM buku')
   container = []
   for id,judul,penulis,penerbit in cursor.fetchall():
      container.append((id,judul,penulis,penerbit,uriTest))
   closeDb()
   return render_template('index.html', container=container, uriTest=uriTest)

# @app.route('/tambah', methods=['GET','POST'])
# def tambah():
#    if request.method == 'POST':
#       id = request.form['id']
#       judul = request.form['judul']
#       penulis = request.form['penulis']
#       penerbit = request.form['penerbit']
#       data = (id, judul, penulis, penerbit)
#       openDb()
#       cursor.execute('''
#         INSERT INTO buku VALUES('%s','%s','%s','%s')''' % data)
#       conn.commit()
#       closeDb()
#       return redirect(url_for('index'))
#    else:
#       return render_template('tambah_form.html')

# @app.route('/ubah/<id>', methods=['GET','POST'])
# def ubah(id):
#    openDb()
#    cursor.execute("SELECT * FROM buku WHERE id='%s'" % id)
#    data = cursor.fetchone()
#    if request.method == 'POST':
#       id = request.form['id']
#       judul = request.form['judul']
#       penulis = request.form['penulis']
#       penerbit = request.form['penerbit']
#       cursor.execute('''
#          UPDATE buku SET judul='%s', penulis='%s', penerbit='%s' 
#          WHERE id='%s'
#       ''' % (judul, penulis, penerbit, id))
#       conn.commit()
#       closeDb()
#       return redirect(url_for('index'))
#    else:
#       closeDb()
#       return render_template('ubah_form.html', data=data)

@app.route('/hapus/<id>', methods=['GET','POST'])
def hapus(id):
   openDb()
   cursor.execute("DELETE FROM buku WHERE id='%s'" % id)
   conn.commit()
   closeDb()
   return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(debug=True)
