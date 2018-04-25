import os
import platform
import sqlite3

def arr_idx( dbc, arr_name ):
    arr_query = 'SELECT argmnt_idx FROM arrangements WHERE filepath = ?'
    dbc.execute( arr_query, (arr_name,))
    arridx = dbc.fetchone()
    return arridx
    
def arr_insert( dbc, arr_name ):
    arr_cmd = 'INSERT INTO arrangements (filepath) VALUES (?)'
    dbc.execute( arr_cmd, (arr_name,))
    
if __name__ == "__main__":
    if platform.node == '5CB345145G':
        music_db = '/scratch/setlist/music_db.sqlite'
        arrngmnt_dir = '/scratch/setlist'
    else:
        music_db = '/Users/sisyp/Documents/SONA/scripts/music_db.sqlite'
        arrngmnt_dir = '/Users/sisyp/Documents/SONA/'
    
    mdbh = sqlite3.connect( music_db )
    mc = mdbh.cursor()

    update_count=0
    arr_files = os.listdir( arrngmnt_dir )
    for arr in arr_files:
        idx = arr_idx( mc, arr )
        if idx == None:
            arr_insert(mc, arr)
            print( 'adding ', arr )
            update_count += 1
            
    mdbh.commit()
    mdbh.close()
    print( update_count, ' records updated')    