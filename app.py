from flask import Flask, render_template, request, flash, send_file, redirect, session 
import pandas as pd  
import os  
from CRUD.Creat import creat
from CRUD.Update import update  
from CRUD.Delete import delete
from clean import cleanData 


app = Flask(__name__, static_folder='static')  
app.secret_key = 'your_secret_key_here'  # Thêm khóa bí mật  

# Đọc dữ liệu từ tệp CSV  
file_path = 'data_dirty.csv'  
data = pd.read_csv(file_path)  
cleaned_file_path = 'cleaned_data.csv'  
ROWS_PER_PAGE = 12  

def paginate_data(data, page, rows_per_page):  
    start_idx = (page - 1) * rows_per_page  
    end_idx = start_idx + rows_per_page  
    paginated_data = data.iloc[start_idx:end_idx]  
    table_data = paginated_data.to_dict(orient='records')  
    total_pages = (len(data) + rows_per_page - 1) // rows_per_page  
    start_page = max(1, page - 2)  
    end_page = min(total_pages, page + 2)  
    nearby_pages = range(start_page, end_page + 1)  

    return {  
        "table_data": table_data,  
        "total_pages": total_pages,  
        "has_next": page < total_pages,  
        "has_prev": page > 1,  
        "nearby_pages": nearby_pages,  
    }  

@app.route('/')  
def index():  
    # Đọc lại dữ liệu từ tệp CSV để đảm bảo có dữ liệu mới  
    data = pd.read_csv(file_path)  
    page = int(request.args.get('page', 1))  
    pagination = paginate_data(data, page, ROWS_PER_PAGE)  
    
    return render_template(  
        'index.html',  
        table_data=pagination["table_data"],  
        headers=data.columns,  
        page=page,  
        total_pages=pagination["total_pages"],  
        has_next=pagination["has_next"],  
        has_prev=pagination["has_prev"],  
        nearby_pages=pagination["nearby_pages"]  
    )  

@app.route('/add', methods=['GET', 'POST'])  
def add_data():  
    if request.method == 'POST':  
        Date = request.form['Date']  
        Country_Region = request.form['Country_Region']  
        Confirmed = int(request.form['Confirmed'])  
        Deaths = int(request.form['Deaths'])  
        Recovered = int(request.form['Recovered'])  
        Active = int(request.form['Active'])  
        New_cases = int(request.form['New_cases'])  
        New_deaths = int(request.form['New_deaths'])  
        New_recovered = int(request.form['New_recovered'])  
        WHO_Region = request.form['WHO_Region']  
        if (Confirmed < 0 or Deaths < 0 or Recovered < 0 or
            Active < 0 or New_cases < 0 or New_deaths < 0 or
            New_recovered < 0):
            flash("Giá trị nhập vào phải lớn hơn hoặc bằng 0!", 'danger')
            return redirect('/update')

        new_row = [Date, Country_Region, Confirmed, Deaths, Recovered, Active, New_cases, New_deaths, New_recovered, WHO_Region]  

        try:  
            creat(file_path, new_row)  
            flash("Dòng mới đã được thêm vào thành công!", 'success')  
            return redirect('/add')  
        except Exception as e:  
            flash(f"Lỗi: {str(e)}", 'danger')  
            return redirect('/add')  

    return render_template('add.html')  

# Thêm route xử lý tải lên file CSV  
@app.route('/upload_csv', methods=['POST'])  
def upload_csv():  
    if 'file' not in request.files:  
        flash('Không có tệp nào được chọn', 'danger')  
        return redirect('/add')  

    file = request.files['file']  
    if file.filename == '':  
        flash('Tệp không hợp lệ', 'danger')  
        return redirect('/add')  

    if file and file.filename.endswith('.csv'):  
        try:  
            file_upload = os.path.join('uploads', file.filename)  
            file.save(file_upload)  

            # Đọc tệp CSV và kiểm tra các trường dữ liệu  
            new_data = pd.read_csv(file_upload)  
            if set(new_data.columns) != set(data.columns):  
                flash('Tệp CSV không có cùng các trường dữ liệu với dữ liệu hiện có', 'danger')  
                return redirect('/add')  

            # Thêm dữ liệu mới vào dữ liệu hiện có  
            new_data.to_csv(file_path, mode='a', header=False, index=False)  
            flash(f'Dữ liệu từ {file.filename} đã được thêm thành công!', 'success')  
            return redirect('/add')  
        except Exception as e:  
            flash(f"Lỗi khi thêm dữ liệu từ tệp CSV: {str(e)}", 'danger')  
            return redirect('/add')  

    flash('Vui lòng chọn tệp CSV hợp lệ', 'danger')  
    return redirect('/add') 
