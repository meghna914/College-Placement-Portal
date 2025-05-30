# Database Management Routes - Add to app.py

@app.route('/admin/database')
@login_required
@role_required(['admin'])
def view_database():
    """View database tables"""
    # Get all tables and their row counts
    tables = []
    for table_name in db.metadata.tables.keys():
        table = db.metadata.tables[table_name]
        count = db.session.execute(db.select(db.func.count()).select_from(table)).scalar()
        tables.append({
            'name': table_name,
            'count': count
        })
    
    return render_template(
        'database-viewer.html',
        db_tables=tables,
        selected_table=None,
        table_data=None
    )

@app.route('/admin/database/<table_name>')
@login_required
@role_required(['admin'])
def view_database_table(table_name):
    """View contents of a specific database table"""
    # Get all tables and their row counts for the sidebar
    tables = []
    for t_name in db.metadata.tables.keys():
        table = db.metadata.tables[t_name]
        count = db.session.execute(db.select(db.func.count()).select_from(table)).scalar()
        tables.append({
            'name': t_name,
            'count': count
        })
    
    # Security check - make sure the table exists
    if table_name not in db.metadata.tables:
        flash('Table not found', 'error')
        return redirect(url_for('view_database'))
    
    # Get the table data
    table = db.metadata.tables[table_name]
    result = db.session.execute(db.select(table)).all()
    
    # Format data for the template
    columns = [c.name for c in table.columns]
    rows = [dict(row) for row in result]
    
    table_data = {
        'columns': columns,
        'rows': rows
    }
    
    return render_template(
        'database-viewer.html',
        db_tables=tables,
        selected_table=table_name,
        table_data=table_data
    )

@app.route('/admin/backup-database')
@login_required
@role_required(['admin'])
def backup_database():
    """Create a backup of the database"""
    import sqlite3
    import shutil
    from datetime import datetime
    
    # Create backups directory if it doesn't exist
    backups_dir = os.path.join(app.root_path, 'backups')
    os.makedirs(backups_dir, exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'placement_portal_backup_{timestamp}.db'
    backup_path = os.path.join(backups_dir, backup_filename)
    
    # Get database path
    db_path = os.path.join(app.root_path, 'instance', 'placement_portal.db')
    
    # Copy the database file
    shutil.copy2(db_path, backup_path)
    
    flash(f'Database backup created: {backup_filename}', 'success')
    return redirect(url_for('view_database'))

@app.route('/admin/reset-test-data')
@login_required
@role_required(['admin'])
def reset_test_data():
    """Reset the database with test data"""
    try:
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin@example.com').first()
        if not admin:
            new_admin = User(
                username='admin@example.com',
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                role='admin',
                is_approved=True
            )
            db.session.add(new_admin)
        
        # Add test data here as needed
        # For example, test students, companies, and jobs
        
        db.session.commit()
        flash('Test data has been reset successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error resetting test data: {str(e)}', 'error')
    
    return redirect(url_for('view_database'))

# Add a route to fetch table data via AJAX
@app.route('/admin/table/<table_name>')
@login_required
@role_required(['admin'])
def get_table_data(table_name):
    """Get table data in JSON format for AJAX calls"""
    # Security check - make sure the table exists
    if table_name not in db.metadata.tables:
        return jsonify({'error': 'Table not found'})
        
    try:
        # Get the table data
        table = db.metadata.tables[table_name]
        result = db.session.execute(db.select(table)).all()
        
        # Format data for the response
        columns = [c.name for c in table.columns]
        rows = [dict(row) for row in result]
        
        return jsonify({
            'columns': columns,
            'rows': rows
        })
    except Exception as e:
        return jsonify({'error': str(e)})
