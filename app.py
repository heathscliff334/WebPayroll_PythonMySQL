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
      if request.form['username'] == '':
         print 'kosong'
         errMessage = 'Username / Password Kosong!!'
         return render_template('login.html', errMessage=errMessage)    
      usr = request.form['username']
      passw = request.form['password']

      cursor.execute("SELECT * FROM users WHERE username ='%s'" %usr)
      container = []
      for user_id,username,password,nama_lengkap,role in cursor.fetchall():
         container.append((user_id,username,password,nama_lengkap,role))
      closeDb()

      if usr == username and passw == password:
         print 'benar'
         return redirect(url_for('home'))
      else :
         print 'salah'
         errMessage = 'Username / Password Salah!!'
         return render_template('login.html', errMessage=errMessage)

# USERS
@app.route('/users')
def user():
   openDb()
   uriTest = 'Master User'
   cursor.execute('SELECT * FROM users')
   container = []
   for user_id, username, password, nama_lengkap, role in cursor.fetchall():
      container.append((user_id, username, password, nama_lengkap, role, uriTest))
   closeDb()
   return render_template('user/list_user.html', container=container, uriTest=uriTest)  

@app.route('/tambah_user', methods=['GET','POST'])
def tambah_user():
   uriTest = 'Master User'
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
   uriTest = 'Master User'
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
   uriTest = 'Master Karyawan'
   cursor.execute('SELECT karyawan.nik, karyawan.nama, jabatan.nama_jabatan, karyawan.email, karyawan.telp FROM karyawan JOIN jabatan ON karyawan.jabatan = jabatan.id')
   container = []
   for nik,nama,jabatan,email, telp in cursor.fetchall():
      container.append((nik,nama,jabatan,email, telp,uriTest))
   closeDb()
   return render_template('karyawan/list_karyawan.html', container=container, uriTest=uriTest)  

@app.route('/ubah_karyawan/<nik>', methods=['GET','POST'])
def ubah_karyawan(nik):
   openDb() 
   cursor.execute('SELECT * FROM jabatan')
   dataJabatan = []
   for id, nama_jabatan, tunjangan in cursor.fetchall():
      dataJabatan.append((id, nama_jabatan, tunjangan))    
   uriTest = 'Master Karyawan'
   cursor.execute("SELECT karyawan.nik, karyawan.nama, karyawan.jabatan, jabatan.nama_jabatan, karyawan.email, karyawan.telp FROM karyawan JOIN jabatan ON karyawan.jabatan = jabatan.id WHERE nik='%s'" % nik)
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
      return render_template('karyawan/ubah_karyawan.html', data=data, dataJabatan=dataJabatan, uriTest=uriTest)

@app.route('/tambah_karyawan', methods=['GET','POST'])
def tambah_karyawan():
   openDb()
   cursor.execute('SELECT * FROM jabatan')
   dataJabatan = []
   for id, nama_jabatan, tunjangan in cursor.fetchall():
      dataJabatan.append((id, nama_jabatan, tunjangan))   
   closeDb()
   uriTest = 'Master Karyawan'
   if request.method == 'POST':
      nik = request.form['nik']
      nama = request.form['nama']
      jabatan = request.form['jabatan']
      gaji_pokok = request.form['gapok']
      email = request.form['email']
      telp = request.form['telp']
      data = (nik, nama, jabatan, gaji_pokok, email, telp)
      openDb()
      cursor.execute('''
        INSERT INTO karyawan VALUES('%s','%s','%s','%s', '%s', '%s')''' % data)
      conn.commit()
      closeDb()
      return redirect(url_for('karyawan'))
   else:
      return render_template('karyawan/tambah_karyawan.html', dataJabatan=dataJabatan, uriTest=uriTest)

@app.route('/hapus_karyawan/<nik>', methods=['GET','POST'])
def hapus_karyawan(nik):
   openDb()
   cursor.execute("DELETE FROM karyawan WHERE nik='%s'" % nik)
   conn.commit()
   closeDb()
   return redirect(url_for('karyawan'))

# Payroll
@app.route('/payroll')
def payroll():
   openDb()
   uriTest = 'Payroll'
   cursor.execute("SELECT gaji.id, gaji.nik, karyawan.nama, gaji.tanggal, jabatan.nama_jabatan, gaji.gaji_pokok, jabatan.tunjangan, gaji.total_gaji FROM gaji join karyawan on gaji.nik = karyawan.nik join jabatan on karyawan.jabatan = jabatan.id ORDER BY gaji.id desc")
   container = []
   for id, nik, nama, tanggal, jabatan, gaji_pokok, tunjangan, total_gaji in cursor.fetchall():
      container.append((id, nik, nama, tanggal, jabatan, gaji_pokok, tunjangan, total_gaji, uriTest))
   closeDb()
   return render_template('payroll/list_payroll.html', container=container, uriTest=uriTest)  

