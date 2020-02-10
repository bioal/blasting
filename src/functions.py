from ftplib import FTP

# writes line
def write_line( fp, string ):
    fp.write( string )
    fp.write( '\n')

# downloads file 
def download( server, path, output_file ):
    ftp = FTP( server )
    ftp.login( 'anonymous', '' )

    print( path )
    fp = open( output_file, 'w', encoding='UTF-8' )
    ftp.retrlines( 'RETR ' + path, lambda s: write_line( fp, s ) )
    fp.close()









