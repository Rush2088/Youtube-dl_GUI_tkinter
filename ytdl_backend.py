import subprocess
import json
import os

def download(url, fid, dir1):
    # Use python based youtube-dl
    global p,q

    print('downloading')
    ydl=f"youtube-dl.exe"
    params=f"-f {fid} --restrict-filenames --extract-audio --audio-format mp3 --newline "
    # --extract-audio --audio-format mp3
    out= f'-o "{dir1}/%(title)s.%(ext)s"'
    shellcmd = f'{ydl} {out} {params} {url}'

    p=subprocess.run(shellcmd,  shell=True, 
    stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    if p.returncode==0:
        print('successfully completed')
        q= 100


def validate_urls(queue):
    ydl='youtube-dl'
    url= queue.get()    ##### multi process friendly
    params='-j'  #json dump
    shellcmd = f'{ydl} {params} {url}'

    f1=subprocess.run(shellcmd,  shell=True, capture_output=True, text=True)
    if f1.returncode:
        out_tuple =(1,'---Error---', '','')
        # return

    else:
        Formats =f1.stdout
        # print(Formats)
        extracted = json.loads(Formats)  # returns a dictionary
        # filter out only title, preferred format, size

        filtered = [ x for x in extracted['formats'] if x['format_id']=='140']
        if not filtered:
            filtered = [ x for x in extracted['formats'] if x['format_note']=='tiny']
        selected=filtered[-1]
        title_tmp= extracted['_filename'].split('-')
        title= '-'.join(title_tmp[:-1]) # title name in windows friendly format
        fid= selected['format_id']   # format code for selected audio best quality
        filesize=round(selected['filesize']/(1024*1024),2)  # file size in MB
        filesize = str(filesize)+'MB'
        out_tuple = (0,title, fid, filesize)
    queue.put(out_tuple)
        # return title, fid ,filesize




if __name__ == "__main__":
    download('https://www.youtube.com/watch?v=Yc5OyXmHD0w', 140, 'C:/Users/Rashmil/Downloads' )