@app.route('/tambah_payroll', methods=['GET','POST'])
def tambah_payroll():
   openDb()
   cursor.execute('SELECT karyawan.nik, karyawan.nama, jabatan.tunjangan, karyawan.gaji_pokok FROM karyawan JOIN jabatan ON karyawan.jabatan = jabatan.id')
   dataKaryawan = []
   for nik, nama, tunjangan, gaji_pokok in cursor.fetchall():
      dataKaryawan.append((nik, nama, tunjangan, gaji_pokok))   
   cursor.execute('SELECT MAX(id)+1 FROM gaji')
   dataIdGaji = []
   for id in cursor.fetchall():
      dataIdGaji.append((id))        
   closeDb()   
   uriTest = 'Payroll'
   if request.method == 'POST':
      id = request.form['id']
      nik = request.form['nik']
      tanggal = request.form['date']
      gaji_pokok = request.form['gapok']
      total_gaji = request.form['tot_gaji']
      data = (id, nik, tanggal, gaji_pokok, total_gaji)
      openDb()
      cursor.execute('''
        INSERT INTO gaji VALUES('%s','%s','%s','%s','%s')''' % data)
      conn.commit()
      closeDb()
      return redirect(url_for('payroll'))
   else:
      return render_template('payroll/tambah_payroll.html', dataKaryawan=dataKaryawan, dataIdGaji=dataIdGaji, uriTest=uriTest)

@app.route('/print_payroll/<id>', methods=['GET','POST'])
def print_payroll(id):
   openDb()
   uriTest = 'Print Payroll'
   cursor.execute("SELECT gaji.id, gaji.tanggal,karyawan.nik, karyawan.nama,  karyawan.gaji_pokok, jabatan.tunjangan, gaji.total_gaji FROM karyawan JOIN gaji on karyawan.nik = gaji.nik JOIN jabatan ON karyawan.jabatan = jabatan.id WHERE gaji.id='%s'" % id)
   data = cursor.fetchone()
   closeDb()
   return render_template('payroll/print_payroll.html', data=data, uriTest=uriTest)

@app.route('/hapus_payroll/<id>', methods=['GET','POST'])
def hapus_payroll(id):
   openDb()
   cursor.execute("DELETE FROM gaji WHERE id='%s'" % id)
   conn.commit()
   closeDb()
   return redirect(url_for('payroll'))

# jabatan
@app.route('/jabatan')
def jabatan():
   openDb()
   uriTest = 'Master Jabatan'
   cursor.execute('SELECT * FROM jabatan')
   container = []
   for id, nama_jabatan, tunjangan in cursor.fetchall():
      container.append((id, nama_jabatan, tunjangan, uriTest))
   closeDb()
   return render_template('jabatan/list_jabatan.html', container=container, uriTest=uriTest)  

@app.route('/tambah_jabatan', methods=['GET','POST'])
def tambah_jabatan():
   uriTest = 'Master Jabatan'
   if request.method == 'POST':
      id = request.form['id']
      nama_jabatan = request.form['nama_jabatan']
      tunjangan = request.form['tunjangan']
      data = (id, nama_jabatan, tunjangan)
      openDb()
      cursor.execute('''
        INSERT INTO jabatan VALUES('%s','%s','%s')''' % data)
      conn.commit()
      closeDb()
      return redirect(url_for('jabatan'))
   else:
      return render_template('jabatan/tambah_jabatan.html', uriTest=uriTest)

@app.route('/ubah_jabatan/<id>', methods=['GET','POST'])
def ubah_jabatan(id):
   openDb()
   uriTest = 'Master Karyawan'
   cursor.execute("SELECT * FROM jabatan WHERE id='%s'" % id)
   data = cursor.fetchone()
   if request.method == 'POST':
      id = request.form['id']
      nama_jabatan = request.form['nama_jabatan']
      tunjangan = request.form['tunjangan']
      cursor.execute('''
         UPDATE jabatan SET nama_jabatan='%s', tunjangan='%s'
         WHERE id='%s'
      ''' % (nama_jabatan, tunjangan, id))
      conn.commit()
      closeDb()
      return redirect(url_for('jabatan'))
   else:
      closeDb()
      return render_template('jabatan/ubah_jabatan.html', data=data, uriTest=uriTest)

@app.route('/hapus_jabatan/<id>', methods=['GET','POST'])
def hapus_jabatan(id):
   openDb()
   cursor.execute("DELETE FROM jabatan WHERE id='%s'" % id)
   conn.commit()
   closeDb()
   return redirect(url_for('jabatan'))

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