# Các route khác cho chức năng sửa, xóa, làm sạch, thống kê và biểu đồ  
@app.route('/update', methods=['GET', 'POST'])
def update_data():
    if request.method == 'POST':  
        date_to_search = request.form.get('Date')  
        country_to_search = request.form.get('Country_Region')  

        if 'Confirmed' in request.form:  # Nếu tồn tại trường Confirmed, nghĩa là đang cập nhật dữ liệu  
            try:  
                # Validate dữ liệu đầu vào  
                updated_data = [  
                    request.form['Date'],  
                    request.form['Country_Region'],  
                    int(request.form['Confirmed']),  
                    int(request.form['Deaths']),  
                    int(request.form['Recovered']),  
                    int(request.form['Active']),  
                    int(request.form['New_cases']),  
                    int(request.form['New_deaths']),  
                    int(request.form['New_recovered']),  
                    request.form['WHO_Region']  
                ]  
                
                # Thực hiện update  
                update(file_path, updated_data)  
                
                # Flash message chi tiết bằng tiếng Việt   
                flash(f"Cập nhật dữ liệu cho {updated_data[1]} vào ngày {updated_data[0]} thành công!", 'success')  
            except ValueError as ve:  
                # Bắt lỗi nhập số không hợp lệ  
                flash(f"Đầu vào không hợp lệ: {str(ve)}. Vui lòng nhập các giá trị số chính xác.", 'danger')  
            except Exception as e:  
                # Bắt các lỗi khác  
                flash(f"Lỗi khi cập nhật bản ghi: {str(e)}", 'danger')  
            
            return redirect('/update')  
        
        # Nếu chỉ tìm kiếm  
        try:  
            data = pd.read_csv(file_path)  
            
            # Xử lý ngày tháng chính xác hơn  
            data['Date'] = pd.to_datetime(data['Date'], format='mixed', dayfirst=True, errors='coerce')  
            data['Date'] = data['Date'].dt.strftime('%d/%m/%Y')  

            # Tìm kiếm không phân biệt hoa thường  
            record = data[  
                (data['Date'] == date_to_search) &   
                (data['Country/Region'].str.lower() == country_to_search.lower())  
            ]  
            
            if not record.empty:  
                # Convert record to a dictionary for easier access in the template  
                record_dict = record.iloc[0].to_dict()  
                return render_template('update.html', record=record_dict)  
            else:  
                # Nếu không tìm thấy bản ghi  
                flash(f"Không tìm thấy bản ghi cho {country_to_search} vào ngày {date_to_search}", 'warning')  
                return render_template('update.html', search=True)  
        
        except Exception as e:  
            # Xử lý các lỗi có thể xảy ra khi đọc file  
            flash(f"Lỗi khi tìm kiếm bản ghi: {str(e)}", 'danger')  
            return render_template('update.html')  

    # Nếu không có yêu cầu POST, chỉ hiển thị trang update  
    return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_data():
    data = pd.read_csv(file_path)
    page = int(request.args.get('page', 1))
    pagination = paginate_data(data, page, ROWS_PER_PAGE)

    # Xử lý xóa dữ liệu khi người dùng gửi form
    if request.method == 'POST':
        rows_to_delete = request.form.getlist('rows_to_delete')
        if rows_to_delete:
            rows_to_delete = [int(row)+(page-1)*12 for row in rows_to_delete]
            # Xóa các dòng được chọn
            delete(file_path,data,rows_to_delete)
            flash("Dữ liệu đã được xóa thành công!", 'success')
            return redirect('/delete')

    return render_template(
        'delete.html',
        table_data=pagination["table_data"],
        page=page,
        total_pages=pagination["total_pages"],
        has_next=pagination["has_next"],
        has_prev=pagination["has_prev"],
        nearby_pages=pagination["nearby_pages"]
    )





@app.route('/clean', methods=['GET', 'POST'])
def clean_data():
    if request.method == 'POST':  # Chỉ thực hiện khi nhấn nút "Clean"
        # Làm sạch dữ liệu
        cleaned_data = cleanData(file_path)

        # Lưu dữ liệu đã làm sạch vào file CSV
        cleaned_data.to_csv(cleaned_file_path, index=False)
        cleaned_data.to_csv(file_path, index=False)

        flash("Dữ liệu đã được làm sạch thành công!", "success")

        # Chuyển hướng để hiển thị dữ liệu đã làm sạch
        return redirect('/clean')

    # Phân trang dữ liệu hiện tại (chưa làm sạch nếu chưa nhấn nút)
    data = pd.read_csv(file_path)
    page = int(request.args.get('page', 1))
    pagination = paginate_data(data, page, ROWS_PER_PAGE)

    # Hiển thị dữ liệu trên giao diện
    return render_template(
        'clean.html',
        table_data=pagination["table_data"],
        headers=data.columns,
        page=page,
        total_pages=pagination["total_pages"],
        has_next=pagination["has_next"],
        has_prev=pagination["has_prev"],
        nearby_pages=pagination["nearby_pages"],
    )

@app.route('/download_clean_data')  
def download_clean_data():  
    return send_file(cleaned_file_path, as_attachment=True)  

@app.route('/statistics')
def statistics():
    return "Trang Thống Kê"

@app.route('/chart')
def chart():
    return "Trang Vẽ Biểu Đồ"

if __name__ == '__main__':
    app.run(debug=True)