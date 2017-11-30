#!/usr/bin/env python
# -*- coding: utf8 -*-

# Thanks to http://elinux.org/RPi_Email_IP_On_Boot_Debian
import subprocess
import os
import datetime

def connection_type(word_list):
    """ This function takes a list of words, then, depeding which key word, returns the corresponding
    internet connection type as a string. ie) 'ethernet'.
    """
    if 'wlan0' in word_list or 'wlan1' in word_list:
        con_type = 'wifi'
    elif 'eth0' in word_list:
        con_type = 'ethernet'
    else:
        con_type = 'current'

    return con_type

timestamp = ('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

arg='ip route list | grep wlan0'  # Linux command to retrieve ip addresses.
# Runs 'arg' in a 'hidden terminal'.
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()  # Get data from 'p terminal'.

# Split IP text block into three, and divide the two containing IPs into words.
ip_lines = data[0].splitlines()
split_line_a = ip_lines[1].split()
#split_line_b = ip_lines[2].split()

# connection_type variables for the message text. ex) 'ethernet', 'wifi', etc.
ip_type_a = connection_type(split_line_a)
#ip_type_b = connection_type(split_line_b)

"""Because the text 'src' is always followed by an ip address,
we can use the 'index' function to find 'src' and add one to
get the index position of our ip.
"""
ipaddr_a = split_line_a[split_line_a.index('src')+1]
#ipaddr_b = split_line_b[split_line_b.index('src')+1]

# Creates a sentence for each ip address.
my_ip_a = '%s: %s IP addr is <a href="http://%s">%s</a>' % (timestamp, ip_type_a, ipaddr_a, ipaddr_a)
#my_ip_b = 'Your %s ip is %s' % (ip_type_b, ipaddr_b)

print my_ip_a

# --------------------------------------------------------------
# Upload the wlan0 address to the web server

# Web server used for the photobooth
remote_account        = '[USER AND SERVER ADDRESS OF REMOTE SERVER]' # the username and host of the remote server
remote_file_dir       = os.path.join('public_html', 'other', 'climb') # path to upload images to on web server
remote_url_prefix     = 'www.eoghan.me.uk/other/climb' # the public website URL to the above remote_file_dir

# Ensure the remote dir exits
# TODO: How expensive are calls to mkdir if dir already exists, 
#       better to check dir exists first?
subprocess.check_call("ssh " + remote_account + " 'mkdir -p " + 
                      remote_file_dir + "'", shell=True)

# Write the IP address to a file called ip.html
subprocess.check_call("echo '" + my_ip_a + "<br>' | ssh " + remote_account + " 'cat >> " + 
                      remote_file_dir + "/ip.html'", shell=True)


# Now copy the processed result of the content.php folder onto the server
#    (still call it .php even though it's pure HTML, just for simplicity of the index.html file)
subprocess.check_call("wget -q -O - localhost/content.php | ssh " + remote_account + " 'cat > " + 
                      remote_file_dir + "/content.php'", shell=True)
