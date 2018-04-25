import os
import platform
import sqlite3

def new_gig_idx( dbh, gig_venue, gig_date ):
    gig_query = 'SELECT gig_idx FROM gigs WHERE venue=? AND gig_date=?'
    dbh.execute( gig_query, (gig_venue, gig_date))
    gig_idx = dbh.fetchone()
    print( 'gig_idx = ',gig_idx)
    return gig_idx

def new_gig_read_gig_file( gig_file ):
    gig_fh = open( gig_file, 'r' )
    gig_venue = gig_fh.readline().rstrip()
    gig_date  = gig_fh.readline().rstrip()
    set_lists = gig_fh.readline().split(',')
    gig_fh.close()
    return (gig_venue, gig_date, set_lists )

def gig_delete( dbh, gig_idx ):
    del_from_gigs = 'DELETE FROM gigs WHERE gig_idx = ?'
    del_from_sets = 'DELETE FROM set_lists WHERE gig_idx = ?'
    dbh.execute( del_from_gigs, gig_idx )
    dbh.execute( del_from_sets, gig_idx )
    

if __name__ == "__main__":
    if platform.node() == "5CB345145G":  # work PC
        music_db = '/scratch/setlist/music_db.sqlite'
    else:
        music_db = '/Users/sisyp/Documents/SONA/scripts/music_db.sqlite'
    mdbh = sqlite3.connect( music_db )
    mc = mdbh.cursor()
    
    gig_file = input('Name of gig file> ')
    the_gig = new_gig_read_gig_file( gig_file )
    gig_idx = new_gig_idx( mc, the_gig[0], the_gig[1] )
    if gig_idx != None:
        gig_delete( mc, gig_idx )
        
    mdbh.commit()
    mdbh.close()